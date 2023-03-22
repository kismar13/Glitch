from datetime import datetime

from flask_login import login_user, LoginManager
from sqlalchemy import select
from data.jobs import Jobs
from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
import views.jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars_explorer.db")
    app.register_blueprint(views.jobs.blueprint)
    app.run()
    # session = db_session.create_session()
    # user = User()
    # user.surname = 'Sco'
    # user.name = 'Rid'
    # user.age = 22
    # user.position = 'captain'
    # user.speciality = 'research engineer'
    # user.address = 'module_2'
    # user.email = 'sco_chief@mars.org'
    # user.set_password('123')
    # user.modified_date = datetime.now()
    # session.add(user)
    # session.commit()


@app.route("/")
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    users = session.query(User).all()
    names = {name.id: (name.surname, name.name) for name in users}
    return render_template("index.html", jobs=jobs, names=names)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


main()
