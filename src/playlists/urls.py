from django.urls import path
from .views import FeaturedPlaylistListView, MovieListView,TvShowListView


urlpatterns=[
    path('movies/',MovieListView.as_view()),
    path('shows/',TvShowListView.as_view()),
    path('featured/',FeaturedPlaylistListView.as_view()),


]