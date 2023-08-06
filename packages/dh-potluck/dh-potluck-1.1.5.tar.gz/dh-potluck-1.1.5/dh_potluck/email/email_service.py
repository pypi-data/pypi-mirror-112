from typing import Dict, List

from dh_potluck.email.mandrill_email_client import MandrillEmailClient


class EmailService(object):
    _email_client: MandrillEmailClient = None

    @classmethod
    def _get_email_client(cls):
        if not cls._email_client:
            cls._email_client = MandrillEmailClient()
        return cls._email_client

    @classmethod
    def send_email_template(
        cls,
        recipient_email: str,
        recipient_name: str,
        template_name: str,
        template_vars: List[Dict[str, str]],
        subject: str = None,
    ) -> None:
        try:
            cls._get_email_client().send_email_template(
                recipient_email, recipient_name, template_name, template_vars, subject=subject
            )
        except Exception as e:
            raise EmailServiceException(
                message=f'Error occurred while sending email template: {str(e)}'
            )

    @classmethod
    def send_email_html(
        cls, recipient_email: str, recipient_name: str, subject: str = None, html: str = None
    ) -> None:
        try:
            cls._get_email_client().send_email_html(
                recipient_email, recipient_name, subject=subject, html=html
            )
        except Exception as e:
            raise EmailServiceException(
                message=f'Error occurred while sending html email: {str(e)}'
            )


class EmailServiceException(Exception):
    def __init__(self, message: str = 'Error occurred while sending email.') -> None:
        self.message = message
        super().__init__(self.message)
