# django_experiment
Django Tut Playground @Ix76

# Notes

## Run the server (Development ONLY)
By default it will serve the site to your local computer (http://127.0.0.1:8000/), but you can also specify other computers on your network to serve to

`python3 manage.py runserver`

## Update Models
Run the following commands to define tables or change the db tables whenever you change something in the models.
- python3 manage.py makemigrations
- python3 manage.py migrate

## Optional can specify app name, in order to migrate only the given apps Models etc.
- python3 manage.py makemigrations catalog

## Models - Important:
- Models define the structure of stored data.
- including field types & possibly their max size, def vals, selection list options, help text for documentation, label text for forms etc.
- Models are implemented as subclasses of:	django.db.models.Model

- `from django.db import models

class MyModelName(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    my_field_name = models.CharField(max_length=20, help_text='Enter field documentation')
    ...

    # Metadata
    class Meta: 
        ordering = ['-my_field_name']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.my_field_name`

- When used in a form, my_field_name would be My field name

### Common Field Arguments
- help_text	-	Label for HTML forms
- verbose_name	-	name for the field, used in Field Labels
- default	-	Default Value
- null		-	If True, store blank vals as NULL. (CharField will be stored as an empty string) Def: False
- blank		-	If True, is allowed to be blank in forms. Def: False, meaning you will be forced to provide a val. (Often used with null=True)
- choices	-	A group of choices for this field. Default form widget will be a select box with these choices.
- primary_key	-	If True, sets the current field as the primary key for the model. If no field is specified, Django will add a field automatically

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
