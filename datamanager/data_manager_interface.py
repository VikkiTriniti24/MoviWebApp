from abc import ABC, abstractmethod

class DataManagerInterface(ABC):
    @abstractmethod
    def get_all_users(self):
        """Return a list of all users."""
        pass

    @abstractmethod
    def add_user(self, user):
        """Add a new user and return it."""
        pass

    @abstractmethod
    def get_user_by_id(self, user_id):
        """Return a single user by ID or None if not found."""
        pass

    @abstractmethod
    def get_all_movies(self):
        """Return a list of all movies."""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """Return a list of movies for a given user ID."""
        pass

    @abstractmethod
    def get_movie_by_id(self, movie_id):
        """Return a single movie by ID or None if not found."""
        pass

    @abstractmethod
    def add_movie(self, movie):
        """Add a new movie and return it."""
        pass

    @abstractmethod
    def update_movie(self, movie):
        """Update an existing movie."""
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        """Delete a movie by ID."""
        pass

    @abstractmethod
    def add_movie_to_user(self, user_id, title, year=None):
        """Convenience: create and assign a new movie to a user."""
        pass

    @abstractmethod
    def get_reviews_for_movie(self, movie_id):
        """Return a list of reviews for a given movie ID."""
        pass

    @abstractmethod
    def add_review(self, review):
        """Add a new review and return it."""
        pass

    @abstractmethod
    def add_review_from_data(self, user_id, movie_id, text, rating):
        """Convenience: create and add a review by providing raw data."""
        pass

    @abstractmethod
    def get_all_directors(self):
        """Return a list of all directors."""
        pass

    @abstractmethod
    def add_director(self, director):
        """Add a new director and return it."""
        pass

    @abstractmethod
    def get_all_genres(self):
        """Return a list of all genres."""
        pass

    @abstractmethod
    def add_genre(self, genre):
        """Add a new genre and return it."""
        pass

    @abstractmethod
    def reset_database(self):
        """Reset the database (drop and recreate all tables)."""
        pass
