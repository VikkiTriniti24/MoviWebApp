from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, joinedload

# --- Base & Models ---
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    movies = relationship('Movie', back_populates='user', cascade='all, delete-orphan')
    reviews = relationship('Review', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User id={self.id} name={self.name!r}>"

class Director(Base):
    __tablename__ = 'directors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    birth_date = Column(String)

    movies = relationship('Movie', back_populates='director', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Director id={self.id} name={self.name!r}>"

class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    movies = relationship('Movie', back_populates='genre', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Genre id={self.id} name={self.name!r}>"

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    year = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    director_id = Column(Integer, ForeignKey('directors.id'), nullable=True)
    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=True)

    user = relationship('User', back_populates='movies')
    director = relationship('Director', back_populates='movies')
    genre = relationship('Genre', back_populates='movies')
    reviews = relationship('Review', back_populates='movie', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Movie id={self.id} title={self.title!r} year={self.year}>"

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    text = Column(Text)

    user = relationship('User', back_populates='reviews')
    movie = relationship('Movie', back_populates='reviews')

    def __repr__(self):
        return (f"<Review id={self.id} user_id={self.user_id} "
                f"movie_id={self.movie_id} rating={self.rating}>")

# --- DataManager ---
class SQLiteDataManager:
    def __init__(self, db_path: str = 'moviwebapp.db'):
        # db_path: Datei-Name oder ':memory:'
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False, future=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, future=True)

    def reset_database(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    # --- User Methods ---
    def get_all_users(self):
        with self.Session() as session:
            return session.query(User).all()

    def add_user(self, user: User):
        with self.Session() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def get_user_by_id(self, user_id: int):
        with self.Session() as session:
            return session.query(User).filter(User.id == user_id).one_or_none()

    def update_user_name(self, user_id: int, new_name: str):
        with self.Session() as session:
            user = session.query(User).filter(User.id == user_id).one_or_none()
            if not user:
                raise ValueError('User not found')
            user.name = new_name
            session.commit()
            return user

    # --- Movie Methods ---
    def get_all_movies(self):
        with self.Session() as session:
            return session.query(Movie).all()

    def get_user_movies(self, user_id: int):
        with self.Session() as session:
            return session.query(Movie).filter(Movie.user_id == user_id).all()

    def add_movie(self, movie: Movie):
        with self.Session() as session:
            session.add(movie)
            session.commit()
            session.refresh(movie)
            return movie

    def add_movie_to_user(self, user_id: int, title: str, year: int = None):
        with self.Session() as session:
            if session.get(User, user_id) is None:
                raise ValueError('User not found')
            movie = Movie(user_id=user_id, title=title, year=year)
            session.add(movie)
            session.commit()
            session.refresh(movie)
            return movie.id

    def get_movie_by_id(self, movie_id: int):
        with self.Session() as session:
            return session.query(Movie).filter(Movie.id == movie_id).one_or_none()

    def update_movie(self, movie: Movie):
        with self.Session() as session:
            existing = session.query(Movie).filter(Movie.id == movie.id).one_or_none()
            if not existing:
                raise ValueError('Movie not found')
            existing.title = movie.title
            existing.year = movie.year
            existing.director_id = movie.director_id
            existing.genre_id = movie.genre_id
            session.commit()
            return existing

    def delete_movie(self, movie_id: int):
        with self.Session() as session:
            movie = session.query(Movie).filter(Movie.id == movie_id).one_or_none()
            if not movie:
                raise ValueError('Movie not found')
            session.delete(movie)
            session.commit()

    # --- Director Methods ---
    def get_all_directors(self):
        with self.Session() as session:
            return session.query(Director).all()

    def add_director(self, director: Director):
        with self.Session() as session:
            session.add(director)
            session.commit()
            session.refresh(director)
            return director

    # --- Genre Methods ---
    def get_all_genres(self):
        with self.Session() as session:
            return session.query(Genre).all()

    def add_genre(self, genre: Genre):
        with self.Session() as session:
            session.add(genre)
            session.commit()
            session.refresh(genre)
            return genre

    # --- Review Methods ---
    def add_review(self, review: Review):
        with self.Session() as session:
            session.add(review)
            session.commit()
            session.refresh(review)
            return review

    def add_review_from_data(self, user_id: int, movie_id: int, text: str, rating: int):
        with self.Session() as session:
            review = Review(user_id=user_id, movie_id=movie_id, text=text, rating=rating)
            session.add(review)
            session.commit()
            session.refresh(review)
            return review

    def get_reviews_for_movie(self, movie_id):
        with self.Session() as session:
            return (
                session.query(Review)
                .options(joinedload(Review.user))  # eager load user
                .filter(Review.movie_id == movie_id)
                .all()
            )

    def get_reviews_by_user(self, user_id: int):
        with self.Session() as session:
            return session.query(Review).filter(Review.user_id == user_id).all()
