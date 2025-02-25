import os
from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    price = Column(Float)
    quantity = Column(Integer)
    order_type = Column(String)

Base.metadata.create_all(bind=engine)

class OrderCreate(BaseModel):
    symbol: str
    price: float
    quantity: int
    order_type: str

active_connections: List[WebSocket] = []

async def notify_clients(order: Order):
    for connection in active_connections:
        await connection.send_json({
            "id": order.id,
            "symbol": order.symbol,
            "price": order.price,
            "quantity": order.quantity,
            "order_type": order.order_type
        })

@app.post("/orders/")
async def create_order(order: OrderCreate):
    db = SessionLocal()
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    await notify_clients(db_order)
    db.close()
    return db_order

@app.get("/orders/")
def read_orders():
    db = SessionLocal()
    orders = db.query(Order).all()
    db.close()
    return orders

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception as e:
        print(f"Connection closed: {e}")
    finally:
        active_connections.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)