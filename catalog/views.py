from django.shortcuts import render

# Create your views here.
from catalog.models import Author, Book, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default
    num_authors = Author.objects.count()

    # Instances of books that contain the word django
    # Here: book is a foreign key in model BookInstance, so we reference the Book and its title.
    num_instances_of_books_containing_django = BookInstance.objects.filter(book__title__icontains='django').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_instances_of_books_containing_django': num_instances_of_books_containing_django,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
    # render() accepts:
    #   - original request  -   HttpRequest
    #   - an HTML template  -   with PLACEHOLDERS for the data
    #   - context variable  -   which is a Python dict, containing the data to insert into the PLACEHOLDERS
