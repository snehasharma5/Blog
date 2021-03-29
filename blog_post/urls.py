from django.urls import path
from . import views
from .views import HomeView, ArticleDetailView, AddPostView, UpdatePostView, DeletePostView, AddCategoryView, \
    category_view, category_list_view, like_view, AddCommentView, search_result


urlpatterns = [
    path('', HomeView.as_view(), name='Home'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('add_post/', AddPostView.as_view(), name='add-post'),
    path('add_category/', AddCategoryView.as_view(), name='add-category'),
    path('article/edit/<int:pk>', UpdatePostView.as_view(), name='update-post'),
    path('article/<int:pk>/remove', DeletePostView.as_view(), name='delete-post'),
    path('category/<str:cats>/', category_view, name='category'),
    path('category-list/', category_list_view, name='category-list'),
    path('like/<int:pk>/', like_view, name='like-post'),
    path('article/<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('search/', search_result, name='search_result'),

]
