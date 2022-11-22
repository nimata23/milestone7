from venv import create
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from flask_login import LoginManager
from dotenv import load_dotenv

from werkzeug.security import generate_password_hash

db = SQLAlchemy()
DB_NAME = "database.db"
# the location of the csv upload folder
UPLOAD_FOLDER = "./csvs"
load_dotenv()

def create_test_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
    db.init_app(app)

    from .models import User
    create_database(app)

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("postgres", "postgresql", 1)
    
    
    # configure an upload folder for csv uploads
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    db.init_app(app)

    from .models import User, Hawkins
    create_database(app)

    from .views import views
    from .auth import auth
    # from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    # app.register_blueprint(auth, url_prefix='/')



    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app: Flask):
    #if not path.exists('instance/' + DB_NAME):
        

    # use app context in order to initialize properly
    with app.app_context():
        db.create_all()
        populate()
    print('Created Database!')
            

def populate():
# with app.app_context():
    # Users

    from .models import User, Team

    matt = User(
        email = "matt@colby.edu",
        first_name = "Matt",
        last_name = "Cerrato",
        password = generate_password_hash("1234567890", method='sha256'),
        role = "athlete"
    )

    milo = User(
        email = "milo@colby.edu",
        first_name = "Milo",
        last_name = "Lani-Caputo",
        password = generate_password_hash("1234567890", method='sha256'),
        role = "athlete"
    )

    hannah = User(
        email = "hannah@colby.edu",
        first_name = "Hannah",
        last_name = "Soria",
        password = generate_password_hash("1234567890", method='sha256'),
        role = "coach"
    )

    nicole = User(
        email = "nicole@colby.edu",
        first_name = "Nicole",
        last_name = "Matamoros",
        password = generate_password_hash("1234567890", method='sha256'),
        role = "coach"
    )

    anne = User(
        email = "anne@colby.edu",
        first_name = "Anne",
        last_name = "Doctor",
        password = generate_password_hash("1234567890", method='sha256'),
        role = "admin"
    )

    # Teams
    swim = Team(
        name = "mens_swim"
    )
    swim.users += [matt, milo, hannah, nicole]

    tennis = Team(
        name = "womens_tennis"
    )
    tennis.users += [matt, milo, hannah, nicole]


    # Sleep
    # Readiness
    # hawkins
    # nutrition
    # Note

    db.session.add_all([matt, milo, hannah, nicole, swim, tennis, anne])
    db.session.commit()

def drop_database(app):
    with app.app_context():
        db.session.remove()
        db.drop_all()
    print('Dropped Database!')