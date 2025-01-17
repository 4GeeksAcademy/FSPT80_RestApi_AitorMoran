from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#TABLA PEOPLE ______________________________________________________

class People (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    lastname = db.Column(db.String(150), nullable=False)
    side = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "side": self.side
        }
    

#TABLA PLANETAS ______________________________________________________

class Planets (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    terrain = db.Column(db.String(150), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    galaxy = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "population": self.population,
            "galaxy": self.galaxy
        }
    

#TABLA FAVORITOS PEOPLE ______________________________________________________


class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)

    person = db.relationship('People', backref=db.backref('favorites', lazy=True))

    def __repr__(self):
        return f'<Favorites {self.person_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "person_id": self.person_id
        }
    

#TABLA FAVORITOS PLANETS ______________________________________________________


class Planetforites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)

    planet = db.relationship('Planets', backref=db.backref('planetforites', lazy=True))

    def __repr__(self):
        return f'<Planetforites {self.planet_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id
        }