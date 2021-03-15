import sqlite3
from django.shortcuts import render, redirect, reverse
from libraryapptwo.models import Library, model_factory, Book
from django.contrib.auth.decorators import login_required
from ..connection import Connection

def create_library(cursor, row):
    _row = sqlite3.Row(cursor, row)

    library = Library()
    library.id = _row["id"]
    library.title = _row["title"]
    library.address = _row["address"]

    # blank books list to be populated later
    library.books = []
    
    book = Book()
    book.id = _row["book_id"]
    book.title = _row["book_title"]
    book.author = _row["author"]
    book.isbn = _row["isbn"]
    book.year_published = _row["year_published"]

    # return tuple containing library and book build from data in current row of data set
    return (library, book)

@login_required
def list_libraries(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = create_library
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT
                li.id,
                li.title,
                li.address,
                b.id book_id,
                b.title book_title,
                b.author,
                b.year_published,
                b.isbn
            FROM libraryapptwo_library li
            JOIN libraryapptwo_book b ON li.id = b.location_id
            """)

            # all_libraries = []
            all_libraries = db_cursor.fetchall()

            library_groups = {}

            for (library, book) in all_libraries:

                # if dict has a key of current library id value, add the key and set the value to the current library
                if library.id not in library_groups:
                    library_groups[library.id] = library
                    library_groups[library.id].books.append(book)

                # if key does not exist, append current book to the list of books for current library
                else:
                    library_groups[library.id].books.append(book)

                print("test1", library_groups)

            # for row in dataset:
            #     lib = Library()
            #     lib.id = row["id"]
            #     lib.address = row["address"]
            #     lib.title = row["title"]

            #     all_libraries.append(lib)

        template = 'libraries/list.html'

        context = {
            'all_libraries': library_groups.values()
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()
            db_cursor.execute("""
            INSERT INTO libraryapptwo_library
            (
                title, address
            )
            VALUES (?, ?)
            """,
            (form_data['title'], form_data['address']))

        return redirect(reverse('libraryapptwo:libraries'))


