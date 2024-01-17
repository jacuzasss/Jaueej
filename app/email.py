from app.models import User, Email
from datetime import datetime
from flask import render_template, current_app, url_for
from flask_ezmail.message import Message
import logging
from markdown import Markdown
from threading import Thread
from urllib.parse import urlencode


def send_async_email(app, msg):
    # sends a single email asyncronously
    with app.app_context():
        mail = Email.query.first()
        mail.send(msg)


def send_async_bulkmail(app, msg, users):
    # accepts user list and message, sending msg to all paid users
    with app.app_context():
        mail = Email.query.first()
        try:
            with mail.connect() as conn:
                for user in users:
                    if user.expiration <= datetime.today():
                        break
                    msg.recipients = [user.email]
                    conn.send(msg)
        except Exception:
            logging.exception('Exception in send_async_bulkmail')
            raise


def send_email(subject, sender, recipients, text_body, html_body):
    # composes a single email and passes it to send_async_email fn
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(
        target=send_async_email,
        args=(current_app._get_current_object(), msg)).start()


def send_reminder_emails(app, reminder_set):
    '''
    Takes a list of users about to expire, and emails them fresh
    payment links that direct to BTCPay.
    '''
    if not reminder_set:
        return None
    with app.app_context():
        mail = Email.query.first()
        try:
            site = app.config['BLOGGING_SITENAME']
            with mail.connect() as conn:
                for user in reminder_set:
                    dict = {}
                    dict['username'] = user.username
                    params = urlencode(dict)
                    url = str(url_for('main.create_invoice'))\
                        + '?' + str(params)
                    expires = user.expiration.date()
                    msg = Message(
                        f'{site} Renewal',
                        sender=mail.default_sender,
                        recipients=[user.email],
                        body=render_template(
                            'email/reminder.txt',
                            site=site,
                            user=user,
                            url=url,
                            expires=expires,
                        ),
                        html=None
                    )
                    conn.send(msg)
        except Exception:
            logging.exception('Exception in send_reminder_emails')
            raise


def send_failed_emails(app, failed_list, declined_list):
    '''
    Takes a list of users whose credit card renewals failed via
    Square, and emails them asking to update their credit card.
    '''
    if not failed_list and not declined_list:
        return None
    with app.app_context():
        mail = Email.query.first()
        site = app.config['BLOGGING_SITENAME']
        url = url_for('main.support')
        with mail.connect() as conn:
            for user in failed_list:
                expires = user.expiration.date()
                msg = Message(
                    f'{site} Subscription Update',
                    sender=mail.default_sender,
                    recipients=[user.email],
                    body=render_template(
                        'email/reminder_cc.txt',
                        site=site,
                        user=user,
                        url=url,
                        expires=expires,
                    ),
                    html=None
                )
                conn.send(msg)
            for user in declined_list:
                expires = user.expiration.date()
                msg = Message(
                    f'{site} Card Declined',
                    sender=mail.default_sender,
                    recipients=[user.email],
                    body=render_template(
                        'email/cc_declined.txt',
                        site=site,
                        user=user,
                        url=url,
                        expires=expires,
                    ),
                    html=None
                )
                conn.send(msg)


def send_bulkmail(subject, sender, users, text_body, html_body):
    # composes an email message and sends ti to send_async_bulkmail
    msg = Message(subject, sender=sender)
    msg.body = text_body
    msg.html = html_body
    Thread(
        target=send_async_bulkmail,
        args=(current_app._get_current_object(), msg, users)).start()


def send_password_reset_email(user):
    # emails user a token to reset password
    token = user.get_reset_password_token()
    mail = Email.query.first()
    send_email(
        'Password Reset',
        sender=mail.default_sender,
        recipients=[user.email],
        text_body=render_template('email/reset_password.txt',
                                  user=user, token=token),
        html_body=None
    )


def email_post(post):
    '''
    Takes a blog post, uses the Markdown engine to render it to HTML,
    then creates an email message from the HTML. The msg is then passed
    to send_bulkmail function.
    '''
    mail = Email.query.first()
    try:
        markdown = Markdown()
        post['rendered_text'] = markdown.convert(post['text'])
        html_body = render_template(
            'email/email_post.html',
            post=post,
        )
        text_body = render_template(
            'email/email_post.txt',
            post=post,
        )
        site = current_app.config.get('BLOGGING_SITENAME')
        users = User.query.filter_by(mail_opt_out=False).all()
        send_bulkmail(
            f'New Update from {site}',
            sender=mail.default_sender,
            users=users,
            html_body=html_body,
            text_body=text_body
        )
    except Exception:
        logging.exception('Exception in email_post')
        raise
