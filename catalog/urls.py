from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

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

    # User registration
    path('register/', views.register, name='register'),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),

    # Password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
