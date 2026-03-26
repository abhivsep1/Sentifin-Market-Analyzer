import sys
sys.path.insert(0, "D:/project_imp")

from model.stocks import fetch_prices
from database.db import init_price_table, insert_prices, get_prices_by_ticker

# initialize price table
init_price_table()
print("Price table ready")

# fetch prices
print("\nFetching prices...")
prices = fetch_prices()
print(f"Fetched {len(prices)} price records")
print("\nSample:")
print(prices[0])

# store in database
insert_prices(prices)
print("\nStored successfully")

# verify
print("\nVerifying TSLA prices from database:")
rows = get_prices_by_ticker("TSLA")
for row in rows:
    print(row)