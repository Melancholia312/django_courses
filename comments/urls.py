from django.urls import path
from .views import AddComment, CommentDelete, LikeComment

urlpatterns = [
    path('course/<int:pk>/add_comment', AddComment.as_view(), name='add_comment'),
    path('comment/<int:pk>/delete/', CommentDelete.as_view(), name='comment_delete'),
    path('comment/<int:pk>/like/', LikeComment.as_view(), name='like_comment')
]