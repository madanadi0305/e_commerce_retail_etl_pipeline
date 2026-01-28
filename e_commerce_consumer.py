from kafka import KafkaConsumer
import os
from dotenv import load_dotenv
load_dotenv()
import json 
import time 
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import pandas as pd
import psycopg2
from psycopg2 import DatabaseError

def consumer():
    connection = None
    cursor = None
    try:
        consumer = KafkaConsumer(
            os.getenv('KAFKA_TOPIC'),
            bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        connection = psycopg2.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME')
        )
        cursor = connection.cursor()
        
        print(f"Consumer started - Topic: {os.getenv('KAFKA_TOPIC')}, Database: {os.getenv('DB_NAME')}\n")
        
        for message in consumer:
            try:
                msg_type = message.value.get('type')
                msg_data = message.value.get('data')
                timestamp = message.value.get('timestamp')
                
                print(f"Received {msg_type} message at {timestamp}")
                
                if msg_type == 'orders':
                    for order in msg_data:
                        cursor.execute("""
                            INSERT INTO orders (order_id, customer_id, product_id, product_name, quantity, price, total_amount, order_added_at, order_updated_at, status, payment_method, shipping_address)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (order_id) DO UPDATE SET
                                customer_id = EXCLUDED.customer_id,
                                product_id = EXCLUDED.product_id,
                                product_name = EXCLUDED.product_name,
                                quantity = EXCLUDED.quantity,
                                price = EXCLUDED.price,
                                total_amount = EXCLUDED.total_amount,
                                order_updated_at = EXCLUDED.order_updated_at,
                                status = EXCLUDED.status,
                                payment_method = EXCLUDED.payment_method,
                                shipping_address = EXCLUDED.shipping_address
                        """, (
                            order.get('order_id'),
                            order.get('customer_id'),
                            order.get('product_id'),
                            order.get('product_name'),
                            order.get('quantity'),
                            order.get('price'),
                            order.get('total_amount'),
                            order.get('order_added_at'),
                            order.get('order_updated_at'),
                            order.get('status', 'pending'),
                            order.get('payment_method'),
                            order.get('shipping_address')
                        ))
                    connection.commit()
                    print(f"✓ Inserted/Updated {len(msg_data)} orders")
                
                elif msg_type == 'products':
                    for product in msg_data:
                        cursor.execute("""
                            INSERT INTO products (product_id, product_name, category, price, quantity, product_added_at, product_updated_at, description, brand)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (product_id) DO UPDATE SET
                                product_name = EXCLUDED.product_name,
                                category = EXCLUDED.category,
                                price = EXCLUDED.price,
                                quantity = EXCLUDED.quantity,
                                product_updated_at = EXCLUDED.product_updated_at,
                                description = EXCLUDED.description,
                                brand = EXCLUDED.brand
                        """, (
                            product.get('product_id'),
                            product.get('product_name'),
                            product.get('category'),
                            product.get('price'),
                            product.get('quantity', 0),
                            product.get('product_added_at'),
                            product.get('product_updated_at'),
                            product.get('description'),
                            product.get('brand')
                        ))
                    connection.commit()
                    print(f"✓ Inserted/Updated {len(msg_data)} products")
                
                elif msg_type == 'customers':
                    for customer in msg_data:
                        cursor.execute("""
                            INSERT INTO customers (customer_id, customer_name, email, total_orders, customer_added_at, customer_updated_at, city, state, country, zip_code, phone_number)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (customer_id) DO UPDATE SET
                                customer_name = EXCLUDED.customer_name,
                                email = EXCLUDED.email,
                                total_orders = EXCLUDED.total_orders,
                                customer_updated_at = EXCLUDED.customer_updated_at,
                                city = EXCLUDED.city,
                                state = EXCLUDED.state,
                                country = EXCLUDED.country,
                                zip_code = EXCLUDED.zip_code,
                                phone_number = EXCLUDED.phone_number
                        """, (
                            customer.get('customer_id'),
                            customer.get('customer_name'),
                            customer.get('email'),
                            customer.get('total_orders', 0),
                            customer.get('customer_added_at'),
                            customer.get('customer_updated_at'),
                            customer.get('city'),
                            customer.get('state'),
                            customer.get('country'),
                            customer.get('zip_code'),
                            customer.get('phone_number')
                        ))
                    connection.commit()
                    print(f"✓ Inserted/Updated {len(msg_data)} customers")
                
                elif msg_type == 'sales_summary':
                    cursor.execute("""
                        INSERT INTO sales_summary (total_revenue, total_orders, total_customers, sales_summary_added_at)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        msg_data.get('total_revenue'),
                        msg_data.get('total_orders'),
                        msg_data.get('total_customers'),
                        msg_data.get('sales_summary_added_at')
                    ))
                    connection.commit()
                    print(f"✓ Inserted sales_summary")
                
            except Exception as e:
                print(f"Error processing message: {e}")
                if connection:
                    connection.rollback()
                continue
    
    except KeyboardInterrupt:
        print("\nShutting down consumer...")
    except Exception as e:
        print(f"Consumer error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("Consumer closed")

if __name__ == "__main__":
    consumer()