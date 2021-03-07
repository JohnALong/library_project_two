from django.urls import path
from .views import *

app_name = "libraryapptwo"

urlpatterns = [
    path('', book_list, name='home'),
    path('books/', book_list, name='books'),
    path('librarians/', list_librarians, name='librarians'),
    path('libraries/', list_libraries, name='libraries'),
]