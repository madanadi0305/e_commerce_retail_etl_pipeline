import json
import time
import os
import requests
import pandas as pd
from kafka import KafkaProducer
from dotenv import load_dotenv
from datetime import datetime
import logging
from urllib3 import request

load_dotenv()
#df_orders = pd.DataFrame()
#df_products = pd.DataFrame()
#df_sales_summary = pd.DataFrame()
#df_customers = pd.DataFrame()
base_url = "http://localhost:8000"
api_endpoints = {
    'orders': '/orders',
    'products': '/products',
    'sales_summary': '/sales/summary',
    'customers': '/customers'
}

seen_records = {
    'orders': set(),
    'products': set(),
    'customers': set()
}

def producer():
    producer = KafkaProducer(
        bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    
    print(f"Starting producer - Kafka: {os.getenv('KAFKA_BOOTSTRAP_SERVERS')}, Topic: {os.getenv('KAFKA_TOPIC')}")
    
    try:
        while True:
            data_orders = None
            data_products = None
            data_sales_summary = None
            data_customers = None
            
            for api_endpoint in api_endpoints:
                if api_endpoint == 'orders':
                    data_orders = requests.get(base_url + api_endpoints[api_endpoint]).json()      
                if api_endpoint == 'products':
                    data_products = requests.get(base_url + api_endpoints[api_endpoint]).json()      
                if api_endpoint == 'sales_summary':
                    data_sales_summary = requests.get(base_url + api_endpoints[api_endpoint]).json()      
                if api_endpoint == 'customers':
                    data_customers = requests.get(base_url + api_endpoints[api_endpoint]).json()
            
            if data_orders:
                for order in data_orders:
                    if not order.get('order_added_at'):
                        order['order_added_at'] = datetime.now().isoformat()
                    if not order.get('order_updated_at'):
                        order['order_updated_at'] = datetime.now().isoformat()
                message_orders = {'type': 'orders', 'data': data_orders, 'timestamp': datetime.now().isoformat()}
                producer.send(os.getenv('KAFKA_TOPIC'), value=message_orders)
                print(f"Sent {len(data_orders)} orders to Kafka")
            
            if data_products:
                for product in data_products:
                    if not product.get('product_added_at'):
                        product['product_added_at'] = datetime.now().isoformat()
                    if not product.get('product_updated_at'):
                        product['product_updated_at'] = datetime.now().isoformat()
                message_products = {'type': 'products', 'data': data_products, 'timestamp': datetime.now().isoformat()}
                producer.send(os.getenv('KAFKA_TOPIC'), value=message_products)
                print(f"Sent {len(data_products)} products to Kafka")
            
            if data_sales_summary:
                if not data_sales_summary.get('sales_summary_added_at'):
                    data_sales_summary['sales_summary_added_at'] = datetime.now().isoformat()
                message_sales = {'type': 'sales_summary', 'data': data_sales_summary, 'timestamp': datetime.now().isoformat()}
                producer.send(os.getenv('KAFKA_TOPIC'), value=message_sales)
                print(f"Sent sales_summary to Kafka")
            
            if data_customers:
                for customer in data_customers:
                    if not customer.get('customer_added_at'):
                        customer['customer_added_at'] = datetime.now().isoformat()
                    if not customer.get('customer_updated_at'):
                        customer['customer_updated_at'] = datetime.now().isoformat()
                message_customers = {'type': 'customers', 'data': data_customers, 'timestamp': datetime.now().isoformat()}
                producer.send(os.getenv('KAFKA_TOPIC'), value=message_customers)
                print(f"Sent {len(data_customers)} customers to Kafka")
            
            send_email(data_orders, data_products, data_sales_summary, data_customers)
            time.sleep(5)
                
    except KeyboardInterrupt:
        print("\nShutting down producer...")
    finally:
        producer.flush()
        producer.close()
        print("Producer closed")

def send_email(data_orders, data_products, data_sales_summary, data_customers):
     sender = "madandi0305@gmail.com"
     receiver = "madandi0305@gmail.com"
     
     orders_count = len(data_orders) if data_orders else 0
     products_count = len(data_products) if data_products else 0
     sales_count = 1 if data_sales_summary else 0
     customers_count = len(data_customers) if data_customers else 0
     
     message = f"Sent {orders_count} orders, {products_count} products, {sales_count} sales summary, {customers_count} customers at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
     print(message)
    
if __name__ == "__main__":
    producer()