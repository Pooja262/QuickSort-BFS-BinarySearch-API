from django.urls import path
from .views import BinarySearchAPIView, QuickSortAPIView, BFSAPIView, AlgorithmLogListAPIView, AlgorithmLogListAPIView, ExportLogsAPIView


urlpatterns = [
    path('binary-search/', BinarySearchAPIView.as_view(), name='binary-search'),
    path('quick-sort/', QuickSortAPIView.as_view(), name='quick-sort'),
    path('bfs/', BFSAPIView.as_view(), name='bfs'),
    path("logs/export/", ExportLogsAPIView.as_view(), name="export-logs"), # Fetch all logs
]

