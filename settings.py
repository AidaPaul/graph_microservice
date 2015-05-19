__author__ = 'Tymoteusz Paul'

logging_format = '%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s'

redis_server = {
    'host': 'localhost',
    'port': 6379,
}

bottle_server = {
    'host': '0.0.0.0',
    'port': 9191,
    'debug': True,
    'server': 'cherrypy',
}

rest_prefix = 'http://127.0.0.1:%s' % bottle_server['port']
