from django.contrib import admin

# Register your models here.

from .models import Author, Book, BookInstance, Genre, Language



class BookInline(admin.StackedInline):  # StackedInline - Different layout
    model = Book
    extra = 0   # show no empty values underneath the ones that exist

# Author
# Previously:
#admin.site.register(Author)
# Changed to:
# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    # pass    # If pass is defined here the Admin site behaviour won't be changed
    # list_display -> which column names to show
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # fields -> column order of appearance (& layout - Fields in a tuple are displayed horizontally)
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)


# Similarly:
# Book
# admin.site.register(Book)
#
# But, we are declaring a class extending admin.TabularInLine
# to be able to modify related items from the Detail View.
# So,
# 1) we create: class BooksInstanceInline
# 2) we add the "inlines" attribute to the BookAdmin admin.ModelAdmin class
# These 2 add an inline block in the Book Details View.
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

class BookAdmin(admin.ModelAdmin):
    # pass
    list_display = ('title', 'author', 'display_genre')
    # as genre is a ManyToManyField we cannot display it directly in list_display()
    # instead we:
    # 1) (catalog/models.py) - In the Book Class defined a function to get the info as a string
    #                           display_genre()
    # 2) (catalog/models.py) - In the Book Class define the attribute
    #                           display_genre - which returns output of the above function.
    # as:
    #   def display_genre(self):
    #       """Create a string for the Genre. This is required to display genre in Admin."""
    #       return ', '.join(genre.name for genre in self.genre.all()[:3])
    #   display_genre.short_description = 'Genre'
    #
    # Note from the docs: Getting the genre may not be a good idea here, because of the "cost"
    # of the database operation.
    # We're showing you how because calling functions in your models can be
    # very useful for other reasons — for example to add a Delete link next to every
    # item in the list.
    inlines = [BooksInstanceInline]


# Register the admin class with the associated model
admin.site.register(Book, BookAdmin)


# We are changing BookInstanceAdmin as well, but;
# Instead we could use the decorator "@register"
# and achieve the exact same thing, but with different syntax.
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    # pass
    list_filter = ('status', 'due_back')
    # Once you've got a lot of items in a list, it can be useful to be able to
    # filter which items are displayed.
    # This is done by listing fields in the list_filter attribute.
    #

    # list_display = ('status', 'due_back', 'id')
    list_display = ('book', 'status', 'borrower', 'due_back')
    exclude = ['id']

    # Add "Sections" in detail view
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint')   # , 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )


# Models Language and Genre won't be changed so they are left unchanged
admin.site.register(Language)
admin.site.register(Genre)
