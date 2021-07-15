from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("activelist", views.activelist, name="activelist"),
    path("category/<str:catag>", views.category, name="category"),
    path("createauction", views.createauction, name="createauction"),
    path("viewlist/<int:listing_id>", views.viewlist, name="viewlist"), 
    path("dltwatchlist/<int:listing_id>", views.dltwatchlist, name="dltwatchlist"), 
    path("addwatchlist/<int:listing_id>", views.addwatchlist, name="addwatchlist"), 
    path("viewwatchlist", views.viewwatchlist, name="viewwatchlist"), 
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("closeauction/<int:listing_id>", views.closeauction, name="closeauction") 

]
