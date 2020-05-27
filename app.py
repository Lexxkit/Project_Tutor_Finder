"""Before the first start of this app:
1. Run 'project_bd.py' script to create all necessary DB-like json files.
2. Make DB migration
3. Run add_data_to_db() function to fill the DB with data.
If you add a new goal in the GOALS dict - run update_goals_db() function. You can add icon
for it in the goals_pics dictionary in the 'base.html' template for render it at web pages.
"""
import json

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, RadioField
from wtforms.validators import InputRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.secret_key = 'mysecretstring'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# set goals
GOALS = {"travel": "Для путешествий", "study": "Для учебы", "work": "Для работы",
         "relocate": "Для переезда", 'program': 'Для программирования'}


# declare BookingForm for 'booking.html' template
class BookingForm(FlaskForm):
    client_name = StringField("Вас зовут", [InputRequired()])
    client_phone = StringField("Ваш телефон", [InputRequired()])
    client_weekday = HiddenField()
    client_time = HiddenField()
    client_teacher = HiddenField()


# declare RequestForm for 'request.html' template
class RequestForm(FlaskForm):
    goal_buttons = RadioField('goal', choices=[(k, v) for k, v in GOALS.items()])
    time_buttons = RadioField('time', choices=[('1-2 часа в неделю', '1-2 часа в неделю'),
                                               ('3-5 часов в неделю', '3-5 часов в неделю'),
                                               ('5-7 часов в неделю', '5-7 часов в неделю'),
                                               ('7-10 часов в неделю', '7-10 часов в неделю')])
    client_name = StringField('Вас зовут', [InputRequired()])
    client_phone = StringField('Ваш телефон', [InputRequired()])


tutors_goals_association = db.Table('tutors_goals',
                                    db.Column('tutor_id', db.Integer, db.ForeignKey('tutors.id')),
                                    db.Column('goal_id', db.Integer, db.ForeignKey('goals.id'))
                                    )


# create Tutor DB model
class Tutor(db.Model):
    __tablename__ = 'tutors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    about = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    free = db.Column(db.Text, nullable=False)
    students = db.relationship('Booking', back_populates='tutor')
    goals = db.relationship('Goal', secondary=tutors_goals_association, back_populates='tutors')


# create Booking DB model
class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    day = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutors.id'))
    tutor = db.relationship('Tutor', back_populates='students')


# create Request DB model
class RequestTutor(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    goal = db.Column(db.String, nullable=False)


class Goal(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key=True)
    goal_badge = db.Column(db.String(15), nullable=False)
    goal_name = db.Column(db.String(30), nullable=False)
    tutors = db.relationship('Tutor', secondary=tutors_goals_association, back_populates='goals')


def add_data_to_db(data='teachers_bd.json', goals_dict=GOALS):
    """Export data from json file to SQL DB table 'tutors'.
    Export data from GOALS dict to DB table 'goals'.
    Create many-to-many relation between 'tutors' and 'goals' tables.
    Should be run manually after the first DB migration.
    """
    # Read information from JSON file
    with open(data, 'r') as f_hand:
        tutors = json.load(f_hand)

    # add data to DB 'goals' table
    for badge, name in goals_dict.items():
        new_goal = Goal(goal_badge=badge, goal_name=name)
        db.session.add(new_goal)

    # add data to DB 'tutors' table
    for tutor in tutors:
        # create string from dict object
        free = json.dumps(tutor['free'])

        new_entry = Tutor(name=tutor['name'], about=tutor['about'],
                          rating=tutor['rating'], picture=tutor['picture'],
                          price=tutor['price'], free=free)
        db.session.add(new_entry)
        # connect 'goals' and 'tutors'
        for goal in tutor['goals']:
            goal_query = Goal.query.filter(Goal.goal_badge == goal).first()
            new_entry.goals.append(goal_query)

    db.session.commit()


def update_goals_db(goals_dict, tutors_id_list):
    """Append new goals to the DB 'goals' table and
    set connection with chosen tutors.
    Should be run manually.

    :param goals_dict: extended GOALS or new dict with goals
    :param tutors_id_list: list of tutor_ids to whom new goals should be connected
    """
    for badge, name in goals_dict.items():
        goals_query = Goal.query.filter(Goal.goal_badge == badge).all()
        if not goals_query:
            new_goal = Goal(goal_badge=badge, goal_name=name)
            db.session.add(new_goal)
            for tutor_id in tutors_id_list:
                tutor_query = Tutor.query.get(tutor_id)
                if tutor_query:
                    new_goal.tutors.append(tutor_query)
                    print(f'New goal {new_goal.goal_badge} added to tutor {tutor_query.id}')

    db.session.commit()


@app.route('/')
def index():
    # get 6 random tutors from DB
    random_tutors = Tutor.query.order_by(db.func.random()).limit(6).all()
    goals_all = Goal.query.all()

    return render_template('index.html', rand_tutors=random_tutors, goals=goals_all)


@app.route('/goals/<goal>/')
def goals(goal):
    # get goal for render in template
    client_goal = GOALS[goal].lower()

    # get tutors with chosen goal in desc order from DB
    tutors_query = Tutor.query.filter(Tutor.goals.any(Goal.goal_badge == goal)).\
        order_by(Tutor.rating.desc()).all()

    return render_template('goal.html', client_goal=client_goal, filt_tutors=tutors_query, goal=goal)


@app.route('/profiles/<int:tutor_id>/')
def profiles(tutor_id):
    # get tutor from DB or throwback 404 error
    tutor = db.session.query(Tutor).get_or_404(tutor_id)

    # create dict object from string
    tutor_free = json.loads(tutor.free)

    return render_template('profile.html', tutor=tutor, tutor_free=tutor_free)


@app.route('/request/', methods=['GET', 'POST'])
def render_request():
    # create the form for 'request.html' template
    form = RequestForm()

    # if data WAS sent and is valid
    if request.method == 'POST' and form.validate():
        # get data from the form
        name = form.client_name.data
        phone = form.client_phone.data
        goal = form.goal_buttons.data
        time = form.time_buttons.data

        # create DB instance with client data
        client_data = RequestTutor(name=name, phone=phone, time=time, goal=goal)
        # update DB
        db.session.add(client_data)
        db.session.commit()

        return render_template('request_done.html', name=name, phone=phone, time=time, goal=goal, goal_bages=GOALS)

    # if data WAS NOT sent yet
    return render_template('request.html', form=form)


@app.route('/booking/<int:tutor_id>/<day>/<time>/', methods=['GET', 'POST'])
def booking(tutor_id, day, time):
    # get tutor from DB or throwback 404 error
    tutor = db.session.query(Tutor).get_or_404(tutor_id)

    # create the form
    form = BookingForm()

    # if data WAS sent and is valid
    if request.method == 'POST' and form.validate():
        # get data from the form
        name = form.client_name.data
        phone = form.client_phone.data
        day = form.client_weekday.data
        time = form.client_time.data
        tutor_id = int(form.client_teacher.data)

        # create DB instance with client data
        client_data = Booking(name=name, phone=phone, day=day, time=time, tutor_id=tutor_id)
        # update DB
        db.session.add(client_data)
        db.session.commit()

        return render_template('booking_done.html', name=name, phone=phone,
                               day=day, time=time, picture=tutor.picture)

    # if data WAS NOT sent yet
    return render_template('booking.html', tutor=tutor, day=day, time=time, form=form)


if __name__ == '__main__':
    app.run()
