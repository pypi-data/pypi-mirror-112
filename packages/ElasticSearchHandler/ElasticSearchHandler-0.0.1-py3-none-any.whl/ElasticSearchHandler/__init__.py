import sys
import json
from os import getenv
from datetime import datetime
from elasticsearch7 import Elasticsearch
from logging import INFO, Logger, Handler, Formatter, basicConfig, getLogger


class ElasticSearchHandler(Handler):
    def __init__(self, level=INFO, index='log', scheme='http',
                 hosts=(getenv('ELASTICSEARCH_SERVICE_HOST', 'localhost'),),
                 port=getenv('ELASTICSEARCH_SERVICE_PORT', 9200),
                 http_auth=None, cert_file=None):
        """

        :param level: logging level (default: logging.INFO)
        :type level: int
        :param index: Elasticsearch index name for log (default: 'log')
        :type index: str
        :param scheme: protocol (default: 'http')
        :type scheme: str
        :param hosts: Elasticsearch hosts (default: environment variable ELASTICSEARCH_SERVICE_HOST or 'localhost' )
        :type hosts: tuple
        :param port: Elasticsearch port (default: environment variable ELASTICSEARCH_SERVICE_PORT or 9200)
        :type port: int
        :param http_auth: authentication data (default: None, example: ('user', 'secret'))
        :type http_auth: tuple
        :param cert_file: path to client certificate (default: None)
        :type cert_file: str

        """
        super().__init__(level=level)
        kwargs = {
            'port': port,
            'scheme': scheme
        }
        if http_auth is not None:
            kwargs['http_auth'] = http_auth
        if cert_file is not None:
            from ssl import create_default_context
            kwargs['ssl_context'] = create_default_context(cafile=cert_file)
        self._es = Elasticsearch(hosts=list(hosts), **kwargs)
        self._es.indices.create(index=index, ignore=400)
        self._index = index
        self._level = level

    def emit(self, record):
        """
        Emit a record.

        :param record Log record
        :type record LogRecord

        """
        try:
            formatted = self.format(record)
            try:
                msg = json.loads(formatted)
            except json.JSONDecodeError:
                msg = formatted
            log_entry = {
                "timestamp": datetime.utcnow(),
                "message": msg
            }
            self._es.index(index=self._index, body=log_entry)
        except Exception as e:
            sys.stderr.write(str(e))
            self.handleError(record)

    def get_elastic_logger(self, logger_name, logging_format):
        """
        Get elasticsearch logger

        :param logger_name: logger name
        :type logger_name: str
        :param logging_format: log format
        :type logging_format: str
        :return: logger
        :rtype: Logger

        """
        basicConfig(level=self._level, format=logging_format)
        logs = getLogger(logger_name)
        handler = self
        handler.setFormatter(Formatter(logging_format))
        logs.addHandler(handler)
        logs.setLevel(level=self._level)
        return logs
