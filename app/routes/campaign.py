from app import *
from app import db
from app.database import *
from app.forms import *
from flask import render_template, redirect, send_from_directory, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
import sys
from app.routes.openai import summarization, text_generation, image_generation

@app.route('/home', methods=['GET', 'POST'])
@login_required
def index():
    form = newCampaignForm() 
    if form.validate_on_submit():
        links=form.links_Form.data,
        perspective=form.perspective_Form.data,
        summary=summarization(links)
        print('created summary!')
        text_advertisement =text_generation(summary, perspective)
        print('created advertisement text!')
        img_prompt = "Generate an image capturing the spirit of the following text" + text_advertisement
        image_url = image_generation(img_prompt)
        print('generated image!')
        # print(myImage)
        campaign = Campaign(
            user_id=current_user.id,
            name=form.campaignName_Form.data,
            links=form.links_Form.data,
            perspective=form.perspective_Form.data,
            summarization = summary,
            text_generated = text_advertisement,
            image_prompt = img_prompt,
            image_generated = image_url
        )
        db.session.add(campaign)
        db.session.commit()
        return redirect(url_for('viewCampaigns'))
    return render_template('campaign.html', form=form)

@app.route('/viewCampaigns', methods=['GET', 'POST'])
@login_required
def viewCampaigns():
    print("View Campaigns route called")
    all_campaigns = Campaign.query.filter_by(user_id = current_user.id).all()
    campaigns = []
    for campaign in all_campaigns:
        name = campaign.name
        creation_date = campaign.creation_date
        links = campaign.links
        summarization = campaign.summarization
        perspective = campaign.perspective
        text_generated = campaign.text_generated
        image_prompt = campaign.image_prompt
        image_generated = campaign.image_generated
        campaigns.append((name, creation_date, links, summarization, perspective, text_generated, image_prompt, image_generated))
        
    return render_template('viewCampaigns.html', campaigns=campaigns)

#   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#   portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'))
#   campaign_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#   name = db.Column(db.String(1000), nullable=False)
#   creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  
#   links = db.Column(db.String(1000))
#   summarization = db.Column(db.String(1000))
#   perspective = db.Column(db.String(1000))
#   text_generated = db.Column(db.String(1000))
#   image_prompt = db.Column(db.String(1000))
#   image_generated = db.Column(db.String(1000))

# @app.route('/updateCampaign/<int:campaign_id>', methods=['POST'])
# @login_required
# def updateCampaign():
#     form = UpdateCampaignForm() 
        
#     return render_template('viewCampaigns.html', campaigns=campaigns)


# @app.route('/add_campaign', methods=['GET', 'POST'])
# @login_required
# def lateadd():
#     form = CourseForm()
#     if form.validate_on_submit():
#         student = Student.query.filter_by(id=current_user.id).first()
#         course = Course.query.filter_by(crn=form.course_id.data).first()
#         add_request = Request(date=form.date.data,
#                          term=form.term.data,
#                          student_id=student.id,
#                          email=student.email,
#                          course_id=course.crn,
#                          comments=form.comments.data,
#                          approver_id=1, status_id=1,
#                          type = "Late Add")
#         # Assign an approver
#         approver = Approver.query.filter_by(id=course.professor_id).first() 
#         if not approver:
#             flash('No approvers found. Please contact the admin.', 'danger')
#             return redirect(url_for('lateadd'))
        
#         add_request.approver_id = approver.id

#         db.session.add(add_request)
#         db.session.commit()
#         prof_msg, student_msg = request_created(student, course.crn, "n add")
#         subject = 'Late Add Request'
#         msg = Message(subject, recipients=[approver.email ], body = prof_msg)
#         msg2 = Message(subject, recipients=[student.email], body = student_msg)
#         mail.send(msg)
#         mail.send(msg2)
#         flash('Your late add request has been submitted', 'success')
#         return redirect(url_for('lateadd'))
#     return render_template('lateadd.html', title='Late Add Request', form=form)

# @app.route('/update_campaign/<int:request_id>', methods=['POST'])
# @login_required
# def updateRequest(request_id):
#     form = ViewRequestForm()
#     request = Request.query.get(request_id)
    
#     # Pending = 1
#     # Approved = 2
#     # Denied = 3
#     # Returned = 4
#     # Awaiting Registrar Approval = 5

#     if form.validate_on_submit():
#         # Update request status and comments based on the form data
#         student = Student.query.filter_by(email = request.email ).first()
#         print("status: " , request.status_id)
#         if form.approve.data:
#             if request.status_id == 5:
#                 request.status_id = 2
#                 request.approver_id = None
                
#             elif request.status_id == 1:
#                 request.status_id = 5
#                 # update to registrar ID
#                 request.approver_id = 3
#                 approver = Approver.query.filter_by(id = request.approver_id).first()
#                 req_type = " " +request.type
#                 prof_msg, student_msg = request_created(student, request.course_id, req_type)
#                 subject = req_type +' Request'
#                 msg = Message(subject, recipients=[approver.email ], body = prof_msg)
                        
                
#         elif form.deny.data:
#             request.status_id = 3
#             request.approver_id = None

#         request.comments = form.comments.data

#         # Save the changes to the database
#         db.session.commit()
#         course = Course.query.filter_by(crn = request.course_id).first()
#         student_msg = status_change(student, course.crn)
#         subject = 'Status Change'
#         msg = Message(subject, recipients=[student.email], body = student_msg)
#         mail.send(msg)

#         # Redirect the user to the viewRequest page
#         return redirect(url_for('viewRequest'))
#     else:
#         # If the form is not valid, render the requestDetails page with the existing data
#         request = Request.query.get(request_id)
#         student = Student.query.filter_by(id = request.student_id).first()
#         course = Course.query.filter_by(crn = request.course_id).first()
#         status = RequestStatus.query.filter_by(id = request.status_id).first()
#         info = [(student.first_name, student.last_name, student.student_id,str(request.timestamp),request.type, course.subject, course.course, course.section, course.crn, request.term, request.comments, request.id, status.status)]
#         return render_template('requestDetails.html', form=form, request=info)
