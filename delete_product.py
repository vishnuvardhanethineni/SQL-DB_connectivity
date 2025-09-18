import os
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()
url=os.getenv("SUPABASE_URL")
key=os.getenv("SUPABASE_KEY")
sb:Client = create_client(url,key)
def delete_product(product_id):
    resp = sb.table("products").delete().eq('product_id',product_id).execute()
    return resp.data
if __name__=='__main__':
    product_id = int(input("Enter product_id : "))
    deleted = delete_product(product_id)
    print(deleted)