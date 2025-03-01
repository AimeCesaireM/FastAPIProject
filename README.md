# FastAPI Orders Application

## Overview
This project is a simple REST API built with FastAPI for managing trade orders. It supports real-time order status updates via WebSocket and stores order data in a PostgreSQL database. The application is containerized using Docker and Docker Compose for easy deployment.

## Features
- **REST API**: Create and retrieve trade orders.
- **WebSocket**: Real-time order status updates.
- **PostgreSQL**: Persistent storage for order data.
- **Docker**: Containerized application for consistent environments.
- **Docker Compose**: Multi-container setup for local development.

## Prerequisites
- Docker
- Docker Compose

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/AimeCesaireM/FastAPIProject.git
cd FastAPIProject
pip install -r requirements.txt
```

### Step 2: Modify your ```docker-compose.yml``` file.
Modify the lines:
```
DATABASE_URL=postgresql://user:password@db:5432/trades
```
and
```
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password 
```
The ``` user``` and ```password``` will be the user and passwords to your database.

### Step 3: Build and Run the Application
```bash
docker-compose up --build
```

### Step 4: Access the Application
- **API Documentation**: http://localhost:8000/docs
- **WebSocket Endpoint**: `ws://localhost:8000/ws`

## API Endpoints

### Create Order
- **URL**: `/orders/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "symbol": "AAPL",
    "price": 150.0,
    "quantity": 10,
    "order_type": "buy"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "symbol": "AAPL",
    "price": 150.0,
    "quantity": 10,
    "order_type": "buy"
  }
  ```

### Get Orders
- **URL**: `/orders/`
- **Method**: `GET`
- **Response**:
  ```json
  [
    {
      "id": 1,
      "symbol": "AAPL",
      "price": 150.0,
      "quantity": 10,
      "order_type": "buy"
    }
  ]
  ```

## WebSocket
Connect to the WebSocket endpoint at `ws://localhost:8000/ws` to receive real-time updates on new orders.

## Development

### Installing Dependencies
If you need to run the application outside of Docker, install the dependencies using:
```bash
pip install -r requirements.txt
```

### Running the Application
Run the application using Uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Database
The application uses PostgreSQL for persistent storage. The database configuration is specified in the `docker-compose.yml` file.

### Creating a New Database User and Database
1. **Access the PostgreSQL prompt**:
    ```bash
    sudo -i -u postgres
    psql
    ```

2. **Create a new user and database**:
    ```sql
    CREATE USER yourusername WITH PASSWORD 'yourpassword';
    CREATE DATABASE yourdatabase;
    GRANT ALL PRIVILEGES ON DATABASE yourdatabase TO yourusername;
    ```
The ``` yourusername``` and ```yourpassword``` should match the ones defined in the ```docker-compose.yml``` file

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
---
