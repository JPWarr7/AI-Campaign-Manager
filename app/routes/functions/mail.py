# from app import *
from app.database import *
from app.forms import *
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from base64 import urlsafe_b64encode
from app import mail_client, MAIL_USERNAME

def create_message(address, msg, subject):
    """
    Create a MIME message to be sent wtih the send_message() function.

    Parameters:
        address (str): Email address of the recipient.
        msg (str): Content of the email.
        subject (str): Subject of the email.

    Returns:
        dict: A dictionary representing the MIME message.
    """
    message = MIMEText(msg)
    message["to"] = address
    message["from"] = MAIL_USERNAME
    message["subject"] = subject
    raw_message = urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    return {"raw": raw_message}

def send_message(mail_client, message):
    """
    Send an email message using the provided mail client.

    Parameters:
        mail_client: An email client object capable of sending messages.
        message (dict): A dictionary representing the message to be sent.

    Returns:
        dict: Information about the sent message.
    """
    try:
        message = (
            mail_client.users()
            .messages()
            .send(userId="me", body=message)
            .execute()
        )
        return message
    
    except HttpError as error:
        print("An error occurred: %s" % error)

def account_creation_notification(user):
    """
    Sends an email notification to the user upon successful account creation by 
    generating a body for an email to be converted to a MIME message using 
    the create_message() function and sent using the send_message() function.

    Parameters:
        user: An object representing the user whose account was created.
    """
    address = user.email
    user_msg = f'''Hello {user.first_name} {user.last_name}, your account for the CampAIgn Manager has been successfully created! 
    \n User Information: 
    \n Username: {user.username} 
    \n Email Address: {user.email} 
    '''
    message = create_message(address, user_msg, subject='Welcome to the CampAIgn Manager!')
    send_message(mail_client, message)

def password_change_notification(user):
    address = user.email
    user_msg = f'''Hello {user.first_name} {user.last_name}, your account password for the CampAIgn Manager has changed. Please 
    try to log in using your user credentials.   
    \n User Information: 
    \n Username: {user.username} 
    \n Email Address: {user.email} 
    '''
    message = create_message(address, user_msg, subject='Password Changed Successfully')
    send_message(mail_client, message)
    
def campaign_creation_notification(user, campaign):
    """
    Sends an email notification to the user upon successful campaign creation by 
    generating a body for an email to be converted to a MIME message using 
    the create_message() function and sent using the send_message() function.

    Parameters:
        user: An object representing the user who created the campaign.
        campaign: An object representing the campaign which was created.
    """
    address = user.email
    user_msg = f'''Hello {user.username}, a new Campaign has been added to your account at {campaign.creation_date}. 
    \n Campaign information is included below. 
    \n {campaign.name} 
    \n Links provided: {campaign.links} 
    \n Summarization generated: {campaign.summarization} 
    \n Perspective provided: {campaign.perspective} 
    \n Advertisement text generated: {campaign.text_generated} 
    \n Image prompt provided: {campaign.image_prompt} 
    \n Image generated: {campaign.image_generated} 
    '''
    message = create_message(address, user_msg, subject='Campaign Creation Successful!')
    send_message(mail_client, message)
    
def campaign_edit_notification(user, old_campaign, new_campaign):
    """
    Sends an email notification to the user upon successful campaign edit by 
    generating a body for an email to be converted to a MIME message using 
    the create_message() function and sent using the send_message() function.

    Parameters:
        user: An object representing the user who created the campaign.
        old_campaign: An object representing the old campaign, prior to editing
        new_campaign: An object representing the new campaign which was generated 
        through editing the old_campaign.
    """
    address = user.email
    user_msg = f'''Hello {user.username}, your Campaign has been successfully edited at {new_campaign.creation_date}. 
    \n Changes to Campaign information are included below. 
    \n {old_campaign.name} -> {new_campaign.name} 
    \n Links provided: 
    \n {old_campaign.links} 
    \n Changes -> 
    \n {new_campaign.links} 
    \n Summarization generated: 
    \n {old_campaign.summarization} 
    \n Changes -> 
    \n {new_campaign.summarization} 
    \n Perspective provided: 
    \n {old_campaign.perspective} 
    \n Changes ->
    \n {new_campaign.perspective} 
    \n Advertisement text generated: 
    \n {old_campaign.text_generated} 
    \n Changes -> 
    \n {new_campaign.text_generated}  
    \n Image prompt provided: 
    \n {old_campaign.image_prompt}   
    \n Changes -> 
    \n {new_campaign.image_prompt}  
    \n Image generated: 
    \n {old_campaign.image_generated} 
    \n Changes -> 
    \n {new_campaign.image_generated} 
    '''
    message = create_message(address, user_msg, subject='Campaign Edited Successfully!')
    send_message(mail_client, message)
    
def portfolio_creation_notification(user, portfolio):
    """
    Sends an email notification to the user upon successful portfolio creation by 
    generating a body for an email to be converted to a MIME message using 
    the create_message() function and sent using the send_message() function.

    Parameters:
        user: An object representing the user who created the campaign.
        portfolio: An object representing the portfolio which was created.
    """
    address = user.email
    user_msg = f'''Hello {user.username}, a new Portfolio has been added to your account at {portfolio.creation_date}. 
    \n Portfolio information is included below. 
    \n {portfolio.name} 
    '''
    message = create_message(address, user_msg, subject='Portfolio Creation Successful!')
    send_message(mail_client, message)
    
def portfolio_edit_notification(user, old_name, portfolio):
    """
    Sends an email notification to the user upon successful portfolio edit by 
    generating a body for an email to be converted to a MIME message using 
    the create_message() function and sent using the send_message() function.

    Parameters:
        user: An object representing the user who created the campaign.
        old_name: A string representing the old portfolio's name 
        new_portfolio: An object representing the new portfolio which was generated 
        through editing the original portfolio.
    """
    address = user.email
    user_msg = f'''Hello {user.username}, your Portfolio has been successfully edited. 
    \n Changes to Portfolio information are included below. 
    \n {old_name} -> {portfolio.name} 
    '''
    message = create_message(address, user_msg, subject='Portfolio Edited Successfully!')
    send_message(mail_client, message)
    