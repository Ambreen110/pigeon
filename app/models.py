from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from datetime import timedelta, datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Cup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    competitions = db.relationship('Competition', backref='cup', lazy=True)


class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    poster = db.Column(db.String(100), nullable=True)
    cup_id = db.Column(db.Integer, db.ForeignKey('cup.id'), nullable=False)
    participants = db.relationship('Participant', backref='competition', lazy=True)
    start_time = db.Column(db.Time, nullable=False)  # Added start time



class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    profile_pic = db.Column(db.String(100), nullable=True)
    landing_times1 = db.Column(db.Time, nullable=True)
    landing_times2 = db.Column(db.Time, nullable=True)
    landing_times3 = db.Column(db.Time, nullable=True)
    landing_times4 = db.Column(db.Time, nullable=True)
    landing_times5 = db.Column(db.Time, nullable=True)
    landing_times6 = db.Column(db.Time, nullable=True)
    landing_times7 = db.Column(db.Time, nullable=True)
    landing_times8 = db.Column(db.Time, nullable=True)
    landing_times9 = db.Column(db.Time, nullable=True)
    landing_times10 = db.Column(db.Time, nullable=True)
    landing_times11 = db.Column(db.Time, nullable=True)
    landing_times12 = db.Column(db.Time, nullable=True)
    total_time = db.Column(db.String(100), nullable=True)

    @property
    def times(self):
        return [
            self.landing_times1,
            self.landing_times2,
            self.landing_times3,
            self.landing_times4,
            self.landing_times5,
            self.landing_times6,
            self.landing_times7,
            self.landing_times8,
            self.landing_times9,
            self.landing_times10,
            self.landing_times11,
            self.landing_times12,
        ]

    def calculate_total_time(self, start_time):
        total_seconds = 0
        for landing_time in self.times:
            if landing_time:
                # Your existing logic for calculating time difference
                landing_time_dt = datetime.combine(datetime.min, landing_time)
                competition_start_time_dt = datetime.combine(datetime.min, start_time)
                difference = landing_time_dt - competition_start_time_dt
                total_seconds += abs(difference.total_seconds())
            else:
                continue  # Skip if the time is not provided

        total_time = str(timedelta(seconds=total_seconds))
        self.total_time = total_time
        return total_time

    def save(self):
        competition = Competition.query.get(self.competition_id)
        if competition and competition.start_time:
            self.total_time = self.calculate_total_time(competition.start_time)
        db.session.add(self)
        db.session.commit()
