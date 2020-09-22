# Book DB
A simple microservice to act as an initial exemplar.
This microservice wraps a database of books in a REST API.


## Building the service
1. Install and run [Docker](https://www.docker.com/).
2. In the `book-db` directory, run `docker build -t book-db .`
3. Run `docker run -p 5000:5000 book-db`
4. Book DB should be running at [http://localhost:5000/](http://localhost:5000/)


## API requests

### Create book
Send a POST request to `/api/book` with a JSON object containing the following attributes.

| Attribute      | Type     |
| -------------- | -------- |
| title          | `string` |
| author         | `string` |
| year_published | `int`    |

### Read book

Send a GET request to `/api/book/:id:` to receive a response containing a JSON object representing the book with ID `:id:`.

### Update book

Send a PUT request to `/api/book/:id:` with a JSON object containing the following attributes.
Note that the `id` attribute should match `:id:` in the URL.

| Attribute      | Type     |
| -------------- | -------- |
| id             | `int`    |
| title          | `string` |
| author         | `string` |
| year_published | `int`    |

### Delete book

Send a DELETE request to `/api/book/:id:` to delete the book with ID `:id:`.

### Filter books

Send a GET request to `/api/books` to retrieve a JSON list of objects corresponding to all of the books matching the filters given in the following query string parameters.
All parameters are optional.

- `author`
- `year`

For example, send a GET request to `/api/books?author=John%20Doe&year=2020` to filter the response to books authored by John Doe and published in 2020.
