from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_submission_notification(submission_type, data):
    """
    Sends confirmation email to submitter and alert email to admin.
    submission_type: 'volunteer', 'contact', 'partnership'
    data: dict containing submission details
    """
    submitter_email = data.get('email')
    full_name = data.get('full_name', data.get('contact_person', 'User'))
    
    # 1. Email to Submitter
    subject_user = f"Thank you for your {submission_type} submission"
    body_user = f"Hello {full_name},\n\nWe have received your {submission_type} form and our team will review it shortly.\n\nThank you for reaching out to Agropastoralists Development Consortium."
    
    # 2. Email to Admin
    subject_admin = f"New {submission_type.capitalize()} Submission: {full_name}"
    
    details_str = "\n".join([f"{k.replace('_', ' ').capitalize()}: {v}" for k, v in data.items() if v])
    body_admin = f"A new {submission_type} has been submitted.\n\nDetails:\n{details_str}"

    try:
        # Send to User
        if submitter_email:
            send_mail(
                subject_user,
                body_user,
                settings.DEFAULT_FROM_EMAIL,
                [submitter_email],
                fail_silently=False,
            )
            
        # Send to Admin
        if settings.ADMIN_EMAIL:
            send_mail(
                subject_admin,
                body_admin,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
    except Exception as e:
        logger.error(f"CRITICAL EMAIL FAILURE for {submission_type}: {str(e)}")
        # We don't re-raise because we want the database record to persist
        # even if the email fails, but the log will now show the EXACT reason.
