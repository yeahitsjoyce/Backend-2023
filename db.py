from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

mood_table = db.Table(
    "mood",
    db.Column("song_id", db.Integer, db.ForeignKey("song.id")),
    db.Column("mood_id", db.Integer, db.ForeignKey("mood.id"))
)

likes_table = db.Table(
    "all_likes",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("song_id", db.Integer, db.ForeignKey("song.id"))
)

class Artist(db.Model):
    """
    Has a one to many relationship with Albums
    """
    __tablename__="artist"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    albums = db.relationship("Album", cascade="delete")

    def __init__(self, **kwargs):
        """
        Creates an Artist Object
        """
        self.name = kwargs.get("name","")

    def serialize(self):
        """
        Serializes an Artist Object
        """
        return {
            "id": self.id,
            "name": self.name,
            "albums": [album.serialize() for album in self.albums]
        }

class Album(db.Model):
    """
    Has a One to Many relationship with Songs
    """
    __tablename__="album"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"), nullable = False)
    songs = db.relationship("Song", cascade="delete")

    def __init__(self,**kwargs):
        """
        Creates an Album object
        """
        self.name = kwargs.get("name","")
        self.artist_id = kwargs.get("artist_id")

    def serialize(self):
        """
        Serializes an Album Object
        """
        return {
            "id": self.id,
            "name": self.name,
            "songs": [song.simple_serialize() for song in self.songs]
        }

class Song(db.Model):
    """
    Has a one to many relationship with comments
    Has a many to many relationship with moods
    Has a many to many relationship with users
    """
    __tablename__="song"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    length = db.Column(db.Real, nullable = False)
    streams = db.Column(db.Integer, nullable = False)
    album_id = db.Column(db.Integer, db.ForeignKey("album.id"))
    comments = db.relationship("Comment", cascade="delete")
    moods = db.relationship("Mood", secondary=mood_table, back_populates="songs")
    liked = db.relationship("User", secondary=likes_table, back_populates="likes")

    def __init__(self, **kwargs):
        """
        Creates a Song object
        """
        self.name = kwargs.get("name")
        self.length = kwargs.get("length")
        self.streams = kwargs.get("streams")
        self.album_id = kwargs.get("album_id")
    
    def serialize(self):
        """
        Serialize a song object
        """
        return {
            "id": self.id,
            "name": self.name,
            "length": self.length,
            "streams": self.streams,
            "album_id": self.album_id,
            "comments": [comment.serialize() for comment in self.comments],
            "moods": [mood.simple_serialize() for mood in self.moods]
        }

    def simple_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "length": self.length,
            "streams": self.streams
        }

class Comment(db.Model):
    """
    Comment Model
    """
    __tablename__="comment"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_comment = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    song_id = db.Column(db.Integer, db.ForeignKey("song.id"), nullable = False)
    
    def __init__(self,**kwargs):
        """
        Creates a comment object
        """
        self.user_comment = kwargs.get("comment")
        self.user_id = kwargs.get("user_id")
        self.song_id = kwargs.get("song_id")

    def serialize(self):
        """
        Serialize a comment object
        """
        return {
            "id":self.id,
            "user_comment": self.user_comment,
            "user_id": self.user_id,
            "song_id": self.song_id
        }


class Mood(db.Model):
    """
    Mood Model
    """
    __tablename__="mood"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    description = db.Column(db.String, nullable = False)
    color = db.Column(db.String, nullable=False)
    song_mood = db.relationship("Song", secondary=mood_table, back_populates="moods")
    
    def __init__(self, **kwargs):
        """
        Creates a mood object
        """
        self.description = kwargs.get("description","")
        self.color = kwargs.get("color")

    def serialize(self):
        """
        Serializes a mood object
        """
        return {
            "id": self.id,
            "description": self.description,
            "color": self.color,
            "song_mood": [song.serialize() for song in self.song_mood]
        }

class User(db.Model):
    """
    Has a one to many relationship with comments
    Has a many to many relationship with songs
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    comments = db.relationship("Comment", cascade="delete")
    likes = db.relationship("Song", secondary=likes_table, back_populates="Liked")

    def __init__(self, **kwargs):
        """
        Initializes a User Object
        """
        self.name = kwargs.get("name")

    def serialize(self):
        """
        Serialize a User object
        """
        return {
            "id":self.id,
            "name":self.name,
            "likes": [song.serialize() for song in self.likes]
        }

