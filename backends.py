from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings
import heapq


class PriorityQueue():
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]


class MultiEmailBackend(EmailBackend):
    _queue = PriorityQueue()

    def _prepare_settings(self):
        """ Prepares queue with servers """

        servers = getattr(settings, 'EMAIL_MULTI', [])
        for server in servers:
            for credential in server['CREDENTIALS']:
                res = (server['HOST'], server['PORT'], server['USE_SSL'], server['USE_TLS'], server['TIMEOUT'],
                       server['FAIL_SILENTLY'], credential[0], credential[1], 0)

                self._queue.push(res, 0)


    def _get_random_server(self):
        """ Gets first server from queue (longest not used one) """

        server = self._queue.pop()

        self.host = server[0]
        self.port = server[1]
        self.use_ssl = server[2]
        self.use_tls = server[3]
        self.timeout = server[4]
        self.fail_silently = server[5]
        self.username = server[6]
        self.password = server[7]

        new_priority = server[8] + 1

        #Increment use count
        new_server = (server[0], server[1], server[2], server[3], server[4], server[5], server[6], server[7],
                      new_priority)

        #And put back on the queue (on the last place)
        self._queue.push(new_server, new_priority)

        return new_server


    def send_messages(self, email_messages):
        """
        Sends one or more EmailMessage objects using different credentials and returns the number of email
        messages sent.
        """

        if not email_messages:
            return
        with self._lock:
            self._prepare_settings()

            num_sent = 0
            for message in email_messages:
                #Prepare from name & from email
                message.from_email = '%s <%s>' % (settings.EMAIL_SETTINGS['FROM_NAME'], settings.EMAIL_SETTINGS['FROM'])
                self._get_random_server()

                new_conn_created = self.open()
                if not self.connection:
                    # We failed silently on open().
                    # Trying to send would be pointless.
                    continue

                sent = self._send(message)
                if sent:
                    num_sent += 1

                if new_conn_created:
                    self.close()

        return num_sent