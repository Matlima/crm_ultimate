from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

from uploads import *
from view.views_user import *
from view.views_login import *
from view.views_customer import *
from view.views_activity import *
from view.views_prospect import *
from view.views_plans import *
from view.views_portfolio import *
from view.views_proposal import *
from view.views_portfolio_user import *
from view.views_reports import *

if __name__ == '__main__':
    app.run(debug=True)