# django_multi_mailer
Multiple e-mail backends for Django Framework

Written for Django 1.7 and Python 3

How to use it?
##############

In settings.py:
    * Add `'django_multi_mailer'` into INSTALLED_APPS
    * Set the EMAIL_BACKEND variable to `EMAIL_BACKEND = 'django_multi_mailer.backends.MultiEmailBackend'`
    * Set the EMAIL_MULTI variable to `EMAIL_MULTI = [
    {
        'HOST': 'put_your_host_here.com',
        'PORT': 25,
        'USE_SSL': False,
        'USE_TLS': True,
        'TIMEOUT': 120,
        'FAIL_SILENTLY': False,
        'CREDENTIALS': [
            ('first@example.com', 'password'),
            ('second@example.com', 'password'),
            ('third@example.com', 'password'),
            ('fourth@example.com', 'password'),
            ('fifth@example.com', 'password')
        ]
    },
]`
    * That's all, you can now send e-mails using default django send_mail function
    
How to send an e-mail?
######################

`
from django.core.mail import send_mail
subject = 'Email Topic'
content = 'Email Content'

recipient_list = ['recipient@example.com']
send_mail(subject, content, None, recipient_list)
`