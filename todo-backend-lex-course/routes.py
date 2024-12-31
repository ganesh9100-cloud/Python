from app import app, db
from models import Task, Event
from flask import jsonify, request, render_template, url_for
from sqlalchemy.sql import text

@app.route('/')
def hello_world():
    return "Hello, World!!"

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()      # This is for Json data response AJAX
    tasks_data = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_completed": task.is_completed,
            # Safely format the date field, assuming "created_at" exists
        }
        for task in tasks
    ]
    # # return """<h1>hello world</h1>""", 200
    return tasks_data
    return jsonify(tasks_data), 200
    return render_template('tasks.html')

@app.route('/tasks', methods=['POST'])
def create_task():
    # data = request.json       #This is for Json data response AJAX
    # new_task = Task(title=data['title'], description=data.get('description'))
    title = request.form.get('title')
    description = request.form.get('description')
    completed = request.form.get('fav_language')
    comp = True if completed == 'HTML' else False
    new_task = Task(title=title, description=description, is_completed=comp)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task created!"}), 201

@app.route('/infyEvents', methods=['GET'])
def get_events():
    return """
        <!DOCTYPE html>
		<head> <title>InfyEvents</title> </head>
		<body>
			<center>
			<h1> InfyEvents </h1>
			<ul type='none'> <li>Home</li> <li>Admin</li> </ul>
			<div> PARTICIPATE - LEARN - GROW </div> <br />
			
			<div> Upcoming Events </div> <br />
			<div>	
				<div> DC Hackathon </div>
				<div> 2021-09-12 09:00:00 </div>
				<div> Organizer : John Mathew </div>
			</div>
			<br />
			<div>				
				<div> DRR Camp </div>
				<div> 2022-01-05 11:30:00 </div>
				<div> Organizer : Ben Fedrick </div>
			</div>
			<br />
			<div>
				<div> Designing Webinar </div>					
				<div> 2021-10-11 14:30:00 </div>
				<div> Organizer : John Mathew </div>
			</div>
			<br />
			<div>
				Copyright 2021 All rights reserved | This template is made by ETA
			</div>
			</center>
		</body>
		</html>
	"""

@app.route('/templateEvents/<location>', methods=['GET'])
def template_events(location):
    return render_template('events.html', loc = location)


@app.route('/ex1/<location>/<int:year>', methods=['GET'])
def view_events_by_location_year(year, location):
    return location + "%d" %year

@app.route('/register', methods=['GET', 'POST'])
def user_registration():
    db.session.flush()
    if request.method == 'POST':
        user_name = request.form['username']
        user_email = request.form['useremail']
        registered_event = request.form['eventname']
        password = request.form['password']
        confirm_password = request.form['confirmpassword']
        message = ""
        # result = db.session.execute(text("SELECT * FROM events")).fetchall()
        # print(result)
        if (password == confirm_password):
            event_id = db.session.execute(text('SELECT event_id FROM events WHERE event_name = :event_name'), {'event_name': registered_event} ).fetchone()
            if event_id:
                already_registered = db.session.execute(text('SELECT COUNT(1) FROM event_registration WHERE LOWER(usermail) = :usermail AND event_id = :event_id'), { 'usermail': user_email.lower(), 'event_id': event_id[0] } ).fetchone()
                if already_registered[0] == 0:
                    seats_available = db.session.execute(text('SELECT COUNT(1) FROM events WHERE event_id = :event_id AND seats_available > 0 AND event_time > CURRENT_TIMESTAMP'), { 'event_id': event_id[0] } ).fetchone()
                    print(seats_available)
                    if seats_available[0] > 0:
                        db.session.execute(text('INSERT INTO event_registration (username, usermail, userpassword, event_id) VALUES (:username, :usermail, :userpassword, :event_id)'), { 'username': user_name, 'usermail': user_email, 'userpassword': password, 'event_id': event_id[0] } )
                        db.session.execute(text('UPDATE events SET seats_available = seats_available - 1 WHERE event_id = :event_id'), { 'event_id': event_id[0] })
                        db.session.commit()
                        message = "Registered successfully !"
                    else:                        
                        message = "Oops! Registration is closed!"
                else:
                    message = "You have already registered for the event " + registered_event
            else:
                message = "Event does not exist!"
        else:
            message = "Password and confirm password does not match"
        return render_template('register.html', message = message)    
    else:
        return render_template('register.html')
