# Notes
This folder contains all notes we kept when walking through the Mozilla Django tutorial, found at: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Introduction

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

- In general filtering happens like this:
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
# External Page
  - Home Page
    - URL Mapping
      - Our main application/urls.py declares that when requests to ip/catalog are received
      - application/urls.py contains
		```
		from django.contrib import admin
		from django.urls import path

		urlpatterns = [
			path('admin/', admin.site.urls),
		]

		# Use include() to add paths from the catalog application
		from django.urls import include
		urlpatterns += [
				path('catalog/', include('catalog.urls')),
		]
		# Note: Whenever Django encounters the import function
		# django.urls.include()
		# it splits the URL string at the designated end character
		# and sends the remaining substring
		# to the included URLconf module for further processing.

		# Add URL maps to redirect the base URL to our application
		from django.views.generic import RedirectView
		urlpatterns += [
				path('', RedirectView.as_view(url='catalog/', permanent=True)),
		]

		# Use static() to add url mapping to serve static files during development (only)
		from django.conf import settings
		from django.conf.urls.static import static

		urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
		```
      - Whenever Django encounters <b>django.urls.include()</b>
        - Django splits the URL string at the designated end character and
        - sends the remaining substring to the included URLconf module for further processing.
      - So, we defined a placeholder <b>/catalog/urls.py</b> file
        - Contents:
			```
			from django.urls import path
			from . import views

			urlpatterns = [
				path('', views.index, name='index')
			]
			# - '' -> a URL pattern which is an empty string
			# - A view function will be called when the pattern is detected:
			#	<b>views.index</b> -> <b>index()</b> in <b>views.py</b>
			# - 'name' identifier for this particular URL mapping
			#	we can use the name to "reverse" the mapper
			#	i.e. to dynamically create a URL that points to the resource that
			#			the mapper is designed to handle.
			#	for example:
			#		we can use the name param
			#		to link to our home page from any other page template
			#			<a href="{% url 'inded' %}">Home</a>
			```
	- View (function-based)
    	- A view is a function that:
        	- processes an HTTP request
        	- fetches the required data from the database
        	- renders the data in an HTML page using an HTML template
        	- returns the generated HTML in an HTTP response
      	- In our example, our Home page
        	- fetches info about the number of Book, BookInstance, available BookInstance and Author records
        	- and passes that info to a template for display
      	- catalog/views.py
        	- <b>render()</b>	-	to generate an HTML file using a template and data:
				```
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

					context = {
						'num_books': num_books,
						'num_instances': num_instances,
						'num_instances_available': num_instances_available,
						'num_authors': num_authors,
					}

					# Render the HTML template index.html with the data in the context variable
					return render(request, 'index.html', context=context)
					# render() accepts:
					#   - original request  -   HttpRequest
					#   - an HTML template  -   with PLACEHOLDERS for the data
					#   - context variable  -   which is a Python dict, containing the data to insert into the PLACEHOLDERS
				```
	- Template
    	- A text file that defines the structure of a file (such as an HTML page).
        	- Uses PLACEHOLDERS to represent actual content.
      	- Django automatically looks for templates in a directory named <b>'templates'</b> in your application
        	- for example when: render(request, 'index.html', context=context)
        	- render will expect to find index.html in /locallibrary/catalog/templates/
        	- if the file is not found:	<b>TemplateDoesNotExist</b> at /catalog/
      	- Based on your project's settings file, Django will look for templates in a number of places, searching in your installed applications by default. More: https://docs.djangoproject.com/en/2.1/topics/templates/
      	- Extending Templates
        	- Puzzle of templates
          	- Sample:
				```
				<!DOCTYPE html>
				<html lang="en">
				<head>s
				{% block title %}<title>Local Library</title>{% endblock %}
				</head>
				<body>
				{% block sidebar %}<!-- insert default navigation text for every page -->{% endblock %}
				{% block content %}<!-- default content text (typically empty) -->{% endblock %}
				</body>
				</html>
				```
			- Notice: <b>Common HTML</b> with sections for title, sidebar or content marked with
    			- <b>block</b>
    			- <b>endblock</b>
			- These are called <b>TEMPLATE TAGS</b>
  			- TEMPLATE TAGS are <b>functions</b> that you can use in a template to:
    			- loop through lists
    			- perform conditional operations based on the val of a var
  			- The syntax also allows:
    			- referencing values passed into the <b>template</b> from the <b>view</b>
    			- using template filters to format variables (for example, to convert a string to lower case).
  			- <b>extends</b> template tag.
    			- When defining a template:
                    1) specify the base template using the extends template tag
                    2) Declare which sections from the template we want to replace (if any), using block/endblock sections
				- In the below example, we override the content block. The generated HTML will include the code and structure defined in the base template, including default content defined in the title block, but the new content block in place of the default one.
					```
					{% extends "base_generic.html" %}

					{% block content %}
						<h1>Local Library Home</h1>
						<p>Welcome to LocalLibrary, a website developed by <em>Mozilla Developer Network</em>!</p>
					{% endblock %}
					```
		- The local Library Base Template
    		- In our library example create:
        		- base_generic.html in /locallibrary/catalog/templates/
        		- styles.css file in /locallibrary/catalog/static/css/
  		- The index template
      		- Create:
        		- index.html in /locallibrary/catalog/templates/	which extends base_generic.html & replaces the content block
        		- index.html declares variables
        		- template:
            		- variables	-	enclosed in double braces ({{ num_books }})
            		- tags (functions)	-	enclosed in single braces with percentage signs ({% extends "base_generic.html" %}).
				- variables are named with the keys we pass in the context dict in function render()
		- Referencing static files in templates
    		- Specify the location in templates relative to the <b>STATIC_URL</b> global setting. (def: /static/)
    		- Use <b>static</b> template tag and specify the relative URL
				```
				{% load static %}
				<link rel="stylesheet" href="{% static 'css/styles.css' %}">
				```
			- or adding an image
				```
				{% load static %}
				<img src="{% static 'catalog/images/local_library_model_uml.png' %}" alt="UML diagram" style="width:555px;height:540px;">
				```
			- Note on the docs: The samples above specify where the files are located, but Django does not serve them by default. We configured the development web server to serve files by modifying the global URL mapper (/locallibrary/locallibrary/urls.py) when we created the website skeleton, but still need to enable file serving in production. We'll look at this later.
		- Linking to URLs
    		- <b>url</b> template tag
				```
				<li><a href="{% url 'index' %}">Home</a></li>
				```
			- accepts the name of a path() function called in your <b>urls.py</b>
    			- The above assumes at least the following content in catalog/urls.py:
					```
					from django.urls import path
					from . import views

					urlpatterns = [
						path('', views.index, name='index')
					]
					```
			- returns a URL that you can use to link to the resource
    	- Configuring where to find the templates
        	- Need to point Django to look for the templates folder.
        	- Add the templats dir to the TEMPLATES object.
        	- edit settings.py	


# Generic list and detail views
- URL mapping
  - add another path in /catalog/urls.py
	```
	path('books/', views.BookListView.as_view(), name='books')
	```
  - views.BookListView.as_view() has a different format than views.index for example.
  - <b>class-based view</b>
    - its own class
    - inheriting from an existing generic view function that already does most of what we want this view function to do
  - as_view()
    - does all the work of creating an instance of the class
    - making sure the right handler methods are called for incoming HTTP requests
- View (class-based)
  - Could easily just build it directly like a normal view (e.g. the index view)
    - we would query the db
    - then call render()
    - pass in the list to a template
  - Instead:
    - class-based generic list view (ListView)
    - ListView:
      - a class that inherits from an existing view.
      - more robust list view with less code
  - catalog/views.py


# Sessions
Django uses a cookie containing a special session id to identify each browser and its associated session with the site. The actual session data is stored in the site database by default (this is more secure than storing the data in a cookie, where they are more vulnerable to malicious users). You can configure Django to store the session data in other places (cache, files, "secure" cookies), but the default location is a good and relatively secure option.

## Enabling sessions
Change your project/settings.py	(in our case:	locallibrary/settings.py)
```
INSTALLED_APPS = [
	...
	'django.contrib.session',
	...
MIDDLENAME = [
	...
	'django.contrib.sessions.middleware.SessionMiddleware',
	...
```

## Using sessions
- Can access session data via the request.session attribute, where request is the request object (an HttpRequest) passed into the view.
- Again: It represents the specific connection to the current user (the current browser)
- <b>request.session</b>	-	<b>dictionary-like</b> object
	- can sort/"check if key is present"/set/delete/"loop through data"
	- HOWEVER -> std "dictionary" API	(most of the time)	-> get/set values
- Example:
	```
	# Get a session value by its key (e.g. 'my_car'), raising a <b>KeyError</b> if the key is not present
	my_car = request.session['my_car']

	# Get a session value, setting a default if it is not present ('mini')
	my_car = request.session.get('my_car', 'mini')

	# Set a session value
	request.session['my_car'] = 'mini'

	# Delete a session value
	del request.session['my_car']
	```
- Furthermore:
	- Methods to manage the associated session cookie
	- Methods to test that cookies are supported in the client browser.
	- Set and check cookie expiry dates.
	- Clear expired sessions from the data store.
	- More at:	https://docs.djangoproject.com/en/2.1/topics/http/sessions/

## Saving session data
By def	-	Django only saves to the session db & sends the session cookie to the client when the session has been modified (assigned or deleted). If you're updating its session key as shown in the previous section, the update is done automatically.
	
```
# This is detected as an update to the session, so session data is saved.
request.session['my_car'] = 'mini'
```

<b>However</b>, if you modify data <b><i>within</i> session data</b>, Django will NOT recognise the change by default. You need to <b>explicitly mark the session as having been modified</b>.

```
# Session object not directly modified, only data WITHIN the session.
# Session changes NOT saved!
request.session['my_car']['wheels'] = 'alloy'

# Set session as modified to FORCE data updates/cookie to be saved.
request.session.modified = True
```

- Alternatively, add SESSION_SAVE_EVERY_REQUEST = True in project/settings.py (here: locallibrary/settings.py)


# User Authentication & Permissions
- many 3d party modules solving common problems exist. (throttling of login attempts, auth against 3d parties (e.g. OAuth))
- The "basic authentication" API is enabled when we perform ```django-admin startproject```
- The DB tables for users and model permissions are created during the first ```python manage.py migrate```.
- 
```
INSTALLED_APPS = [
	...
	'django.contrib.auth', # Core auth framework and its default models.
	'django.contrib.contenttypes', # Django content type system (allows perms to be associated with models)
	...

MIDDLEWARE = [
	...
	'django.contrib.sessions.middleware.SessionMiddleware', # Manages sessions accross requests
	...
	'django.contrib.auth.middleware.AuthenticationMiddleware', # Associates users with requests using sessions.
	...
```
## Creating users & groups
- ```python manage.py createsuperuser``` - already exists WITH all permissions
- Admin Panel: ```Groups``` & ```Users``` tables	-	use this to add extra users 
	- used the admin panel to add 2 groups:
		Groups
		1) Librarians
		2) Library members
		Users
		1) tommy	thisisstupid
		2) tammy	thisisstupid
~CONTINUE at: Setting up your authenticated views

# Setting up our own authentication views
## Project URLs
Add the following to our main application (in our case: locallibrary/urls.py)
```
# Add authentication URLs (for login, logout, password management)
urlpatterns += [
        path('accounts/', include('django.contrib.auth.urls')),
]
```
	- Note: its fine even if we paste this at the bottom.

If we browse to localhost:8000/accounts, we get a 404, BUT:
```
Using the URLconf defined in locallibrary.urls, Django tried these URL patterns, in this order:

    admin/
    catalog/
    ^static/(?P<path>.*)$
    accounts/ login/ [name='login']
    accounts/ logout/ [name='logout']
    accounts/ password_change/ [name='password_change']
    accounts/ password_change/done/ [name='password_change_done']
    accounts/ password_reset/ [name='password_reset']
    accounts/ password_reset/done/ [name='password_reset_done']
    accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
    accounts/ reset/done/ [name='password_reset_complete']

The current path, accounts/, didn't match any of these.
```
As we can see, the default implementation adds URLS to perform several actions.

Now, if we browse to localhost:8000/accounts/login
we get the following error:
```
TemplateDoesNotExist at /accounts/login/
registration/login.html
```
This effectively means that we we should now add a new templates directory:
```

So, let's create the {project_root}/templates/registration folders
Again, our projects structure is like this:
```
locallibrary
catalog
templates/registration
```

Create: 
```
mkdir -p templates/registration
```

Add the new templates directory to the list of directories to check:
In locallibrary/settings.py
```
TEMPLATES = [
    {
        ...
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        ...
```

Create templates/registration/login.html and add the following:
```
{% extends "base_generic.html" %}

{% block content %}

        {% if form.errors %}
                <p>Your username and password didn't match. Please try again.</p>
        {% endif %}

        {% if next %}
                {% if user.is_authenticated %}
                        <p> Your account doesn't have access to this page. To proceed, please login with an account that has access.</p>
                {% else %}
                        <p> Please login to see this page.</p>
                {% endif %}
        {% endif %}

        <form method="POST" action="{% url 'login' %}">
                {% csrf_token %}
                <table>
                        <tr>
                                <td>{{ form.username.label_tag }}</td>
                                <td>{{ form.username }}</td>
                        </tr>
                        <tr>
                                <td>{{ form.password.label_tag }}</td>
                                <td>{{ form.password }}</td>
                        </tr>
                </table>
                <input type="submit" value="login" />
                <input type="hidden" name="next" value="{{ next }}" />
        </form>

        {# Assumes you setup the password_reset view in your URLconf #}
        <p><a href="{% url 'password_reset' %}">Lost password</a></p>

{% endblock %}
``` 

Now visiting localhost:8000/accounts/login will show the login page.
```curl -X GET "http://localhost:8000/accounts/login/"```

<b>Submitting valid creds redirects</b> us to:	```localhost:8000/accounts/profile```

By default, Django expects that upon logging in the user should be redirected to a profile page.
To change this, (and redirect users that logged in to /) open locallibrary/settings.py and add:
```
# Redirect to home URL after login (Default redirects to /account/profile/)
Add the following to mainapp/settings.py (locallibrary/settings.py)

```LOGIN_REDIRECT_URL = '/'```

## Logout Template
logout url:	localhost:8000/accounts/logout/

By default, when a user visits that URL, they are logged out allright; however, they are redirected to the <b>Admin logout page</b>.
The Admin logout page <b>should</b> only available to users with the <b>is_staff</b> permission.
<b>Note:</b>
	- Documentation here states: "That's not what you want, if only because the login link on that page takes you to the Admin login screen (and that is only available to users who have the is_staff permission)."
	- BUT users without that permission set could also access that during my last test.
	- regardless, it is good practice to keep those separated.


Let's create: templates/registration/logged_out.html
```
{% extends "base_generic.html" %}

{% block content %}
	<p>Logged out!</p>
	<a href="{% url 'login' %}>Click here to login again.</a>
{% endblock %}
```

## Password Reset Templates
Add the following
```
vi templates/registration/password_reset_form.html
vi templates/registration/password_reset_done.html
vi templates/registration/password_reset_email.html
vi templates/registration/password_reset_confirm.html
vi templates/registration/password_reset_complete.html
```

- Password reset form
	Create templates/registration/password_reset_form.html
	```
	{% extends "base_generic.html" %}
	
	{% block content %}
		<form action="" method="post">
		{% csrf_token %}
		{% if form.email.errors %}
			{{ form.email.errors }}
		{% endif %}
			<p>{{ form.email }}</p>
			<input type="submit" class="btn btn-default btn-lg" value="Reset password">
		</form>
	{% endblock %}
	```

- Password reset done
	```
	{% extends "base_generic.html" %}

	{% block content %}
        	<p>We've emailed you instructions for setting your password. If they haven't arrived in a few minutes, check your spam folder.</p>
	{% endblock %}
	```

- Password reset email
	```
	Someone asked for password reset for email {{ email }}. Follow the link below:
	{{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}
	```

- Password reset confirm
	```
	{% extends "base_generic.html" %}
	
	{% block content %}
	        {% if validlink %}
	                <p>Please enter (and confirm) your new password.</p>
	                <form action="" method="post">
	                {% csrf_token %}
	                        <table>
	                                <tr>
	                                        <td>{{ form.new_password1.errors }}
	                                                <label for="id_new_password1">New password:</label></td>
	                                        <td>{{ form.new_password1 }}</td>
	                                </tr>
	                                <tr>
	                                        <td>{{ form.new_password2.errors }}
	                                                <label for="id_new_password2">Confirm password:</label></td>
	                                        <td>{{ form.new_password2 }}</td>
	                                </tr>
	                                <tr>
	                                        <td></td>
	                                        <td><input type="submit" value="Change my password" /></td>
	                                </tr>
	                        </table>
	                </form>
	        {% else %}
	                <h1>Password reset failed</h1>
	                <p>The password reset link was invalid, possibly because it has already been used. Plase request a new password reset.</p>
	        {% endif %}
	{% endblock %}
	```

- Password reset complete
	```
	{% extends "base_generic.html" %}
	
	{% block content %}
	        <h1>The password has been changed!</h1>
	        <p><a href="{% url 'login' %}">log in again?</a></p>
	{% endblock %}
	```

## Password Reset Process Overview

- By default, Django will <b>ONLY send</b> an email <b>if the provided e-mail already exists in the db</b>
- Furthermore, currently e-mails are not forwarded from the app.
- BUT, there is a way for us to debug the app and verify that everything is working normally. 

Add the following to mainapp/settings.py (locallibrary/settings.py):

```EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'```

The process, as seen from the running servers log:
```
[07/Oct/2020 17:08:54] "GET /accounts/login/ HTTP/1.1" 200 1665
[07/Oct/2020 17:08:59] "GET /accounts/password_reset/ HTTP/1.1" 200 1246
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Password reset on localhost:8000
From: webmaster@localhost
To: tommy@test.ing
Date: Wed, 07 Oct 2020 16:09:07 -0000
Message-ID: <160208694743.4579.11471690196614365768@shiroe>

Someone asked for password reset for email tommy@test.ing. Follow the link below:
http://localhost:8000/accounts/reset/Mg/abdub7-47eabebc3cbf905e174cfec8454a0fb7/

-------------------------------------------------------------------------------
[07/Oct/2020 17:09:07] "POST /accounts/password_reset/ HTTP/1.1" 302 0
[07/Oct/2020 17:09:07] "GET /accounts/password_reset/done/ HTTP/1.1" 200 1031
[07/Oct/2020 17:09:12] "GET /accounts/reset/Mg/abdub7-47eabebc3cbf905e174cfec8454a0fb7/ HTTP/1.1" 302 0
[07/Oct/2020 17:09:12] "GET /accounts/reset/Mg/set-password/ HTTP/1.1" 200 1671
[07/Oct/2020 17:09:22] "POST /accounts/reset/Mg/set-password/ HTTP/1.1" 302 0
[07/Oct/2020 17:09:22] "GET /accounts/reset/done/ HTTP/1.1" 200 993
[07/Oct/2020 17:09:24] "GET /accounts/login/ HTTP/1.1" 200 1665
```
We can actually change passwords this way!

## Example - listing the current user's books
@TODO

# Misc
- https://stackoverflow.com/a/9181710
