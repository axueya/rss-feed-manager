import logging
from pythonjsonlogger.jsonlogger import JsonFormatter
from kafka import KafkaProducer


class KafkaLoggingHandler(logging.Handler):

    def __init__(self, topic, servers):
        logging.Handler.__init__(self)
        if isinstance(servers, (list, tuple)):
            self.servers = servers
        else:
            self.servers = servers.split(',')

        print(self.servers)
        self.producer = KafkaProducer(bootstrap_servers=self.servers,
                                      max_block_ms=5)
        self.topic = topic
        print(self.topic)

    def emit(self, record):
        try:
            msg = self.format(record)
            self.producer.send(self.topic, bytes(msg, encoding="utf8"))
            print(msg)

        except Exception:
            self.handleError(record)


class KafkaLogging(object):
    base_fields = '%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'
    topic_key = 'KAFKA_LOGGING_TOPIC'
    servers_key = 'KAFKA_LOGGING_SERVERS'

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def _get_handler(self, config):
        return KafkaLoggingHandler(topic=config[self.topic_key],
                                   servers=config[self.servers_key])

    def _get_formatter(self):
        return JsonFormatter(self.base_fields, datefmt="%Y-%m-%d %H:%M:%S")

    def init_app(self, config):
        config[self.topic_key] = 'my_topic'
        config[self.servers_key] = '{}:{}'.format(config['KAFKA_HOST'], config['KAFKA_PORT'])
        if self.topic_key in config and self.servers_key in config:
            handler = self._get_handler(config)
            handler.setLevel(logging.INFO)
            handler.setFormatter(self._get_formatter())
            config['logger'].addHandler(handler)
            config['logger'].setLevel(logging.INFO)


config = {}
config['logger'] = logging.getLogger()
config['KAFKA_HOST'] = 'localhost'
config['KAFKA_PORT'] = 9092
kafka_logging = KafkaLogging()
kafka_logging.init_app(config)


def search_es_by_keyword(user_id, keyword):
    config['logger'].info({'message': keyword, 'id': user_id})


def search_es_by_id(user_id, newsid):
    config['logger'].info({'message': newsid, 'id': user_id})


search_es_by_id('123', 'www.baidu.com')
search_es_by_keyword('456', 'happy day!')
