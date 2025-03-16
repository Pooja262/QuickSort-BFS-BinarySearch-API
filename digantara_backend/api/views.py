from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AlgorithmLog
from .serializers import AlgorithmLogSerializer
import json
from collections import deque
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

# Utility function to log API calls
def log_algorithm_call(algorithm_name, input_data, output_data):
    log_entry = AlgorithmLog.objects.create(
        algorithm_name=algorithm_name,
        input_data=input_data,
        output_data=output_data
    )
    return log_entry

# Binary Search API
class BinarySearchAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            arr = sorted(data.get("array", []))  # Ensure the array is sorted
            target = data.get("target")

            if not isinstance(arr, list) or target is None:
                return Response({"error": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)

            # Binary search implementation
            left, right = 0, len(arr) - 1
            while left <= right:
                mid = (left + right) // 2
                if arr[mid] == target:
                    result = mid
                    break
                elif arr[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1
            else:
                result = -1  # Not found

            log_algorithm_call("Binary Search", data, {"index": result})
            return Response({"index": result}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Quick Sort API
class QuickSortAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            arr = data.get("array", [])

            if not isinstance(arr, list):
                return Response({"error": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)

            # Quick Sort implementation
            def quick_sort(arr):
                if len(arr) <= 1:
                    return arr
                pivot = arr[len(arr) // 2]
                left = [x for x in arr if x < pivot]
                middle = [x for x in arr if x == pivot]
                right = [x for x in arr if x > pivot]
                return quick_sort(left) + middle + quick_sort(right)

            sorted_array = quick_sort(arr)

            log_algorithm_call("Quick Sort", data, {"sorted_array": sorted_array})
            return Response({"sorted_array": sorted_array}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Breadth-First Search API
class BFSAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            graph = data.get("graph", {})
            start_node = data.get("start_node")

            if not isinstance(graph, dict) or start_node is None:
                return Response({"error": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)

            # BFS Implementation
            visited = []
            queue = deque([start_node])

            while queue:
                node = queue.popleft()
                if node not in visited:
                    visited.append(node)
                    queue.extend(graph.get(node, []))

            log_algorithm_call("Breadth First Search", data, {"traversal_order": visited})
            return Response({"traversal_order": visited}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)





# Custom pagination class (10 logs per page)
class LogPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

# Log Retrieval API with filtering & pagination
class AlgorithmLogListAPIView(ListAPIView):
    queryset = AlgorithmLog.objects.all().order_by("-timestamp")  # Latest logs first
    serializer_class = AlgorithmLogSerializer
    pagination_class = LogPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["algorithm_name"]  # Allows filtering by algorithm name
    search_fields = ["algorithm_name"]