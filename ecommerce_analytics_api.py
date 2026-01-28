from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uvicorn

app = FastAPI(
    title="E-Commerce Analytics API",
    description="Basic analytics API for e-commerce data",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orders_store = []
products_store = []
customers_store = []


class Order(BaseModel):
    order_id: str
    customer_id: str
    product_id: str
    product_name: str
    quantity: int
    price: float
    total_amount: float
    order_added_at: str
    order_updated_at: Optional[str] = None
    status: Optional[str] = "pending"
    payment_method: Optional[str] = None
    shipping_address: Optional[str] = None


class Product(BaseModel):
    product_id: str
    product_name: str
    category: str
    price: float
    quantity: Optional[int] = 0
    product_added_at: Optional[str] = None
    product_updated_at: Optional[str] = None
    description: Optional[str] = None
    brand: Optional[str] = None


class Customer(BaseModel):
    customer_id: str
    customer_name: str
    email: str
    total_orders: int
    customer_added_at: Optional[str] = None
    customer_updated_at: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip_code: Optional[str] = None
    phone_number: Optional[str] = None


class SalesSummary(BaseModel):
    total_revenue: float
    total_orders: int
    total_customers: int

@app.post("/orders")
async def create_order(order: Order):
     new_order = {
         "order_id": order.order_id,
         "customer_id": order.customer_id,
         "product_id": order.product_id,
         "product_name": order.product_name,
         "quantity": order.quantity,
         "price": order.price,
         "total_amount": order.total_amount,
         "order_added_at": order.order_added_at if order.order_added_at else datetime.now().isoformat(),
         "order_updated_at": order.order_updated_at,
         "status": order.status,
         "payment_method": order.payment_method,
         "shipping_address": order.shipping_address
     }
     orders_store.append(new_order)
     return {
        "message": f"Order created successfully with order_id {order.order_id}",
        "order": new_order
     }
@app.get("/")
async def root():
    return {
        "message": "E-Commerce Analytics API",
        "version": "1.0.0",
        "endpoints": {
            "orders": "/orders",
            "products": "/products",
            "customers": "/customers",
            "sales_summary": "/sales/summary"
        }
    }


@app.get("/orders", response_model=List[Order])
async def get_orders(limit: int = Query(10, ge=1, le=100)):
    mock_orders = [
        Order(
            order_id="ORD001",
            customer_id="CUST001",
            product_id="PROD001",
            product_name="Wireless Headphones",
            quantity=2,
            price=70.00,
            total_amount=140.00,
            order_added_at=datetime.now().isoformat(),
            status="completed",
            payment_method="credit_card",
            shipping_address="123 Main St, New York, NY 10001"
        ),
        Order(
            order_id="ORD002",
            customer_id="CUST002",
            product_id="PROD002",
            product_name="Smart Watch",
            quantity=1,
            price=200.00,
            total_amount=200.00,
            order_added_at=datetime.now().isoformat(),
            status="pending",
            payment_method="paypal",
            shipping_address="456 Oak Ave, Seattle, WA 98101"
        )
    ]
    all_orders = mock_orders + [Order(**order) for order in orders_store]
    return all_orders[-limit:]


@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    return Order(
        order_id=order_id,
        customer_id="CUST001",
        product_id="PROD001",
        product_name="Wireless Headphones",
        quantity=1,
        price=70.00,
        total_amount=70.00,
        order_added_at=datetime.now().isoformat(),
        status="completed",
        payment_method="credit_card",
        shipping_address="123 Main St, New York, NY 10001"
    )


@app.post("/products")
async def create_product(product: Product):
    new_product = {
        "product_id": product.product_id,
        "product_name": product.product_name,
        "category": product.category,
        "price": product.price,
        "quantity": product.quantity if product.quantity else 0,
        "product_added_at": product.product_added_at if product.product_added_at else datetime.now().isoformat(),
        "product_updated_at": product.product_updated_at,
        "description": product.description,
        "brand": product.brand
    }
    products_store.append(new_product)
    return {
        "message": f"Product created successfully with product_id {product.product_id}",
        "product": new_product
    }


@app.get("/products", response_model=List[Product])
async def get_products(limit: int = Query(10, ge=1, le=100)):
    mock_products = [
        Product(
            product_id="PROD001",
            product_name="Wireless Headphones",
            category="Electronics",
            price=70.00,
            quantity=150,
            product_added_at=datetime.now().isoformat(),
            description="High-quality wireless headphones with noise cancellation",
            brand="TechAudio"
        ),
        Product(
            product_id="PROD002",
            product_name="Smart Watch",
            category="Electronics",
            price=200.00,
            quantity=75,
            product_added_at=datetime.now().isoformat(),
            description="Feature-rich smartwatch with fitness tracking",
            brand="FitTech"
        ),
        Product(
            product_id="PROD003",
            product_name="Laptop Stand",
            category="Accessories",
            price=30.00,
            quantity=200,
            product_added_at=datetime.now().isoformat(),
            description="Ergonomic aluminum laptop stand",
            brand="DeskPro"
        )
    ]
    all_products = mock_products + [Product(**product) for product in products_store]
    return all_products[-limit:]


@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    return Product(
        product_id=product_id,
        product_name="Sample Product",
        category="Electronics",
        price=50.00,
        quantity=100,
        product_added_at=datetime.now().isoformat(),
        description="Sample product description",
        brand="GenericBrand"
    )


@app.post("/customers")
async def create_customer(customer: Customer):
    new_customer = {
        "customer_id": customer.customer_id,
        "customer_name": customer.customer_name,
        "email": customer.email,
        "total_orders": customer.total_orders,
        "customer_added_at": datetime.now().isoformat(),
        "city": customer.city,
        "state": customer.state,
        "country": customer.country,
        "zip_code": customer.zip_code,
        "phone_number": customer.phone_number,
        "customer_updated_at": datetime.now().isoformat()
    }
    customers_store.append(new_customer)
    return {
        "message": "Customer created successfully with customer_id " + customer.customer_id,
        "customer": new_customer
    }


@app.get("/customers", response_model=List[Customer])
async def get_customers(limit: int = Query(10, ge=1, le=100)):
    mock_customers = [
        Customer(
            customer_id="CUST001",
            customer_name="John Doe",
            email="john@example.com",
            total_orders=5,
            customer_added_at= str(datetime.now().isoformat()),
        city= "New York",
        state= "NY",
        country= "USA",
        zip_code= "10001",
        phone_number=" 243-345-6789",
        customer_updated_at= str(datetime.now().isoformat())
        ),
        Customer(
            customer_id="CUST002",
            customer_name="Jane Smith",
            email="jane@example.com",
            total_orders=3,
            customer_added_at=str(datetime.now().isoformat()),
            city="Seattle",
            state="WA",
            country="USA",
            zip_code="98101",
            phone_number="243-345-6789",
            customer_updated_at=str(datetime.now().isoformat())
        )
    ]
    all_customers = mock_customers + [Customer(**customer) for customer in customers_store]
    return all_customers[-limit:]


@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: str):
    return Customer(
        customer_id=customer_id,
        customer_name="John Doe",
        email="john@example.com",
        total_orders=5
    )


@app.get("/sales/summary", response_model=SalesSummary)
async def get_sales_summary():
    return SalesSummary(
        total_revenue=125430.50,
        total_orders=1247,
        total_customers=2340
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
