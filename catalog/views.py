from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Book, Author, BookInstance

# =======================
# Home Page
# =======================
def index(request):
    """View function for home page of site."""
    # Count objects
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    # Track visits in the session
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits + 1,
    }

    return render(request, 'catalog/index.html', context)

# =======================
# Book Views
# =======================
class BookListView(ListView):
    model = Book
    template_name = 'catalog/book_list.html'

class BookDetailView(DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'

class BookCreate(CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'book_image']
    template_name = 'catalog/book_form.html'

class BookUpdate(UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'book_image']
    template_name = 'catalog/book_form.html'

class BookDelete(DeleteView):
    model = Book
    template_name = 'catalog/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')

# =======================
# Author Views
# =======================
class AuthorListView(ListView):
    model = Author
    template_name = 'catalog/author_list.html'

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death', 'author_image']
    template_name = 'catalog/author_form.html'

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death', 'author_image']
    template_name = 'catalog/author_form.html'

class AuthorDelete(DeleteView):
    model = Author
    template_name = 'catalog/author_confirm_delete.html'
    success_url = reverse_lazy('author_list')

# =======================
# Borrowed Books by Current User
# =======================
class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user,
            status__exact='o'
        ).order_by('due_back')

# =======================
# Available Books & Loaning
# =======================
@login_required
def available_books(request):
    available = BookInstance.objects.filter(status__exact='a')
    return render(request, 'catalog/available_books.html', {'available_books': available})

def staff_required(user):
    return user.is_staff

@login_required
@user_passes_test(staff_required)
def loan_book(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    users = User.objects.all()

    if request.method == 'POST':
        borrower_id = request.POST.get('borrower')
        borrower = get_object_or_404(User, pk=borrower_id)

        if book_instance.status == 'a':
            book_instance.status = 'o'
            book_instance.borrower = borrower
            book_instance.save()
            return redirect('available_books')

    return render(request, 'catalog/loan_book.html', {
        'book_instance': book_instance,
        'users': users
    })

# =======================
# User Registration
# =======================
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
