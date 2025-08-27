# Books API - View Documentation

## ListView
- **Endpoint:** GET /books/
- **Description:** Retrieves all books.
- **Permissions:** Public
- **Features:** Filtering, searching, ordering

## DetailView
- **Endpoint:** GET /books/<pk>/
- **Description:** Retrieves a single book by its ID.
- **Permissions:** Public

## CreateView
- **Endpoint:** POST /books/create/
- **Description:** Creates a new book.
- **Permissions:** Authenticated users only
- **Custom Hooks:** 
  - Ensures title is unique (case-insensitive)
  - Publication year cannot be in the future

## UpdateView
- **Endpoint:** PATCH/PUT /books/<pk>/update/
- **Description:** Updates an existing book.
- **Permissions:** Authenticated users only
- **Custom Hooks:** 
  - Title cannot be empty
  - Author cannot be changed

## DeleteView
- **Endpoint:** DELETE /books/<pk>/delete/
- **Description:** Deletes a book.
- **Permissions:** Authenticated users only
