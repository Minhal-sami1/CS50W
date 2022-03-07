from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add/", views.new_product, name = "add"),
    path("product/<int:product_id>", views.listing_view, name="listing"),
    path("product/<int:product_id>/<str:type>", views.change_listing, name="change_listing"),
    path("message/<str:type>/<str:message>", views.message, name = "message"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:type>", views.categories, name="category"),
    path("yourlisting/", views.your_listing, name="your_listing"),
    path("placed_bid", views.placed_bid, name = "placed_bid")
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
