# Data loader for commercetools
import pandas as pd
import json
from pathlib import Path

def load_orders_data():
    """Load orders data extracted by TypeScript script"""
    
    data_file = Path(__file__).parent.parent / 'data' / 'orders.json'
    
    if not data_file.exists():
        raise FileNotFoundError(
            "Orders data not found. Run: npm run extract-data"
        )
    
    with open(data_file, 'r') as f:
        orders_data = json.load(f)
    
    df = pd.DataFrame(orders_data)
    
    # Convert date column
    df['createdAt'] = pd.to_datetime(df['createdAt'])
    
    print(f"✅ Loaded {len(df)} orders from {data_file}")
    return df

if __name__ == "__main__":
    df = load_orders_data()
    print(df.head())
    print(df.info())