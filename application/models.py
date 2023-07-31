from application.database import db
from flask_sqlalchemy import SQLAlchemy








roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))    

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String, unique=False,nullable=False)
    email = db.Column(db.String, unique=True,nullable=False)
    password = db.Column(db.String(255),nullable=False)
    roles = db.relationship('Role', secondary=roles_users,backref=db.backref('users', lazy='dynamic'))
    tickets = db.relationship('Venue_Event', secondary='user_ticket_1', backref=db.backref('users', lazy='dynamic'))

class Event(db.Model):
     __tablename__="event"
     event_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
     name=db.Column(db.String(200),unique=True)
     price=db.Column(db.Integer())
     duration=db.Column(db.Float())
     venues=db.relationship("Venue",secondary="venue_event")
    
     def update_capacity_in_venue_event(self):
        venue_events = Venue_Event.query.filter_by(e_id=self.event_id).all()
        for venue_event in venue_events:
            venue=Venue.query.get(venue_event.v_id)
            venue_event.capacity=venue.capacity
        db.session.commit()


class Venue(db.Model):
    __tablename__="venue"
    venue_id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
    name=db.Column(db.String(200),unique=True)
    location=db.Column(db.String(200))
    capacity=db.Column(db.Integer)
    events=db.relationship("Event",secondary="venue_event",overlaps="venues")
    
    
    def update_capacity_in_venue_event(self):
        venue_events = Venue_Event.query.filter_by(v_id=self.venue_id).all()
        for venue_event in venue_events:
            venue_event.capacity = self.capacity
        db.session.commit()


class Venue_Event(db.Model):
   __tablename__="venue_event"
   ve_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
   v_id = db.Column(db.Integer,db.ForeignKey("venue.venue_id"), nullable=False)
   e_id = db.Column(db.Integer,db.ForeignKey("event.event_id"), nullable=False)
   capacity=db.Column(db.Integer)


class User_Ticket_1(db.Model):
    __tablename__ = 'user_ticket_1'
    ut_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ve_id = db.Column(db.Integer, db.ForeignKey('venue_event.ve_id'), nullable=False)
    tickets = db.Column(db.Integer)