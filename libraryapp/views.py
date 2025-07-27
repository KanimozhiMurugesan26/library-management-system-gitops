from unicodedata import category

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from datetime import datetime

# Helper function to execute raw SQL

def fetch_one(query, params=()):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchone()

def fetch_all(query, params=()):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()

def execute_sql(query, params=()):
    with connection.cursor() as cursor:
        cursor.execute(query, params)

# LOGIN VIEW
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = fetch_one("SELECT user_id, role FROM Users WHERE email=%s AND password=%s", (email, password))
        if user:
            request.session['user_id'] = user[0]
            request.session['role'] = user[1]
            if user[1] == 'admin':
                return redirect('admin_books')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'libraryapp/login.html')

# REGISTER VIEW (stub only, implement insert if needed)
#def register(request):
   # if request.method == 'POST':
      #  messages.success(request, 'Register called')
       # return redirect('login')
    #return render(request, 'libraryapp/register.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Default values
        role = 'User'
        membership_status = 'Active'

        # Insert into Users table
        execute_sql(
            "INSERT INTO Users (Name, Email, Password, Role, Membership_status) VALUES (%s, %s, %s, %s, %s)",
            (name, email, password, role, membership_status)
        )

        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')
    return render(request, 'libraryapp/register.html')

# USER DASHBOARD
def dashboard(request):
    user_id = request.session.get('user_id')
    borrowed_books = fetch_all("SELECT B.Title, T.borrow_date, T.return_date, B.Book_Id FROM Transactions T JOIN Books B ON T.User_User_id = B.Book_Id WHERE T.User_User_id=%s AND T.return_date IS NULL", (user_id,))
    return render(request, 'libraryapp/dashboard.html', {'borrowed_books': borrowed_books})

# LIST BOOKS
def books(request):
    role = request.session.get('role')
    if role == 'admin':
        books = fetch_all("SELECT * FROM Books")
    else:
        books = fetch_all("SELECT * FROM Books WHERE Availability IN (1, 2)")
    return render(request, 'libraryapp/books.html', {'books': books})

# BORROW BOOK
def borrow(request):
    user_id = request.session.get('user_id')
    book_id = request.GET.get('book_id')
    now = datetime.now()
    execute_sql("INSERT INTO Transactions (borrow_date, User_User_id, Books_Book_Id) VALUES (%s, %s, %s)", (now, user_id, book_id))
    execute_sql("UPDATE Books SET Availability = 2 WHERE Book_Id = %s", (book_id,))
    messages.success(request, 'Book borrowed')
    return redirect('dashboard')

# RETURN BOOK
def return_book(request):
    user_id = request.session.get('user_id')
    book_id = request.GET.get('book_id')
    now = datetime.now()
    execute_sql("UPDATE Transactions SET return_date=%s WHERE user_user_id=%s AND books_book_id=%s AND return_date IS NULL", (now, user_id, book_id))
    execute_sql("UPDATE Books SET Availability = 1 WHERE Book_Id=%s", (book_id,))
    messages.success(request, 'Book returned')
    return redirect('dashboard')

# RESERVE BOOK
def reserve(request):
    user_id = request.session.get('user_id')
    book_id = request.GET.get('book_id')
    now = datetime.now()
    execute_sql("INSERT INTO reservations (Request_date, Status, User_User_id, Books_Book_Id) VALUES (%s, 'Pending', %s, %s)", (now, user_id, book_id))
    messages.success(request, 'Book reserved')
    return redirect('dashboard')

# ADMIN - MANAGE BOOKS
def admin_books(request):
    if request.method == 'POST':
        if 'add' in request.POST:
            title = request.POST['title']
            author = request.POST['author']
            genre = request.POST['genre']
            availability = request.POST.get('availability', '1')  # Default to '1' (available) if missing
            if availability == '':
                availability = 1
            else:
                availability = int(availability)
            category= request.POST['category_id']
            execute_sql("INSERT INTO Books (Title, Author, Genre, Availability,Category_Category_id) VALUES (%s, %s, %s, %s, %s )", (title, author, genre, availability,category))
            messages.success(request, 'Book added')
        elif 'delete' in request.POST:
            book_id = request.POST['book_id']
            execute_sql("DELETE FROM Books WHERE Book_Id=%s", (book_id,))
            messages.success(request, 'Book deleted')
        elif 'edit' in request.POST:
            book_id = request.POST['book_id']
            title = request.POST['title']
            author = request.POST['author']
            genre = request.POST['genre']
            availability = request.POST.get('availability', '1')  # Default to '1' (available) if missing
            if availability == '':
                availability = 1
            else:
                availability = int(availability)
            execute_sql("UPDATE Books SET Title=%s, Author=%s, Genre=%s, Availability=%s WHERE Book_Id=%s", (title, author, genre, availability, book_id))
            messages.success(request, 'Book updated')
    books = fetch_all("SELECT * FROM Books")
    categories = fetch_all("SELECT category_id, category_name FROM Categories")
    return render(request, 'libraryapp/admin_books.html', {'books': books,
                                                           'categories': categories })
# ADMIN - TRANSACTIONS
def reservations(request):
    role = request.session.get('role')
    if role == 'admin':
        transactions = fetch_all("SELECT T.transaction_id, B.Title, U.name, T.borrow_date, T.return_date FROM Transactions T JOIN Users U ON T.user_id = U.user_id JOIN Books B ON T.book_id = B.Book_Id")
    else:
        transactions = []
    return render(request, 'libraryapp/reservations.html', {'transactions': transactions})
