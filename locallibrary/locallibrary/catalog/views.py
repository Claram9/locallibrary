from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre, Language
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required


# Create your views here.
def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    num_genres=Genre.objects.all().count()
    # Available books (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # The 'all()' is implied by default.
    # Books with the word 'prueba'
    books_search=Book.objects.filter(title__icontains='prueba').count()

    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors,
                'num_genres':num_genres,'books_search':books_search,'num_visits':num_visits},
    )


# @login_required
class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    # context_object_name = 'my_book_list'   # your own name for the list as a template variable
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location

    # def get_queryset(self):
    #    return Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war

    # def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
    #    context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
    #    context['some_data'] = 'This is just some data'
    #    return context


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


#@permission_required('catalog.can_mark_returned')
#@permission_required('catalog.can_edit')
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')



class LoanedBooksLibrariansListView(PermissionRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
