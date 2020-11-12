from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

#Honestly, I don't even know what this is used for, I just saw it at some point and added it
SECRET_KEY =  'kkck_wey'

db = SQLAlchemy()

app.config["SECRET_KEY"] = "CoronavirusWillKillUsAll2020!!"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://s2gadmin@s2g-database-iops:EMaaS2020!!@s2g-database-iops.postgres.database.azure.com/s2g-db"

db.init_app(app)
