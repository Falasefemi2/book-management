<!-- @format -->

# 📚 Book Management System (FastAPI + SQLite)

This is a **Book Management System API** built using **FastAPI** and **SQLite**. It allows users to **add, retrieve, update, and delete books** using RESTful API endpoints.

---

## 🚀 Features

- Add a new book
- Retrieve all books
- Get details of a specific book
- Update book details (Full or Partial)
- Delete a book
- Uses **FastAPI** for the API framework
- Stores data in an **SQLite database**

---

## 🛠 Installation

### **1️⃣ Clone the Repository**

```sh
git clone https://github.com/Falasefemi2/book-management.git
cd book-management
```

### **2️⃣ Create a Virtual Environment**

```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**

```sh
pip install fastapi uvicorn sqlalchemy sqlite3
```

---

## 📌 Running the API

Start the FastAPI server with:

```sh
uvicorn main:app --reload
```

The API will be available at: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

Access the **interactive Swagger UI** at:
**[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 🔥 API Endpoints

### **1️⃣ Add a New Book**

📌 **Endpoint:** `POST /books`

#### **Request Body:**

```json
{
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "year": 2008
}
```

#### **Response:**

```json
{
  "message": "Book added successfully",
  "book": {
    "id": 1,
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "year": 2008
  }
}
```

---

### **2️⃣ Retrieve All Books**

📌 **Endpoint:** `GET /books`

#### **Response:**

```json
[
  {
    "id": 1,
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "year": 2008
  }
]
```

---

### **3️⃣ Retrieve a Book by ID**

📌 **Endpoint:** `GET /books/{book_id}`

#### **Example Request:** `GET /books/1`

#### **Response:**

```json
{
  "id": 1,
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "year": 2008
}
```

---

### **4️⃣ Update a Book (Full Update)**

📌 **Endpoint:** `PUT /books/{book_id}`

#### **Request Body:**

```json
{
  "title": "The Clean Coder",
  "author": "Robert C. Martin",
  "year": 2011
}
```

#### **Response:**

```json
{
  "message": "Book updated successfully",
  "book": {
    "id": 1,
    "title": "The Clean Coder",
    "author": "Robert C. Martin",
    "year": 2011
  }
}
```

---

### **5️⃣ Update a Book (Partial Update)**

📌 **Endpoint:** `PATCH /books/{book_id}`

#### **Request Body:**

```json
{
  "title": "Refactoring"
}
```

#### **Response:**

```json
{
  "message": "Book updated successfully",
  "book": {
    "id": 1,
    "title": "Refactoring",
    "author": "Robert C. Martin",
    "year": 2011
  }
}
```

---

### **6️⃣ Delete a Book**

📌 **Endpoint:** `DELETE /books/{book_id}`

#### **Response:**

```json
{
  "message": "Book deleted successfully"
}
```

---

## 📂 Project Structure

```
book-management-api/
│── main.py          # Main FastAPI application
│── database.py      # Database connection & model
│── README.md        # Project documentation
│── requirements.txt # Dependencies (optional)
```

---

## 📌 Next Steps

- Implement **search and filtering** for books
- Add **user authentication** for secure access
- Deploy the API to a cloud server (e.g., **Render, Railway, or AWS**)

🚀 **Happy Coding!**

---

## 📌 Endpoints

### **📘 Get Books (with Filtering, Pagination, and Sorting)**

#### **Endpoint:**

```http
GET /books
```

#### **Query Parameters:**

| Parameter | Type      | Description                                                              |
| --------- | --------- | ------------------------------------------------------------------------ |
| `title`   | `string`  | Search books by title (optional)                                         |
| `author`  | `string`  | Search books by author (optional)                                        |
| `year`    | `integer` | Filter books by publication year (optional)                              |
| `sort_by` | `string`  | Sort books by `title`, `author`, or `year` (default: `title`)            |
| `order`   | `string`  | Sorting order: `asc` (ascending) or `desc` (descending) (default: `asc`) |
| `skip`    | `integer` | Number of records to skip (default: `0`)                                 |
| `limit`   | `integer` | Number of records to return per page (default: `10`, max: `100`)         |

#### **Example Requests:**

1️⃣ **Get first 10 books sorted by title (default order):**

```sh
GET /books
```

2️⃣ **Find books by author "Robert C. Martin" and sort by year (newest first):**

```sh
GET /books?author=martin&sort_by=year&order=desc
```

3️⃣ **Paginate results (skip first 10, return next 10 books):**

```sh
GET /books?skip=10&limit=10
```

4️⃣ **Sort books by title (Z-A) and return only 5 results:**

```sh
GET /books?sort_by=title&order=desc&limit=5
```

#### **Example Response:**

```json
{
  "total": 100,
  "books": [
    {
      "id": 1,
      "title": "Clean Code",
      "author": "Robert C. Martin",
      "year": 2008
    },
    {
      "id": 2,
      "title": "The Pragmatic Programmer",
      "author": "Andrew Hunt",
      "year": 1999
    }
  ]
}
```

---

## 🔜 Next Steps: Authentication

We will now implement **JWT-based authentication** to secure the API.

Stay tuned! 🚀
