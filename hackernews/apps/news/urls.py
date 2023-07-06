from django.urls import path

from .views import FetchHackerNewsView, HackernewsDetails, HackernewsListView

urlpatterns = [
    path('list/', HackernewsListView.as_view(), name='news-list'),
    path('list-<str:item_type>/', HackernewsListView.as_view(), name='news-list'),
    path('news-detail/<int:pk>/', HackernewsDetails.as_view(), name='news-detail'),
     path('fetch/', FetchHackerNewsView.as_view(), name='fetch_hacker_news'),
    

]


