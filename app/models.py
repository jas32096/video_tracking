from app import db

class View(db.Model):
    __tablename__ = 'views'

    ip          =  db.Column(db.String)
    user_agent  =  db.Column(db.String)
    video_id    =  db.Column(db.BigInteger, db.ForeignKey('videos.id'), nullable=False)
    video = db.relationship('Video', backref=db.backref('views', lazy='dynamic', cascade='delete'), uselist=False)

class Video(db.Model):
    __tablename__ = 'videos'

    name       =  db.Column(db.String, index=True, nullable=False)
    brand      =  db.Column(db.String, nullable=False)
    published  =  db.Column(db.Date, nullable=False)

    count = db.column_property(db.select([db.func.count(View.id)]).where(db.text('views.video_id=videos.id')))
