from django.shortcuts import render

# Create your views here.
from catalog.models import Author, Book, BookInstance, Genre

#def index(request):
#    """View function for home page of site."""
#
#    # Generate counts of some of the main objects
#    num_books = Book.objects.all().count()
#    num_instances = BookInstance.objects.all().count()
#
#    # Available books (status = 'a')
#    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
#
#    # The 'all()' is implied by default
#    num_authors = Author.objects.count()
#
#    # Instances of books that contain the word django
#    # Here: book is a foreign key in model BookInstance, so we reference the Book and its title.
#    num_instances_of_books_containing_django = BookInstance.objects.filter(book__title__icontains='django').count()
#
#    context = {
#        'num_books': num_books,
#        'num_instances': num_instances,
#        'num_instances_available': num_instances_available,
#        'num_authors': num_authors,
#        'num_instances_of_books_containing_django': num_instances_of_books_containing_django,
#    }
#
#    # Render the HTML template index.html with the data in the context variable
#    return render(request, 'index.html', context=context)
#    # render() accepts:
#    #   - original request  -   HttpRequest
#    #   - an HTML template  -   with PLACEHOLDERS for the data
#    #   - context variable  -   which is a Python dict, containing the data to insert into the PLACEHOLDERS
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

    # ACCESSING SESSION DATA (COOKIE VALUE)
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)   # If not already set, set to 0
    request.session['num_visits'] = num_visits + 1      # Maybe check if cookies are even supported in the browser
                                                        # https://docs.djangoproject.com/en/2.1/topics/http/sessions/

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_instances_of_books_containing_django': num_instances_of_books_containing_django,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
    # render() accepts:
    #   - original request  -   HttpRequest
    #   - an HTML template  -   with PLACEHOLDERS for the data
    #   - context variable  -   which is a Python dict, containing the data to insert into the PLACEHOLDERS



# Create a class-based view
from django.views import generic

class BookListView(generic.ListView):
    model = Book
    # The generic view will query the db to get all records for the specified model Book
    # and
    # then render() a template located at "/locallibrary/catalog/templates/catalog/book_list.html"
    # within the template - can access the list of books with the template var: object_list OR book_list
    # i.e. generically - "the_model_name_list"
    #
    # generic views look for templates in /application_name/the_model_name_list.html
    # (catalog/book_list.html in this case)
    # inside the application's /application_name/templates/ directory
    # (/catalog/templates/)
    #
    # can alter the above
    # for example here:
    #
    # List top 5 books read by other users
    # context_object_name = 'my_book_list'    # our own name for the list as a template variable
    # queryset = Book.object.filter(title__icontains='django')[:5]    # Get 5 books containing the title 'django'
    # template_name = 'books/my_arbitrary_template_name_list.html'    # Specify our own template name/location

    # Can also override methods in class-based views
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='django')[:5]
    #
    # or for example override get_context_data() in order to pass additional context vars to the template
    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first -> get context
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     # Create data & add to the context
    #     context['some_data'] = 'some data'
    #     return context
    #
    # When doing this it is important to follow the pattern used above:
    # - First get the existing context from our superclass.
    # - Then add your new context information.
    # - Then return the new (updated) context.

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author


# Add a view that will list all BookInstance objects currently loaned to a specific user.
# We only want this view to be available to logged-in users.
# For this reason, we are going to use:	LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
	"""Generic class-based view listing books on looan to current user."""
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by = 10

	# Using 'get_queryset' we can restrict the list to BookInstance objects for the current user.
	# locallibrary/catalog/models.py -> BookInstance -> LOAN_STATUS (===array where 'o' means on_loan)
	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class BooksByUserAsStaffListView(LoginRequiredMixin, generic.ListView):
	permission_required = ('catalog.can_mark_returned')
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_staff.html'
	paginate_by = 10

	def get_queryset(self):
		return BookInstance.objects.filter(status__exact='o')	# objects.all()

