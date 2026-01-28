# E-Commerce Analytics API

A comprehensive FastAPI-based analytics API for e-commerce platforms providing real-time insights into sales, customers, products, and business metrics.

## Features

- **Sales Analytics**: Revenue, orders, average order value, and items sold
- **Customer Insights**: Customer segmentation, retention rates, lifetime value
- **Product Performance**: Top products, category analytics, inventory alerts
- **Conversion Metrics**: Funnel analysis, cart abandonment, conversion rates
- **Revenue Trends**: Time-series data with customizable granularity
- **Real-time Dashboard**: Live metrics for active users and recent activity
- **Geographic Analytics**: Sales breakdown by region and country
- **Multi-channel Analytics**: Revenue analysis across different sales channels

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

Start the server:
```bash
python ecommerce_analytics_api.py
```

Or using uvicorn directly:
```bash
uvicorn ecommerce_analytics_api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, access:
- **Interactive API docs (Swagger)**: http://localhost:8000/docs
- **Alternative docs (ReDoc)**: http://localhost:8000/redoc

## Endpoints

### Core Analytics

- `GET /` - API information and endpoint list
- `GET /analytics/sales` - Sales metrics for specified time period
- `GET /analytics/customers` - Customer analytics and retention metrics
- `GET /analytics/conversion` - Conversion funnel and abandonment rates
- `GET /analytics/realtime` - Real-time dashboard metrics

### Product Analytics

- `GET /analytics/products/top` - Top performing products
- `GET /analytics/products/{product_id}` - Specific product analytics
- `GET /analytics/categories` - Category-level analytics

### Advanced Analytics

- `GET /analytics/revenue/trend` - Revenue trends over time
- `GET /analytics/revenue/by-channel` - Revenue by sales channel
- `GET /analytics/customers/segments` - Customer segmentation data
- `GET /analytics/geographic` - Geographic sales distribution
- `GET /analytics/inventory/alerts` - Inventory alerts and warnings

## Query Parameters

Most endpoints support:
- `time_range`: today, week, month, quarter, year, custom
- `start_date`: Custom start date (YYYY-MM-DD)
- `end_date`: Custom end date (YYYY-MM-DD)
- `limit`: Number of results to return

## Example Usage

### Get monthly sales metrics
```bash
curl "http://localhost:8000/analytics/sales?time_range=month"
```

### Get top 5 products by revenue
```bash
curl "http://localhost:8000/analytics/products/top?limit=5&sort_by=revenue"
```

### Get daily revenue trend
```bash
curl "http://localhost:8000/analytics/revenue/trend?granularity=day"
```

## Integration with Data Sources

This API currently returns mock data. To integrate with real data sources:

1. **Database Integration**: Add SQLAlchemy or your preferred ORM
2. **Kafka Integration**: Connect to Kafka streams for real-time data
3. **Spark Integration**: Use PySpark for large-scale data processing
4. **Cache Layer**: Add Redis for performance optimization

## Next Steps

- Connect to your database (PostgreSQL, MySQL, MongoDB, etc.)
- Integrate with Kafka for real-time event streaming
- Add authentication and authorization
- Implement rate limiting
- Add data validation and error handling
- Set up logging and monitoring
- Deploy to production (Docker, Kubernetes, cloud platforms)

## License

MIT
