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
    db.session.add(visitor)
    db.session.commit()
    message = Mail(
    from_email='xyz@gmail.com',      #this is company's mail id , through which the email will be sent
    to_emails=host_email,
    subject="Visitor's details:",
    html_content='<ol><li>Name:{}</li> <li>Email:{}</li> <li>Phone:{}</li><li>Check-in time : {}</li></ol>'.format(visitor_name,visitor_email,visitor_phone,time))
    try:
      sg = SendGridAPIClient(os.getenv("SENDGRID_SECRET"))
      response = sg.send(message)
      print(response.status_code, response.body, response.headers)
      return redirect('/')
    except:
      return redirect('/')
 
  else:
    return render_template("checkin.html")

@app.route('/checkout',methods=['POST','GET'])
def checkout():
  exists=-1
  if request.method=='POST':
    email_id=request.form['visitor-email']
    exists = visitor.query.filter_by(email=email_id).count()
    if exists>0:
      visitor.query.filter_by(email=email_id).first().checkout_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
      n=visitor.query.filter_by(email=email_id).first().name
      p=visitor.query.filter_by(email=email_id).first().phone
      ci=visitor.query.filter_by(email=email_id).first().checkin_time
      co=visitor.query.filter_by(email=email_id).first().checkout_time
      message = Mail(
      from_email='xyz@gmail.com',     #this is company's mail id , through which the email will be sent
      to_emails=email_id,
      subject="Your visit details:",
      html_content='<ol><li>Name:{}</li> <li>Email:{}</li> <li>Phone:{}</li><li>Check-in time:{}</li><li>Check-out time:{}</li></ol>'.format(n,email_id,p,ci,co))
      visitor.query.filter_by(email=email_id).delete()
      db.session.commit()
      try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_SECRET"))
        response = sg.send(message)
        print(response.status_code, response.body, response.headers)
        return redirect('/')
      except:
        return redirect('/')
    else:
      exists=0
      render_template("checkout.html",exists=exists)
  return render_template("checkout.html",exists=exists)

  