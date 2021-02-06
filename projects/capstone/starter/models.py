from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy


database_name = "casting"
database_path = "postgresql://{}:{}@{}/{}".format('brian', 'admin', 'localhost:5432', database_name)
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class Movie(db.Model):
    __tablename__ = 'movies'
    # Autoincrementing, unique primary key
    id = db.Column(db.Integer, primary_key=True)
    # String Title
    title = db.Column(db.String, nullable = False)
    # String Release Date
    release_date = db.Column(db.String, nullable = False)

    '''
    insert()
        inserts a new model into a database
        the model must have a unique id or null id
        the model must have a title (not null) and release_date (not null)
        EXAMPLE:
            movie = Movie(title=req_title, release_date=req_recipe)
            movie.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    update()
        updates a model in the database
        the model must exist in the database
        EXAMPLE:
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            movie.title = 'Last for One'
            movie.update()
    '''
    def update(self):
        db.session.commit()

    '''
    delete()
        deletes a model from the database
        the model must exist in the database
        EXAMPLE:
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            movie.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Movie {self.id} {self.title} {self.release_date}>'

class Actor(db.Model):
    __tablename__ = 'actors'
    # Autoincrementing, unique primary key
    id = db.Column(db.Integer, primary_key=True)
    # String Name
    name = db.Column(db.String, nullable = False)
    # Integer Age
    age = db.Column(db.Integer, nullable = False)
    # String Gender
    gender = db.Column(db.String, nullable = False)

    '''
    insert()
        inserts a new model into a database
        the model must have a unique id or null id
        the model must have a title (not null) and release_date (not null)
        EXAMPLE:
            actor = Actor(name=req_name, age=req_age, gender=reg_age)
            actor.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    update()
        updates a model in the database
        the model must exist in the database
        EXAMPLE:
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            actor.name = 'Samson'
            actor.update()
    '''
    def update(self):
        db.session.commit()

    '''
    delete()
        deletes a model from the database
        the model must exist in the database
        EXAMPLE:
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            actor.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Actor {self.id} {self.name} {self.age} {self.gender}>'