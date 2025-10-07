from django.contrib import admin
from .models import Book, Author, Genre, BookInstance

# Inline genre display for Book
class BookInline(admin.TabularInline):
    model = Book
    extra = 0

# Enhanced Author admin
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death', 'author_image']
    inlines = [BookInline]

# Enhanced Book admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn')
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'book_image']
    filter_horizontal = ('genre',)

# Genre stays simple
admin.site.register(Genre)

# Enhanced BookInstance admin
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
