from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpRequest


class UserPasswordRecovery:

    def __init__(self, request: HttpRequest, email: str):
        self.email = email
        self.request = request

    def execute(self):
        form = PasswordResetForm({"email": self.email})
        from_email = self.get_from_email()
        remember_password = self.get_remember_password_url()
        if form.is_valid():
            opts = {
                'use_https': self.request.is_secure(),
                'token_generator': PasswordResetTokenGenerator(),
                'from_email': from_email,
                'email_template_name': 'emails/password_recovery/email.html',
                'subject_template_name': 'emails/password_recovery/subject.txt',
                'request': self.request,
                'html_email_template_name': 'emails/password_recovery/email.html',
                'extra_email_context': {'REMEMBER_PASSWORD_URL': remember_password},
            }
            form.save(**opts)

    def get_remember_password_url(self):
        return getattr(settings, 'REMEMBER_PASSWORD_URL', 's/accounts/reset')


    def get_from_email(self):
        return getattr(settings, 'EMAIL_FROM', 'localhost@localhot.com')

