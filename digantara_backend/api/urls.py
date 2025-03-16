from django.urls import path
from .views import BinarySearchAPIView, QuickSortAPIView, BFSAPIView, AlgorithmLogListAPIView

urlpatterns = [
    path('binary-search/', BinarySearchAPIView.as_view(), name='binary-search'),
    path('quick-sort/', QuickSortAPIView.as_view(), name='quick-sort'),
    path('bfs/', BFSAPIView.as_view(), name='bfs'),
    path('logs/', AlgorithmLogListAPIView.as_view(), name='logs'),  # Fetch all logs
]
