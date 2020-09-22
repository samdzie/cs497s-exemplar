"""A Flask app to store books in a database."""

from flask import Flask, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow.exceptions import ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Book(db.Model):
    """Book SQLAlchemy model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    year_published = db.Column(db.Integer)

    def __repr__(self):
        return '<Book %r>' % self.id


class BookSchema(SQLAlchemyAutoSchema):
    """Book Marshmallow-SQLAlchemy serialization schema."""
    class Meta:
        model = Book
        load_instance = True

    id = auto_field()
    title = auto_field()
    author = auto_field()
    year_published = auto_field()


@app.route('/api/')
def welcome():
    """Return a welcome message for the API."""
    return 'Welcome to the Exemplary Book API!'


@app.route('/api/book', methods=['POST'])
def create_book():
    """Add a book to the database."""
    schema = BookSchema()
    try:
        book = schema.load(request.json, session=db.session)
    except ValidationError:
        abort(400)
    db.session.add(book)
    db.session.commit()
    return jsonify(schema.dump(book))


@app.route('/api/book/<int:book_id>')
def read_book(book_id):
    """Respond with a JSON object representing a book."""
    book = Book.query.filter_by(id=book_id).first()
    if book is None:
        abort(404)
    schema = BookSchema()
    return jsonify(schema.dump(book))


@app.route('/api/book/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Update a book's info in the database."""
    book = Book.query.filter_by(id=book_id).first()
    if book is None:
        abort(404)
    schema = BookSchema()
    try:
        book = schema.load(request.json, session=db.session)
    except ValidationError:
        abort(400)
    db.session.add(book)
    db.session.commit()
    return jsonify(schema.dump(book))


@app.route('/api/book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a book from the database."""
    book = Book.query.filter_by(id=book_id).first()
    if book is None:
        abort(404)
    db.session.delete(book)
    db.session.commit()
    schema = BookSchema()
    return jsonify(schema.dump(book))


@app.route('/api/books')
def list_books():
    """List all books matching author and year published filters."""
    books = Book.query
    if (author := request.args.get('author')) is not None:
        books = books.filter_by(author=author)
    if (year := request.args.get('year')) is not None:
        books = books.filter_by(year_published=int(year))
    books = books.all()
    schema = BookSchema(many=True)
    return jsonify(schema.dump(books))
