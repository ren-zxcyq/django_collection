from django.db import models

# Create your models here.

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    # No verbose_name has been defined, so the field will be called 'Name' in forms.


    def __str__(self):
        """String representing the Model object."""
        return self.name


class Language(models.Model):
    """Model representing a language books are written in."""
    name = models.CharField(max_length=50, help_text='Enter a language.')

    def __str__(self):
        """Returns the URL to access a particular author instance."""
        return self.name


from django.urls import reverse # Used to generate URLs by reversing the URL patterns

class Book(models.Model):
    """Model representing a book (not a specific copy)."""
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one one author, but authors can have multiple books.
    # Author as a string rather than object because it hasn't been declared yet in the file.
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # null = True - allows the db to store a NULL if no author is selected
    # on_delete=models.SET_NULL which will set the value of the author to Null if the associated author record is deleted.
    #
    # ForeignKey Setup - We set up the Author ForeignKey using a string because the Author class is not defined yet (it is defined after the Book class).

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    # ForeignKey Setup - We set up the Language ForeignKey using the class name because the Language class is defined before the Book class.

    def __str__(self):
        """String representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
        # get_absolute_url() returns a URL that can be used to access a detail record for this model
        # (for this to work we will have to define a URL mapping that has the name book-detail, and
        # define an associated view and template).

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

# ForeignKey -> Identify the associated Book (depicting a 1-Many relationship)


import uuid # Required for unique book instances

class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. one that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across the whole library')
    # UUIDField is used for the id field to set it as the primary_key for this model.
    # This type of field allocates a globally unique value for each instance.

    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    # due_back can be   blank or null   -    needed when the book is available
    # (Class Meta) uses this field to order records when they are returned in a query

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )
    # status is a CharField that defines a choice/selection list.
    # LOAN_STATUS is the tuple that defines this list.
    # The value in a key/value pair is a display value that a user can select,
    # The keys are the values that are actually saved if the option is selected.
    # 'm' will be the value that books will have before they are stocked on the shelves (when they are bought by the library and are not yet available)


    class Meta:
        ordering = ['due_back'] # When queried, order tables by column 'due_back'
    
    def __str__(self):
        """String representing the Model object."""
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    # both date_of_birth & date_of_death are optional
    # 'Died'

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])
    # get_absolute_url() method reverses the author-detail URL mapping to get the URL for displaying an individual author.

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'