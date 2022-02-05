from django.urls import path
from .views import AddComment, CommentDelete

urlpatterns = [
    path('course/<int:pk>/add_comment', AddComment.as_view(), name='add_comment'),
    path('comment/<int:pk>/delete/', CommentDelete.as_view(), name='comment_delete'),
]