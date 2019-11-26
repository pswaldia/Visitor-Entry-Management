
from flask_sqlalchemy import SQLAlchemy

class Visitor(db.Model):
  email=db.Column(db.String(30),primary_key=True)
  name=db.Column(db.String(30),nullable=False)
  phone=db.Column(db.String(20),nullable=False)
  checkin_time=db.Column(db.String(20),default=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
  checkout_time=db.Column(db.String(20),default=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
  host_email=db.Column(db.String(30),nullable=False)
  host_name=db.Column(db.String(30),nullable=False)
  host_phone=db.Column(db.String(20),nullable=False)
  def __repr__(self):
    return '<Visitor %r>' % self.email