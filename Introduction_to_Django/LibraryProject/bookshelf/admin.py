from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Fields shown in list view
    search_fields = ('title', 'author')  # Search bar filters
    list_filter = ('publication_year',)  # Sidebar filters

admin.site.register(Book, BookAdmin)
