# vim: tabstop=4 shiftwidth=4 softtabstop=4
import logging
import uuid
import sys

import contrib # adds contrib to the path
import anyjson

from carrot import connection
from carrot import messaging

import calllib

_log = logging.getLogger('ampqlib')
_log.setLevel(logging.WARN)

def generic_response(message_data, message):
    _log.debug('response %s', message_data)
    message.ack()
    sys.exit(0)

def send_message(topic, message, wait=True):
    msg_id = uuid.uuid4().hex
    message.update({'_msg_id': msg_id})
    _log.debug('topic is %s', topic)
    _log.debug('message %s', message)

    if wait:
        consumer = messaging.Consumer(connection=calllib.Connection.instance(),
                                      queue=msg_id,
                                      exchange=msg_id,
                                      auto_delete=True,
                                      exchange_type="direct",
                                      routing_key=msg_id)
        consumer.register_callback(generic_response)

    publisher = messaging.Publisher(connection=calllib.Connection.instance(),
                                    exchange="nova",
                                    exchange_type="topic",
                                    routing_key=topic)
    publisher.send(message)
    publisher.close()

    if wait:
        consumer.wait()
    
    
if __name__ == "__main__":
    send_message(sys.argv[1], anyjson.deserialize(sys.argv[2]))
