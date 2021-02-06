from flask_sqlalchemy import SQLAlchemy


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

class Movies(db.Model):
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
            movie = Movie(title=req_title, release_date=req_recipe)
            movie.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()