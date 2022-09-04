from django.urls import path,include
from django.contrib.auth.views import LogoutView
from . import views

app_name = "books"

urlpatterns = [
    path("book/<int:pk>/renew/", views.renew_book, name='renew-book'),
    path("test/", views.test,name='test'),
    path("suggestions/", views.SuggestionFunc, name='Suggestionfunc'),
    path("book/add_wishlist/<int:pk>/", views.add_wishlist, name='add-wishlist'),
    path("", views.home,name='homepage'),
    path("guidelines/", views.guidelines,name='guidelines'),
    path('login/', views.LoginView.as_view(),name="login"),
    path('logout/', LogoutView.as_view(),name = 'logout'),
    path("book/available/", views.avail_books,name='avail_books'),
    path("book/wishlist/", views.see_wishlist,name='see_wishlist'),

    path("book/article/", views.article_overview,name='a'),
    path("books/search_result/",views.searched_fun,name='searchresult'),
    path("books/remove_wishlist/<int:pk>",views.remove_from_wishlist,name='remove-book-wl'),

    path("book/search/",views.search_fun,name='searchfun'),
    path("book/contact/",views.contact)


]