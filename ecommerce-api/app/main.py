import uvicorn
from fastapi import FastAPI
from app.routers import products, users, orders, categories
from app.database import engine, Base

# Database table initialization.
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Register routes.
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])


@app.get("/")
async def root():
    return {"message": "Welcome to the E-commerce API"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)




