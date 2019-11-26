from app import app
from flask import render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

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
visitor=Visitor()

@app.route('/',methods=['POST','GET'])
def index():
  if request.method=='POST':
    visitor_name=request.form['visitor-name']
    visitor_email=request.form['visitor-email']
    visitor_phone=request.form['visitor-phone']
    host_name=request.form['host-name']
    host_email=request.form['host-email']
    host_phone=request.form['host-phone']
    time=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    visitor=Visitor(email=visitor_email, name=visitor_name, phone=visitor_phone, 
                    checkin_time=time,
                    checkout_time=None,
                    host_name=host_name,
                    host_email=host_email,
                    host_phone=host_phone)
    print(visitor_email,visitor_name,visitor_phone,host_email,host_phone,host_name,datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    db.session.add(visitor)
    db.session.commit()
    message = Mail(
    from_email=visitor_email,
    to_emails=host_email,
    subject="Visitor's details",
    html_content='<ol><li>Name:{}</li> <li>Email:{}</li> <li>Phone:{}</li><li>Check-in time : {}</li></ol>'.format(visitor_name,visitor_email,visitor_phone,time))
    try:
      sg = SendGridAPIClient('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')
      response = sg.send(message)
      print(response.status_code, response.body, response.headers)
    except:
      return "Email not sent"
    return redirect('/')
 
  else:
    return render_template("checkin.html")

@app.route('/checkout',methods=['POST','GET'])
def checkout():
  return render_template("checkout.html")

  