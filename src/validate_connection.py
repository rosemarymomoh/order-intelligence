import sys
sys.path.append('../src')
from api_client import get_commercetools_client
import pandas as pd
from datetime import datetime, timedelta

def test_commercetools_connection():
    """Comprehensive test of commercetools API connection and data"""
    
    print("🔍 Testing commercetools connection...")
    
    try:
        # 1. Test basic connection
        client = get_commercetools_client()
        project = client.project().get()
        print(f"✅ Connected to project: {project.name}")
        print(f"   Project key: {project.key}")
        print(f"   Currencies: {project.currencies}")
        
        # 2. Test orders endpoint
        print("\n📊 Testing orders data...")
        
        # Try different time ranges to find data
        test_ranges = [7, 30, 90, 365]  # days
        
        for days in test_ranges:
            since_date = datetime.now() - timedelta(days=days)
            
            orders = client.orders().get(
                where=f'createdAt > "{since_date.isoformat()}"',
                limit=50
            )
            
            print(f"   Last {days} days: {orders.total} orders found")
            
            if orders.total > 0:
                # Found data - let's examine it
                sample_orders = orders.results[:5]
                
                print(f"\n📋 Sample data from last {days} days:")
                for i, order in enumerate(sample_orders[:3]):
                    print(f"   Order {i+1}:")
                    print(f"     ID: {order.id}")
                    print(f"     Created: {order.created_at}")
                    print(f"     Total: {order.total_price.cent_amount/100} {order.total_price.currency_code}")
                    print(f"     Items: {len(order.line_items)}")
                    
                    # Check line items
                    if order.line_items:
                        item = order.line_items[0]
                        print(f"     First item: {item.name}")
                
                # Create test DataFrame
                order_data = []
                for order in sample_orders:
                    order_data.append({
                        'id': order.id,
                        'created_at': order.created_at,
                        'total_price': order.total_price.cent_amount / 100,
                        'currency': order.total_price.currency_code,
                        'order_state': order.order_state,
                        'item_count': len(order.line_items)
                    })
                
                df = pd.DataFrame(order_data)
                print(f"\n📈 DataFrame created successfully:")
                print(df.head())
                print(f"\nDataFrame info:")
                print(df.info())
                
                return True, days, orders.total
        
        print("⚠️  No orders found in any time range - this might be a demo/empty project")
        return True, None, 0
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False, None, 0

def test_other_endpoints():
    """Test other commercetools endpoints to understand available data"""
    
    print("\n🔍 Testing other data endpoints...")
    
    client = get_commercetools_client()
    
    # Test products
    try:
        products = client.products().get(limit=5)
        print(f"   Products: {products.total} available")
        if products.results:
            sample_product = products.results[0]
            print(f"   Sample product: {sample_product.master_data.current.name}")
    except Exception as e:
        print(f"   Products: Error - {e}")
    
    # Test customers
    try:
        customers = client.customers().get(limit=5)
        print(f"   Customers: {customers.total} available")
    except Exception as e:
        print(f"   Customers: Error - {e}")
    
    # Test categories
    try:
        categories = client.categories().get(limit=5)
        print(f"   Categories: {categories.total} available")
    except Exception as e:
        print(f"   Categories: Error - {e}")

if __name__ == "__main__":
    success, days_with_data, order_count = test_commercetools_connection()
    
    if success:
        print(f"\n✅ commercetools connection: VALIDATED")
        if days_with_data:
            print(f"   Data available: {order_count} orders in last {days_with_data} days")
        else:
            print(f"   Data status: Empty project (this is OK for testing)")
        
        test_other_endpoints()
        
        print(f"\n🚀 Ready to proceed to MCP testing!")
    else:
        print(f"\n❌ Fix commercetools connection before proceeding to MCP")
        