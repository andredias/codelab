from flask_mail import Message
from logging import Handler, NOTSET


class MailHandler(Handler):

    def __init__(self, async_mail_func, subject, sender, recipients, level=NOTSET):
        Handler.__init__(self, level)
        self.async_mail_func = async_mail_func
        self.subject = subject
        self.sender = sender
        self.recipients = recipients

    def emit(self, record):
        body = self.format(record)
        message = Message(
            subject=self.subject,
            sender=self.sender,
            recipients=self.recipients,
            body=body,
        )
        self.async_mail_func(message)
        return
