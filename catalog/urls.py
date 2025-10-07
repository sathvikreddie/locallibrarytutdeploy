from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    # Book views
    path('book_list/', views.BookListView.as_view(), name='book_list'),
    path('book_detail/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),

    # Author views
    path('author_list/', views.AuthorListView.as_view(), name='author_list'),
    path('author_detail/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),

    # Borrowed books for current user
    path('my_books/', views.LoanedBooksByUserListView.as_view(), name='my_books'),

    # Librarian functions
    path('available/', views.available_books, name='available_books'),
    path('book/<uuid:pk>/loan/', views.loan_book, name='loan_book'),

    # Registration
    path('register/', views.register, name='register'),


]
