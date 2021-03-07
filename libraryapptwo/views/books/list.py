import sqlite3
from django.shortcuts import render
from libraryapptwo.models import Book
from libraryapptwo.models import model_factory
from django.contrib.auth.decorators import login_required
from ..connection import Connection

@login_required
def book_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:

            conn.row_factory = model_factory(Book)

            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                b.id,
                b.title,
                b.isbn,
                b.author, b.year_published,
                b.librarian_id,
                b.location_id
            from libraryapptwo_book b
            """)

            all_books = db_cursor.fetchall()
            # dataset = db_cursor.fetchall()

            # for row in dataset:
            #     book = Book()
            #     book.id = row['id']
            #     book.title = row['title']
            #     book.isbn = row['isbn']
            #     book.author = row['author']
            #     book.year_published = row['year_published']
            #     book.librarian_id = row['librarian_id']
            #     book.location_id = row['location_id']

            #     all_books.append(book)

        template = 'books/list.html'
        context = {
            'all_books': all_books
        }

        return render(request, template, context)