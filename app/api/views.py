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
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
import csv


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
            arr = data.get("array")
            target = data.get("target")

            if not isinstance(arr, list) or not all(isinstance(i, (int, float)) for i in arr):
                return Response({"error": "Invalid input. 'array' must be a list of numbers."}, status=status.HTTP_400_BAD_REQUEST)

            if not isinstance(target, (int, float)):
                return Response({"error": "Invalid target. Must be a number."}, status=status.HTTP_400_BAD_REQUEST)

            # Ensure the array is sorted
            arr.sort()

            # Perform binary search
            result = self.binary_search(arr, target)

            # Log the request and response
            AlgorithmLog.objects.create(algorithm_name="Binary Search", input_data={"array": arr, "target": target}, output_data=result)

            return Response({"result": result}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def binary_search(self, arr, target):
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                return mid  # Return index if found
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1  # Not found
    

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




class ExportLogsAPIView(APIView):
    def get(self, request, format=None):
        try:
            logs = AlgorithmLog.objects.all().order_by("-timestamp")

            if not logs.exists():
                return Response({"error": "No logs found."}, status=status.HTTP_404_NOT_FOUND)

            export_format = request.GET.get("format", "json").lower()

            if export_format == "csv":
                response = HttpResponse(content_type="text/csv")
                response["Content-Disposition"] = 'attachment; filename="logs.csv"'
                writer = csv.writer(response)
                writer.writerow(["Algorithm Name", "Input Data", "Output Data", "Timestamp"])

                for log in logs:
                    writer.writerow([log.algorithm_name, json.dumps(log.input_data), json.dumps(log.output_data), log.timestamp])

                return response

            elif export_format == "json":
                log_data = [
                    {
                        "algorithm_name": log.algorithm_name,
                        "input_data": log.input_data,
                        "output_data": log.output_data,
                        "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    for log in logs
                ]
                return JsonResponse(log_data, safe=False)

            else:
                return Response({"error": "Invalid format. Use 'json' or 'csv'."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)