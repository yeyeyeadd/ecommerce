# E-commerce Backend API

## Description
A simple backend API for an C2C e-commerce platform built using FastAPI.


## Features
- User registration and authentication
- Product management
- Product categories management
- Order processing

## API enhancements and security measures:
Added features:
Authentication: Users need to pass JWT authentication after logging in to limit access to specific APIs.
Permission control: Sellers can add products and buyers can place orders.

## Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Configure the .env file with DATABASE_URL.
4. Run the server in development mode:
   ```bash
   uvicorn app.main:app --reload
5. Serving at: http://127.0.0.1:8000                  
   API docs: http://127.0.0.1:8000/docs               
   Running in production use:   
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

  --host 0.0.0.0 means listening on all network interfaces, --port 8000 means listening on port 8000, and --workers 4 means using 4 worker processes to improve concurrent processing capabilities.                        
6. Run the unit test:
    ```bash
   pytest
   
