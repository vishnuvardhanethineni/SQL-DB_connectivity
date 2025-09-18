import os
from supabase import create_client , Client
from dotenv import load_dotenv
load_dotenv()
url=os.getenv("SUPABASE_URL")
key=os.getenv("SUPABASE_KEY")
sb:Client = create_client(url,key)
def add_book(title,author,category,stock):
    payload={'title':title,'author':author,'category':category,'stock':stock}
    resp = sb.table('books').insert(payload).execute()
    return resp.data 
def add_member(name,email):
    payload = {'name': name , 'email':email}
    resp = sb.table('members').insert(payload).execute()
    return resp.data 
def list_books():
    resp = sb.table("books").select("*").order("book_id", desc=False).execute()
    return resp.data
def update_stock(book_id,stock):
    resp =sb.table('books').update({'stock':stock}).eq('book_id',book_id).execute()
    return resp.data
def update_member(name,email):
    resp =sb.table('members').update({'email':email}).eq('name',name).execute()
    return resp.data
def search_books(title=None, author=None, category=None):
    query = sb.table("books").select("*")
    if title:
        query = query.ilike("title", f"%{title}%")
    if author:
        query = query.ilike("author", f"%{author}%")
    if category:
        query = query.ilike("category", f"%{category}%")
    resp = query.execute()
    return resp.data
def member_detils_and_borrowed_books():
    resp = sb.table('borrow_records').select('*').order('record_id',desc=False).execute()
    return resp.data
def delete_book_if_not_borrowed(book_id: int):
    try:
        borrowed = sb.table("borrowed") \
                 .select("borrow_id") \
                 .eq("book_id", book_id) \
                 .execute()
    
        if borrowed.data:  
            return f" Cannot delete book {book_id} (it has been borrowed)."
    

        resp = sb.table("books") \
             .delete() \
             .eq("book_id", book_id) \
             .execute()
        return resp.data
    except :
        return ("Book_id record is not present")

def delete_member_if_no_borrows(member_id: int):
    try:
        borrowed = sb.table("borrowed") \
                 .select("borrow_id") \
                 .eq("member_id", member_id) \
                 .execute()
    
        if borrowed.data:  
            return f" Cannot delete member {member_id} (has borrowed books)."
    
        resp = sb.table("members") \
             .delete() \
             .eq("member_id", member_id) \
             .execute()
        return resp.data
    except :
        return ("Member not present in database")
if __name__=='__main__':
    while True:
        print("\n===== Library Menu =====")
        print("1. Add Book")
        print("2. Add Member")
        print("3. List Books")
        print("4. Update Stock")
        print("5. Update Member Email")
        print("6. Search Books")
        print("7. Member & Borrowed Books")
        print("8. Delete Book (if not borrowed)")
        print("9. Delete Member (if no borrowed books)")
        print("0. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            title = input("Enter title: ")
            author = input("Enter author: ")
            category = input("Enter category: ")
            stock = int(input("Enter stock: "))
            print(add_book(title, author, category, stock))

        elif choice == '2':
            name = input("Enter member name: ")
            email = input("Enter member email: ")
            print(add_member(name, email))

        elif choice == '3':
            books = list_books()
            for b in books:
                print(b)

        elif choice == '4':
            book_id = int(input("Enter Book ID: "))
            stock = int(input("Enter new stock: "))
            print(update_stock(book_id, stock))

        elif choice == '5':
            name = input("Enter member name: ")
            email = input("Enter new email: ")
            print(update_member(name, email))

        elif choice == '6':
            title = input("Enter title keyword (or leave blank): ")
            author = input("Enter author keyword (or leave blank): ")
            category = input("Enter category keyword (or leave blank): ")
            results = search_books(title if title else None,
                                   author if author else None,
                                   category if category else None)
            for r in results:
                print(r)

        elif choice == '7':
            records = member_detils_and_borrowed_books()
            for r in records:
                 print(r)

        elif choice == '8':
            book_id = int(input("Enter Book ID to delete: "))
            print(delete_book_if_not_borrowed(book_id))

        elif choice == '9':
            member_id = int(input("Enter Member ID to delete: "))
            print(delete_member_if_no_borrows(member_id))

        elif choice == '0':
            print("Exiting program...")
            break
        else :
            print('Invalid choice')