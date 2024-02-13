from flask_mail import Mail, Message
from app import *
from app.database import *
from app.forms import *
from os import environ

# # Specify mail environment variables
MAIL_USERNAME = environ.get('MAIL_USERNAME')
MAIL_APP_PASSWORD = environ.get('MAIL_APP_PASSWORD')
MAIL_SENDER_NAME = environ.get('MAIL_SENDER_NAME')

# Setup mail client
app.config.update(
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 465,
        MAIL_USE_TLS = False,
        MAIL_USE_SSL = True,
        MAIL_USERNAME = MAIL_USERNAME,
        MAIL_PASSWORD = MAIL_APP_PASSWORD,
        MAIL_DEFAULT_SENDER = (MAIL_SENDER_NAME, MAIL_USERNAME)
        )

# mail send
mail = Mail(app)

# Replace these values with your email credentials
# Create project-specific email, get API email key
EMAIL_USER = 'jonathanwarren2022@gmail.com'
EMAIL_PASSWORD = ''

def send_mail(addr, msg):
    recipient = addr
    subject = 'Test Flask email'
    message = Message(subject, recipients=[recipient], body = msg)
    mail.send(message)
    
# email notification of sign-up
# ACCT_EMAIL = email
# try:
#     server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#     server.login(EMAIL_USER, EMAIL_PASSWORD)

#     body = f"Subject: Account Created\n\nWelcome to the Finance Tracker, {first_name} {last_name}! Your account information is listed below: \nName: {first_name} {last_name}\nEmail: {email}"
#     server.sendmail(EMAIL_USER, ACCT_EMAIL, body)

#     server.quit()

# except Exception as e:
#     return f"Error: {e}" 

# def request_created(student, crn, type):
#     course = Course.query.filter_by(crn=crn).first()
#     approver = Approver.query.filter_by(id=course.professor_id).first()
#     prof_msg = f"Hello {approver.title}, {student.first_name} {student.last_name} has submitted a{type} request for {course.subject} {course.course}-{course.section}."
#     student_msg = f"Hello {student.first_name} {student.last_name}, your {type} request for {course.subject} {course.course}-{course.section} has been sent to {approver.title}."
#     return prof_msg, student_msg

# def status_change(student, crn):
#     course = Course.query.filter_by(crn=crn).first()
#     approver = Approver.query.filter_by(id=course.professor_id).first()
#     student_msg = f"Hello {student.first_name} {student.last_name}, your request for {course.subject} {course.course}-{course.section} has been reviewed and the status has changed."
#     return student_msg