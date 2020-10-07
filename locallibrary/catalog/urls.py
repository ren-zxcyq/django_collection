from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),

    # If you need more refined filtering (for example, to filter only strings
    # that have a certain number of characters) then you can use the re_path() method.
    # This method is used just like path() except that it allows you to specify a
    # pattern using a Regular expression. For example, the previous path could have been
    # written as shown below:
    # re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),

    # Passing additional options in your URL maps
    # One feature that we haven't used here, but which you may find valuable, is that you can declare and pass additional options to the view. The options are declared as a dictionary that you pass as the third un-named argument to the path() function. This approach can be useful if you want to use the same view for multiple resources, and pass data to configure its behaviour in each case (below we supply a different template in each case).
    # path('url/', views.my_reused_view, {'my_template_name': 'some_path'}, name='aurl'),
    # path('anotherurl/', views.my_reused_view, {'my_template_name': 'another_path'}, name='anotherurl'),
    # Note: Both extra options and named captured patterns are passed to the view as named arguments. If you use the same name for both a captured pattern and an extra option then only the captured pattern value will be sent to the view (the value specified in the additional option will be dropped). 

    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]