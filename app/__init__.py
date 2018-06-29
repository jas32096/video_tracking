from flask import Flask
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy import Column, DateTime, BigInteger
from flask_potion import Api, fields
from flask_cors import CORS

from datetime import datetime, date

class TimedModel(Model):
    id         = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return "<{} #{}>".format(self.__class__.__name__, self.id)

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app, model_class=TimedModel)
CORS(app, expose_headers=['X-Total-Count', 'Link', 'Date'])

from app.resources import VideoResource, ViewResource, OverrideManger

API = Api(app, default_manager=OverrideManger)
API.add_resource(ViewResource)
API.add_resource(VideoResource)
