# Web application built using [Flask](http://flask.palletsprojects.com/en/1.1.x/) as backend.

### Why Flask?
Flask provides simplicity, flexibility, and fine-grained control and is suitable for fast prototyping an app.

### Technology Stack
- Flask
- SQLite Database
- SQLAlchemy
- Bootstrap
- HTML,CSS,Javascript
- External APIs for email and SMS facilities.
  - [Nexmo](https://www.nexmo.com/) for sms
  - [Sendgrid](https://sendgrid.com/) for email

### List of contents

- [Introduction](#introduction)
- [Working](#working)
- [Installation](#installation)
- [Running](#running)


## Introduction
---
[(Back to top)](#list-of-contents)

This Web application provides a facility to manage the entry of visitors. On the frontend part, a visitor enters his information
and host's information he is having an appointment with. This sends an email and SMS to the host informing him about the visitor's
details and his check-in time. After the visit, the visitor performs checkout and receives SMS and email containing information
about his visit, check-in and check-out time.

### User Interface

![img](https://imgur.com/dmK4aKP.jpg) 
 
![img](https://imgur.com/XijkHCh.jpg)
 
## Working
---
[(Back to top)](#list-of-contents)

The step-by-step procedure of the Project:

+ Collection of visitor's and host's information using an interface.
+ Two databases are maintained: one to persist the data throughout and another one to facilitate the checkout facility.
  - [test.db](https://github.com/pswaldia/Visitor-Entry-Management/blob/master/app/test.db) : contains the information received through the interface with email as a primary key. When user checkouts he/she
              enters his/her email which will delete the record associated with the email address after sending email and SMS
              and thus marking the end of a visit.
  - [records.db](https://github.com/pswaldia/Visitor-Entry-Management/blob/master/app/records.db) : contains the information of the visit using check-in timestamp as a key. This database can be queried by the 
                 administrator whenever he wants to extract the list of all the visitors.
+ Email and SMS utility is provided using Sendgrid and Nexmo API respectively.  

*NOTE*
Nexmo API's use is very restricted for Indian demographics (for ex: ) and also free tier does not allow sending of
more than 8-10 SMS and that too is restricted to some numbers. So this facility might not work. On the other hand, email
utility works smooth.

### Screenshots of an email received by both visitor and the host

### Email received by host containing the information of the visitor
![img](https://imgur.com/YU0HDoh.jpg)


### Email received by the visitor containing the complete details of the visit.

![img](https://imgur.com/nKwT6zF.jpg)


*NOTE*
The emails received have been marked as SPAM as the email address used to send mail is not a trusted one (xyz@gmail.com).

## Installation
---
[(Back to top)](#list-of-contents)

These instructions assume you have `git` installed for cloning and pushing changes to the remote repository.

1. Clone the repository, and navigate to the downloaded folder. Follow the below commands.
```
git clone https://github.com/pswaldia/Visitor-Entry-Management
cd Visitor-Entry-Management
```

2. Creating a python virtual environment using virtualenv package using the following lines of code.

NOTE: For this step make sure you have virtualenv package installed.

```
virtualenv venv
source venv/bin/activate

```

3. Install a few required python packages, which are specified in the [requirements.txt](https://github.com/pswaldia/Visitor-Entry-Management/blob/master/requirements.txt) file.
```
pip3 install -r requirements.txt

```

## Running
---
[(Back to top)](#list-of-contents)

Run the following code from the top-level directory:
```shell
flask run
```
Now copy the URL of the local host that will appear on your terminal and run it in a browser.

 
