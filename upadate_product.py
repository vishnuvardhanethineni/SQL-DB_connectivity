from supabase import create_client, Client
from dotenv import load_dotenv
import os
 
load_dotenv()
 
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)
def update_product(product_id,stock):
    resp =sb.table('products').update({'stock':stock}).eq('product_id',product_id).execute()
    return resp.data
if __name__=='__main__':
    product_id =int(input("Enter product id: "))
    stock =int(input("Enter stock value: "))
    updated=update_product(product_id,stock)
    print(updated)