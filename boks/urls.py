from django.urls import path
from .views import BookListByGenre, Review, BookListView

urlpatterns = [
    path("api/book/list/", BookListView.as_view(), name='BookListView'),
    path("api/book/<str:genre>/", BookListByGenre.as_view(), name='BookListByGenre'),
    path("api/review/add/", Review.as_view(), name='Review'),
    path("api/review/update/", Review.as_view(), name='UpdateReview'),
    path("api/review/delete/", Review.as_view(), name='DeleteReview'),
]
