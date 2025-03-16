📌 DSAForge API - Binary Search, Quick Sort & BFS
This project provides API endpoints to execute and log algorithm calls for Binary Search, Quick Sort, and BFS (Breadth-First Search).
Language Used: Python

📋 Features
✔ API endpoints for executing algorithms
✔ Logs API calls (Algorithm name, Input, Output, Timestamp)
✔ Supports exporting logs in JSON and CSV formats
✔ Error handling for invalid inputs

🚀 Getting Started
Follow these steps to install, run, and use the API.

1️⃣ Prerequisites
Ensure you have the following installed:
✅ Python 3.x
✅ Django & Django REST Framework
✅ Git
✅ Postman or cURL (for testing API requests)

2️⃣ Installation Steps
Clone the repository
git clone https://github.com/Pooja262/DQuickSort-BFS-BinarySearch-API.git
cd DSAForge

Create a Virtual environment
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate  # On Windows

Install Dependencies
pip install -r requirements.txt

Apply Migrations
python manage.py migrate

Create a Superuser
python manage.py createsuperuser

Run the development server
python manage.py runserver
Now, your API is running at http://127.0.0.1:8000/ 🎯


🌐 API Endpoints
1️⃣ Run Algorithms
Algorithm	    Method	      Endpoint	                                        Sample Input JSON
Binary Search POST	      http://127.0.0.1:8000//api/binary-search/	        {"array": [1, 3, 5, 7], "target": 5}
Quick Sort    POST	      http://127.0.0.1:8000//api/quick-sort/	          {"array": [10, 3, 2, 8]}
BFS Search    POST	      http://127.0.0.1:8000//api/bfs/	                {"graph": {"A": ["B", "C"], "B": ["D"]},"start": "A"}



2️⃣ View Algorithm Logs
Action	      Method	    Endpoint	                    Format
View Logs	      GET	       /api/logs/	                  JSON
Export Logs	    GET	      /api/logs/export/?format=csv	CSV file


curl -X GET http://127.0.0.1:8000/api/logs/export/?format=csv

This will download logs.csv containing:

Algorithm Name, Input Data, Output Data, Timestamp

🛠 Future Enhancements
🔹 Add more algorithms (Dijkstra, Merge Sort, etc.)
🔹 Implement authentication for API access
🔹 Store logs in a database instead of local storage
