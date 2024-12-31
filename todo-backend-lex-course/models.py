from app import app,db

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    is_completed = db.Column(db.Boolean, default=False)
    # timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Task {self.title}>'

class Event(db.Model):
    __tablename__ = 'events'  # Table name in the database

    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_name = db.Column(db.String(255), nullable=False)
    event_desc = db.Column(db.String(500), nullable=False)
    event_location = db.Column(db.String(255), nullable=False)
    event_time = db.Column(db.DateTime, nullable=False)
    organiser = db.Column(db.String(255), nullable=False)
    seats_available = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Event {self.event_name}, {self.organiser}, {self.event_time}>"

class EventRegistration(db.Model):
    __tablename__ = 'event_registration'

    register_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    usermail = db.Column(db.String(100), nullable=False)
    userpassword = db.Column(db.String(100), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
    
    # You can create a unique constraint on usermail + event_id
    __table_args__ = (db.UniqueConstraint('usermail', 'event_id', name='_usermail_event_uc'),)
    
    def __repr__(self):
        return f'<EventRegistration {self.username} for Event {self.event_id}>'

# Create tables
with app.app_context():
    event_instance = db.session.query(Event)
    db.create_all()

