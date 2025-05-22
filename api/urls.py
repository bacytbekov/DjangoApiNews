from django.urls import path,include

from api.views import WorkersAPIView, NewsAPIView, NewsDetailAPIView

urlpatterns = [
    path('workers/', WorkersAPIView.as_view()),
    path('login/', WorkersAPIView.as_view()),
    path('news/', NewsAPIView.as_view()),
    path('news/<int:pk>/', NewsDetailAPIView.as_view()),

]