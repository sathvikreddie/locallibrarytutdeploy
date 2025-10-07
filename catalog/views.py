from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book, Author
from .models import Book, Author, BookInstance
from django.contrib.auth.mixins import LoginRequiredMixin



# ✅ Homepage view
def index(request):
    return render(request, 'catalog/index.html')

# ✅ Book views
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

# ✅ Author views
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

    from django.contrib.auth.mixins import LoginRequiredMixin
    from .models import BookInstance

    # ✅ Borrowed books by current user
    class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
        model = BookInstance
        template_name = 'catalog/bookinstance_list_borrowed_user.html'
        paginate_by = 10

        def get_queryset(self):
            return BookInstance.objects.filter(
                borrower=self.request.user,
                status__exact='o'
            ).order_by('due_back')

class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user,
            status__exact='o'
        ).order_by('due_back')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import BookInstance

@login_required
def available_books(request):
    available = BookInstance.objects.filter(status__exact='a')
    return render(request, 'catalog/available_books.html', {'available_books': available})

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import BookInstance

@login_required
def loan_book(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if book_instance.status == 'a':
        book_instance.status = 'o'
        book_instance.borrower = request.user
        book_instance.save()

    return redirect('book_detail', pk=book_instance.book.pk)

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Optional: log in after registration
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
