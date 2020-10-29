"""A template Flask app for creating new services.

Please include a descriptive docstring like this at the beginning of
your code. It should give a one-line summary of its purpose and more
details below if it would help readers understand your code.

Be sure to use comments and docstrings to make your code readable!
It'll help both you and other developers.
"""
from flask import abort, Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import auto_field, SQLAlchemySchema


app = Flask(__name__)
# Make the database at /srv/template/db/data.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////srv/template/db/data.db'
# Do not track modifications to save overhead
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Album(db.Model):
    """A SQLAlchemy model representing an album."""
    # ID is an integer and serves as a primary key (i.e., unique identifier)
    id = db.Column(db.Integer, primary_key=True)
    # Title and artist are strings that cannot be left null
    title = db.Column(db.String(80), nullable=False)
    artist = db.Column(db.String(80), nullable=False)


# Create all tables; all models must be defined above this line
db.create_all()


class AlbumSchema(SQLAlchemySchema):
    class Meta:
        model = Album # Generate the schema from the above Album model
        load_instance = True

    # Automatically fill these fields
    id = auto_field()
    title = auto_field()
    artist = auto_field()


@app.route('/')
def hello_world():
    """A simple hello world for testing."""
    return 'hello world!'


@app.route('/album', methods=['POST'])
def create_album():
    """Create an album from a POSTed JSON object."""
    # If the request has no JSON, respond HTTP 400
    json = request.json
    if json is None:
        abort(400)
    # If the JSON exists but has no title or artist, respond HTTP 400
    title = json.get('title')
    artist = json.get('artist')
    if title is None or artist is None:
        abort(400)
    # Create the album object
    album = Album(title=title, artist=artist)
    # Add it to the database
    db.session.add(album)
    db.session.commit()
    # Serialize the album as a JSON object and return it
    schema = AlbumSchema()
    return jsonify(schema.dump(album))


@app.route('/album/<album_id>')
def get_album(album_id):
    """Return the album with the given ID as a JSON object."""
    # Filter albums matching album_id and select the first one found
    album = Album.query.filter_by(id=album_id).first()
    # If no album matches album_id, respond HTTP 404
    if album is None:
        abort(404)
    # Serialize the album as a JSON object and return it
    schema = AlbumSchema()
    return jsonify(schema.dump(album))


@app.route('/album/<album_id>', methods=['PUT'])
def update_album(album_id):
    """Update the album with the given ID."""
    # If the request has no JSON, respond HTTP 400
    json = request.json
    if json is None:
        abort(400)
    # Filter albums matching album_id and select the first one found
    album = Album.query.filter_by(id=album_id).first()
    # If no album matches album_id, respond HTTP 404
    if album is None:
        abort(404)
    # Update the title and/or artist, if present in JSON
    if 'title' in json:
        album.title = json.get('title')
    if 'artist' in json:
        album.artist = json.get('artist')
    # Add it to the database
    db.session.add(album)
    db.session.commit()
    # Serialize the album as a JSON object and return it
    schema = AlbumSchema()
    return jsonify(schema.dump(album))


@app.route('/album/<album_id>', methods=['DELETE'])
def delete_album(album_id):
    """Delete the album with the given ID."""
    # Filter albums matching album_id and select the first one found
    album = Album.query.filter_by(id=album_id).first()
    # If no album matches album_id, respond HTTP 404
    if album is None:
        abort(404)
    # Delete it from the database
    db.session.delete(album)
    db.session.commit()
    # Serialize the album as a JSON object and return it
    schema = AlbumSchema()
    return jsonify(schema.dump(album))
