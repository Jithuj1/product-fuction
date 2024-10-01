import sendgrid
from sendgrid.helpers.mail import Mail
from django.conf import settings

class EmailSender:
    def __init__(self):
        api_key = settings.SENDGRID_API_KEY
        self.from_email = settings.DEFAULT_FROM_EMAIL
        self.client = sendgrid.SendGridAPIClient(api_key=api_key)

    def send_email(self, to_address, subject, content):

        message = Mail(
            from_email=self.from_email,
            to_emails=to_address,
            subject=subject,
            html_content=content  # You can send plain text or HTML content
        )

        try:
            response = self.client.send(message)
            print(f"Email sent with status code: {response.status_code}")
            response_data = {
                "success": True,
                "message": "Email sent successfully"
            }
            return response_data
        
        except Exception as e:
            response_data = {   
                "success": False,
                "message": f"Error sending email: {str(e)}"
            }
            return response_data