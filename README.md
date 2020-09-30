# django_experiment
Django Tut Playground @Ix76y

# Notes

## Run the server (Development ONLY)
By default it will serve the site to your local computer (http://127.0.0.1:8000/), but you can also specify other computers on your network to serve to.

- `python3 manage.py runserver`

## Update Models
Run the following commands to define tables or change the db tables whenever you change something in the models.
- `python3 manage.py makemigrations`
- `python3 manage.py migrate`

Optional can specify app name, in order to migrate only the given apps Models etc.
- `python3 manage.py makemigrations catalog`

## Models - Important:
- Models define the structure of stored data.
- including field types & possibly their max size, def vals, selection list options, help text for documentation, label text for forms etc.
- Models are implemented as subclasses of:	django.db.models.Model

- An Example

	```
	from django.db import models

	class MyModelName(models.Model):
		"""A typical class defining a model, derived from the Model class."""

		# Fields
		my_field_name = models.CharField(max_length=20, help_text='Enter field documentation')
		...

		# When used in a form, my_field_name would be 'My field name'

		# Metadata
		class Meta: 
			ordering = ['-my_field_name']

		# Methods
		def get_absolute_url(self):
			"""Returns the url to access a particular instance of MyModelName."""
			return reverse('model-detail-view', args=[str(self.id)])
			
		def __str__(self):
			"""String for representing the MyModelName object (in Admin site etc.)."""
			return self.my_field_name
	```

### Common Field Arguments
- help_text	-	Label for HTML forms
- verbose_name	-	name for the field, used in Field Labels
- default	-	Default Value
- null		-	If True, store blank vals as NULL. (CharField will be stored as an empty string) Def: False
- blank		-	If True, is allowed to be blank in forms. Def: False, meaning you will be forced to provide a val. (Often used with null=True)
- choices	-	A group of choices for this field. Default form widget will be a select box with these choices.
- primary_key	-	If True, sets the current field as the primary key for the model. If no field is specified, Django will add a field automatically (named: id)

### Common Field Types
- CharField	-	Must specify max_length
- TextField	-	Arbitrary length, may specify max_length
- IntegerField	-	Storing int vals, and for validating entered values as ints in forms.
- DateField	-	datetime.date
- DateTimeField	-	datetime.datetime	objects.
			- auto_now=True - declare to set to the curr date whenever the model is saved
			- auto_now_add - to only set the date when the model is first created
			- default - set a def date that can be overriden by the user
- EmailField	-	store & validate
- FileField	-
- ImageField	-	upload files & images.
			- Simply adds validation that the uploaded file is an image.
			- They both have params that define how & where the uploaded files are stored.
- AutoField	-	IntegerField that automatically increments.
			- A PK of this type is automatically added to ur model if you don't specify one.
- ForeignKey	-	specify a one-to-many relationship to another db model.
			- the "one" side represents the model that contains the "key"
- ManyToManyField	specify a many-to-many relationship
			- param on_delete -> specify what happens when the associated record is deleted
				- (e.g. a val of models.SET_NULL would simply set the vall to NULL)
- etc: https://docs.djangoproject.com/en/2.1/ref/models/fields/#field-types


## Metadata
- https://docs.djangoproject.com/en/2.1/ref/models/options/
- ordering = ['title', '-pubdate'] or ['-my_field_name']	-	Ordering upon querying
- verbose_name = 'BetterName'
- define access permissions	- different than the ones assigned by default
- declare a model class as abstract	- will allow the Model to be used for other Models (and prevent storing records)
- others control how data are stored; they can be used to map the model to a different db that already exists


## Methods
- \_\_str__()		-	Should be defined on every model. Represent individual records in the Admin site.
- get_absolute_url()	-	(usually) URL displays individual model records. (Automatically adds a "View on Site" button to the model's editing screens in the Admin site.
- any other method

## Model Management

- Create & Modify Record
	```
	# Create a new record using the model's constructor
    record = MyModelName(my_field_name="Instance No1")`

	# Save the object into the db.
    record.save()

	# Access the fields using dot syntax
    print(record.id)	# Should return 1 for the first record.print
	# (record.my_field_name)	# Should print 'Instance No1'

	# Save the modified record
	record.my_field_name = "New Instance Name"
	record.save()
	```

- Searching for records
	```
	# Can retrieve records for a model as a QuerySet. (iterable object) - e.g. objects.all()
	all_books = Book.objects.all()

	# Filter the returned QuerySet (text or numeric field).
	wild_books = Book.objects.filter(title__contains='wild')
	number_wild_books = wild_books.count()
	```

-	In general filtering happens like this:
	-	field_name__match_type
	-	field_name__field_name__match_type	-	Will match on: Fiction, Science fiction, non-fiction etc.
		- `books_containing_genre = Book.objects.filter
		(genre__name__icontains='fiction')`
	-	match_type can be:
		-	contains	Case-Sensitive
		-	icontains	insensitive
		-	iexact		insensitive exact match
		-	exact
		-	in, gt
		-	startswith
		-	https://docs.djangoproject.com/en/2.1/ref/models/querysets/#field-lookups
	-	There is a lot more you can do with queries, including backwards searches from related models, chaining filters, returning a smaller set of values etc. https://docs.djangoproject.com/en/2.1/topics/db/queries/

## Model Registering
- After model creation in the dependent app (here: catalog) we need to register our models in:	dependentapp/admin.py
- This populates the Admin area of the site.
- Format of registration: (Contents of catalog/admin.py)
	```
	from django.contrib import admin

	# Register your models here.

	from .models import Language, Genre, Author, Book, BookInstance

	admin.site.register(Language)
	admin.site.register(Genre)
	admin.site.register(Author)
	admin.site.register(Book)
	admin.site.register(BookInstance)
	```

# Creating a superuser
- In order to log on to the admin site, we need an acc with <i>Staff</i> status enabled.
- ?Can further define permissions.
- Creation Process:
  ```
  python3 manage.py createsuperuser
  # Prompts for: Username && email && pass
  # And run server again:
  python3 manage.py runserver
  ```

# Admin Site

## Overview
- You can edit an entry by selecting its name in the link.
  - The edit page for an entry is almost identical to the "Add" page.
  - The main differences are the page title and the addition of Delete, HISTORY and VIEW ON SITE buttons.
  - <b>VIEW ON SITE</b> (button appears because we defined the <b>get_absolute_url()</b> method in our model).
- Can create an instance of a table from a table that contains its ForeignKey
  - In our example we can create a Book from a BookInstance.
- Can actually change how lists appear and what options exist in the Admin site.
  - You can further customise the interface to make it even easier to use. Some of the things you can do are:

    - List views: 
        - Add additional fields/information displayed for each record. 
        - Add filters to select which records are listed, based on date or some other selection value (e.g. Book loan status).
        - Add additional options to the actions menu in list views and choose where this menu is displayed on the form.
    - Detail views
        - Choose which fields to display (or exclude), along with their order, grouping, whether they are editable, the widget used, orientation etc.
        - Add related fields to a record to allow inline editing (e.g. add the ability to add/edit book records while creating their author record).
  - https://docs.djangoproject.com/en/2.1/ref/contrib/admin/

## Modifying Admin site behaviour
- Register a ModelAdmin class	(which describes the layout - Src: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#modeladmin-objects)
  - Open dependentapp/admin.py (in our case: catalog/admin.py) and:
    - Comment out our original registration
    - Create a class that "extends" the admin.ModelAdmin class
    - Register the model using that class
    - Below, you can see the contents of my catalog/admin.py
		```
		from django.contrib import admin

		# Register your models here.

		from .models import Author, Book, BookInstance, Genre, Language


		# Author
		# Previously:
		#admin.site.register(Author)
		# Changed to:
		# Define the admin class
		class AuthorAdmin(admin.ModelAdmin):
			pass    # If pass is defined here the Admin site behaviour won't be changed

		# Register the admin class with the associated model
		admin.site.register(Author, AuthorAdmin)


		# Similarly:
		# Book
		# admin.site.register(Book)
		class BookAdmin(admin.ModelAdmin):
			pass

		# Register the admin class with the associated model
		admin.site.register(Book, BookAdmin)


		# We are changing BookInstanceAdmin as well, but;
		# Instead we could use the decorator "@register"
		# and achieve the exact same thing, but with different syntax.
		@admin.register(BookInstance)
		class BookInstanceAdmin(admin.ModelAdmin):
			pass


		# Models Language and Genre won't be changed so they are left unchanged
		admin.site.register(Language)
		admin.site.register(Genre)
		```
  - Modify the "extending" classes to implement Admin site behaviour.
    - Example:
      - Configure list views
        - The Author list on the Admin site just displayed "Last Name"
        - That was the result of using the object name generated from the model using the \_\_str__() method
        - list_display() instead of \_\_str__() makes it possible for us to show more columns.
        - Modify the AuthorAdmin(admin.ModelAdmin) class
		```
		# Define the admin class
		class AuthorAdmin(admin.ModelAdmin):
			# pass    # If pass is defined here the Admin site behaviour won't be changed
			list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

		# Register the admin class with the associated model
		admin.site.register(Author, AuthorAdmin)
		```
		- Another scenario - ManyToMany relationship depicted by a Books Genre
		```
		# Similarly:
		# Book
		# admin.site.register(Book)
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

		# Register the admin class with the associated model
		admin.site.register(Book, BookAdmin)
		```
	- Add List filters	-	done by <b>list_filter</b>  attribute
    	- Adds a sidebar in the Admin site, which allows you item filtering
		- In dependentapp/admin.py - (catalog/admin.py) - Again, modify the admin.ModelAdmin extending function.
			```
			@admin.register(BookInstance)
			class BookInstanceAdmin(admin.ModelAdmin):
				# pass
				list_filter = ('status', 'due_back')
				# Once you've got a lot of items in a list, it can be useful to be able to
				# filter which items are displayed.
				# This is done by listing fields in the list_filter attribute.
			```
	- Organize detail view layout:
    	- Def: Items are shown vertically in the sequence declared in the apps models.py
    	- Can change:
        	- order
        	- which fields are displayed
        	- whether sections are used to organise the info
        	- whether fields are displayed horizontally or vertically
        	- what widgets are used in the admin forms
		- A few examples:
    		- Which fields are displayed
        		- attribute <b>fields = ['first_name', 'last_name']</b>
        		- Modify appname/admin.py
					```
					# Define the admin class
					class AuthorAdmin(admin.ModelAdmin):
						# pass    # If pass is defined here the Admin site behaviour won't be changed
						# list_display -> which column names to show
						list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
						# fields -> column order of appearance (& layout - Fields in a tuple are displayed horizontally)
						fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


					# Register the admin class with the associated model
					admin.site.register(Author, AuthorAdmin)
					```
				- attribute <b>exclude</b>
    				- Declare a list of attributes which are not shown
    		- Sectioning the Detail View
        		- attribute <b>fieldsets</b>
        		- add "sections" to group related model information within the detail form.
          		- Modify appname/admin.py
					```
					@admin.register(BookInstance)
					class BookInstanceAdmin(admin.ModelAdmin):
						# pass
						list_filter = ('status', 'due_back')
						# Once you've got a lot of items in a list, it can be useful to be able to
						# filter which items are displayed.
						# This is done by listing fields in the list_filter attribute.
						#

						# Add "Sections" in detail view
						fieldsets = (
							(None, {
								'fields': ('book', 'imprint', 'id')
							}),
							('Availability', {
								'fields': ('status', 'due_back')
							}),
						)
					```
			- Inline editing of associated records
    			- can add associated records at the same time
    			- declare inlines of type TabularInline (horizontal layout) or StackedInline (vertical layout)
					```
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
					```

# Misc
- https://stackoverflow.com/a/9181710