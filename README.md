# django_collection
Django Tutorials Notes Collection & Playground
by: @ren-zxcyq & @Ix76y

# Useful Commands and Links

## Links

### General References
[Template Stuff](https://docs.djangoproject.com/en/3.1/ref/templates/language/)
[sessions](https://docs.djangoproject.com/en/3.1/topics/http/sessions/)
[e-mail Password Reset](https://docs.djangoproject.com/en/3.1/topics/email/)
[User auth](https://docs.djangoproject.com/en/3.1/topics/auth/)
[Using the User auth system](https://docs.djangoproject.com/en/3.1/topics/auth/default/)
[Decorating Class-based views](https://docs.djangoproject.com/en/3.1/topics/class-based-views/intro/#decorating-class-based-views)


### Tutorials

[Official Django Tutorial](https://docs.djangoproject.com/en/3.1/intro/tutorial01/)

[Mozilla Developer - Django Introductions](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Introduction)


### Books

- O'Reilly - Leightweight Django

## Commands
### Run the server (Development ONLY)
By default it will serve the site to your local computer (http://127.0.0.1:8000/), but you can also specify other computers on your network to serve to.

- `python3 manage.py runserver`

### Update Models
Run the following commands to define tables or change the db tables whenever you change something in the models.
- `python3 manage.py makemigrations`
- `python3 manage.py migrate`

Optionally, we can specify app name, in order to migrate only the given apps Models etc.
- `python3 manage.py makemigrations catalog`

### Create a superuser
- In order to log on to the admin site, we need an acc with <i>Staff</i> status enabled.
- ?Can further define permissions.
- Creation Process:
  ```
  python3 manage.py createsuperuser
  # Prompts for: Username && email && pass
  # And run server again:
  python3 manage.py runserver
  ```
