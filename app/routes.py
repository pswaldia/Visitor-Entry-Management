from app import app
from flask import render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

import nexmo

client = nexmo.Client(key=os.getenv("NEXMO_KEY"), secret=os.getenv("NEXMO_SECRET"))


from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
app.config['SQLALCHEMY_BINDS']={'record':'sqlite:///records.db'}

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

class Record(db.Model):
  __bind_key__='record'
  checkin_time_r=db.Column(db.DateTime(),primary_key=True,default=datetime.utcnow())
  email_r=db.Column(db.String(30),nullable=False)
  name_r=db.Column(db.String(30),nullable=False)
  phone_r=db.Column(db.String(20),nullable=False)
  host_email_r=db.Column(db.String(30),nullable=False)
  host_name_r=db.Column(db.String(30),nullable=False)
  host_phone_r=db.Column(db.String(20),nullable=False)
  def __repr__(self):
    return '<Visitor %r>' % self.email_r

record=Record()

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
    record=Record(
                    checkin_time_r=datetime.utcnow(),
                    email_r=visitor_email, 
                    name_r=visitor_name,      
                    phone_r=visitor_phone, 
                    host_name_r=host_name,
                    host_email_r=host_email,
                    host_phone_r=host_phone)
    present=visitor.query.filter_by(email=visitor_email).count()
    print(present)
    if present==0:
      db.session.add(visitor)
      db.session.commit()
      db.session.add(record)
      db.session.commit()
      message = Mail(
      from_email='xyz@gmail.com',      #this is company's mail id , through which the email will be sent
      to_emails=host_email,
      subject="Visitor's details:",
      html_content='<ol><li>Name:{}</li> <li>Email:{}</li> <li>Phone:{}</li><li>Check-in time : {}</li></ol>'.format(visitor_name,visitor_email,visitor_phone,time))
      try:
        client.send_message({
          'from': 'Nexmo',
          'to': host_phone,
          'text': """Name:{}
                     Email:{}
                     Phone:{}
                     Checkin-time:{}
                  """.format(visitor_name,visitor_email,visitor_phone,time),
         })
        sg = SendGridAPIClient(os.getenv("SENDGRID_SECRET"))
        response = sg.send(message)
        print(response.status_code, response.body, response.headers)
        return redirect('/')
      except:
        return redirect('/')
    else:
        return render_template("checkin.html",present=1) 
  else:
    return render_template("checkin.html",present=-1)

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
      hn=visitor.query.filter_by(email=email_id).first().host_name
      message = Mail(
      from_email='xyz@gmail.com',     #this is company's mail id , through which the email will be sent
      to_emails=email_id,
      subject="Your visit details:",
      html_content='<ol><li>Name:{}</li> <li>Email:{}</li> <li>Phone:{}</li><li>Check-in time:{}</li><li>Check-out time:{}</li><li>Host Name:{}</li></ol>'.format(n,email_id,p,ci,co,hn))
      visitor.query.filter_by(email=email_id).delete()
      db.session.commit()
      try:
        client.send_message({
          'from': 'Nexmo',
          'to': p,
          'text': """Name:{}
                     Email:{}
                     Phone:{}
                     Checkin-time:{}
                     Checkout-time:{}
                     Host-Name:{}
                  """.format(visitor_name,visitor_email,visitor_phone,ci,co,hn),
         })
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

  