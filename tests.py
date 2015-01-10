from django.test import TestCase
from django_multi_mailer.backends import MultiEmailBackend
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
import unittest.mock as mock
import django_multi_mailer


class MultiEmailBackendTestCase(TestCase):
    def setUp(self):
        self.backend = django_multi_mailer.backends.MultiEmailBackend()

        self.credentials = [
            ('a@a.pl', 'abc'),
            ('b@a.pl', 'abc'),
            ('c@a.pl', 'abc'),
            ('d@a.pl', 'abc'),
            ('e@a.pl', 'abc'),
        ]

        settings.EMAIL_MULTI = [
            {
                'HOST': 'smtp.gmail.com',
                'PORT': 587,
                'USE_SSL': True,
                'USE_TLS': True,
                'TIMEOUT': 120,
                'FAIL_SILENTLY': False,
                'CREDENTIALS': self.credentials
            },
        ]

    def test_get_random_server(self):
        """
        Test if first server from queue is returned and then is placed on last position
        """

        self.backend._prepare_settings()

        random_server = self.backend._get_random_server()
        random_server_2 = self.backend._get_random_server()

        #We cannot rely on items in heap, so we must make full cycle of queue and then check if item matches
        for i in range(2, len(self.credentials)):
            self.backend._get_random_server()

        #Strip priority from tuples
        random_server = random_server[:-1]
        random_server_2 = random_server_2[:-1]

        #Get two first items - they should be first ones that we got
        a = self.backend._get_random_server()[:-1]
        b = self.backend._get_random_server()[:-1]

        self.assertTupleEqual(random_server, a)
        self.assertTupleEqual(random_server_2, b)


    def test_send_messages(self):
        subject = 'Topic'
        content = 'Content'

        from_email = 'b@a.pl'
        recipient_list = ['a@a.pl']

        mail = EmailMultiAlternatives(subject, content, from_email, recipient_list,
                                  connection=self.backend)

        #TODO mock open function in backend
        is_sent = self.backend.send_messages([mail])

        #is_sent = send_mail(subject, content, None, recipient_list)

        #print(is_sent)
        self.assertFalse(is_sent)