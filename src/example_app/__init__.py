# Import required libraries
import datetime

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Create a new Flask app
app = Flask(__name__)

# Configure the database
db_uri = "sqlite:///events.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a new database connection
db = SQLAlchemy(app)


# Define a database model for events
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, title, start_time, end_time):
        self.title = title
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return f"Event(title='{self.title}', start_time='{self.start_time}', end_time='{self.end_time}')"


def create_database():
    with app.app_context():
        db.create_all()


def database_exists():
    with app.app_context():
        try:
            db.session.query("1").from_statement("SELECT 1").all()
            return True
        except:
            return False


with app.app_context():
    if not database_exists():
        create_database()
    db.create_all()


# Route for displaying the calendar
@app.route("/")
def calendar():
    events = Event.query.all()
    return render_template('calendar.html', events=events)


@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        start_time = datetime.datetime.strptime(request.form['date'], '%Y-%m-%d')
        end_time = datetime.datetime.strptime(request.form['date'], '%Y-%m-%d')

        event = Event(title=request.form['name'], start_time=start_time, end_time=end_time)
        db.session.add(event)
        db.session.commit()
        return redirect('/')
    return render_template('add.html')


# Route for creating new events
@app.route("/create", methods=['POST'])
def create():
    title = request.form['title']
    start_time = request.form['start_time']
    end_time = request.form['end_time']

    event = Event(title=title, start_time=start_time, end_time=end_time)
    db.session.add(event)
    db.session.commit()

    return redirect('/')


# Route for updating events
@app.route("/edit_event/<int:id>", methods=['POST'])
def edit_event(id):
    event = Event.query.get(id)
    event.title = request.form['title']
    event.start_time = request.form['start_time']
    event.end_time = request.form['end_time']

    db.session.commit()

    return redirect('/')


@app.route("/delete_event/<int:id>", methods=['POST'])
def delete_event(id):
    event = Event.query.get(id)
    db.session.delete(event)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
