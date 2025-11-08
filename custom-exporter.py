"""
Custom Prometheus Exporter for Currency Exchange Rates
Example: collecting currency data (Frankfurter API)
"""

from prometheus_client import start_http_server, Gauge, Info
import requests
import time
from datetime import datetime

# Define the list of currencies you want to track
BASE_CURRENCY = 'USD'
TARGET_CURRENCIES = [
    'EUR', 'JPY', 'GBP', 'AUD', 'CAD', 'CHF', 'CNY', 'INR', 'BRL', 'KZT'
]

# Metric Definitions

# A single Gauge with labels.
currency_exchange_rate = Gauge(
    'currency_exchange_rate',
    'Current exchange rate',
    ['base_currency', 'target_currency']
)

# API Status
currency_api_status = Gauge(
    'currency_api_status',
    'Currency API status (1=up, 0=down)'
)

# Data Timestamp
currency_data_timestamp = Gauge(
    'currency_data_timestamp_seconds',
    'Timestamp of the latest data from the API (Unix epoch)'
)

# Exporter Info
exporter_info = Info(
    'currency_exporter_info',
    'Information about the currency exporter'
)

def fetch_currency_data():
    """
    Get currency data from api.frankfurter.app (free, no key required)
    """
    
    try:
        url = "https://api.frankfurter.app/latest"
        params = {
            'from': BASE_CURRENCY,
            'to': ','.join(TARGET_CURRENCIES)
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        
        rates = data['rates']
        base = data['base']
        
        # Loop through the returned rates and set the Gauge for each
        for currency, rate in rates.items():
            currency_exchange_rate.labels(
                base_currency=base,
                target_currency=currency
            ).set(rate)
        
        # Parse the date string and set the data timestamp
        # The API returns a date string, e.g., "2025-11-07"
        date_str = data['date']
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        timestamp = dt.timestamp()
        currency_data_timestamp.set(timestamp)
             
        # Set API status to 'up'
        currency_api_status.set(1)        
        print(f"Successfully fetched {len(rates)} rates. Base: {base}")
        return True
        
    except requests.exceptions.RequestException as e:
        # Set API status to 'down' on any request failure
        print(f"Error fetching data: {e}")
        currency_api_status.set(0)
        return False
    except Exception as e:
        print(f"An error occurred during data processing: {e}")
        currency_api_status.set(0) # Also set to 0 for parsing errors
        return False


if __name__ == '__main__':
    # Set exporter info
    exporter_info.info({
        'version': '1.1',
        'author': 'Student',
        'source_api': 'api.frankfurter.app',
        'base_currency': BASE_CURRENCY
    })
    
    # Start HTTP server on port 8000
    start_http_server(8000)
    
    # Infinite metrics collection loop
    while True:
        try:
            fetch_currency_data()
        except KeyboardInterrupt:
            print("\nExporter stopping...")
            break
        except Exception as e:
            print(f"An unexpected error occurred in the main loop: {e}")
        
        # Update every 30 seconds
        time.sleep(30)