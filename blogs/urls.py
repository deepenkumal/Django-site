from django.urls import path
from . import views

urlpatterns = [
    path("",views.IndexView.as_view(), name="index"),
    path("posts/",views.posts, name="posts"),
    path('posts/read-later/',views.ReadLaterViews.as_view(), name='read_later'),
    path("posts/<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/tag/<str:tag>/", views.tag_page, name="tag_page"),

]