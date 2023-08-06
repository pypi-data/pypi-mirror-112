# ElasticSearchHandler

Standard logging handler module for sending logs to Elasticsearch.


How to install
--------------

* `pip install git+git://github.com/oleglpts/ElasticSearchHandler.git` or
* `pip install ElasticSearchHandler`


Example:
--------

    import json
    import logging
    from os import uname
    from datetime import datetime
    from ElasticSearchHandler import ElasticSearchHandler
    
    
    def log_json(text, comment=None):
        host = uname()
        log_entry = {
            "os": host[0],
            "host": host[1],
            "kernel": host[2],
            "build": host[3],
            "platform": host[4],
            "text": text
        }
        if comment is not None:
            log_entry['comment'] = comment
        logger.info(json.dumps(log_entry))
    
    
    if __name__ == '__main__':
        logging.getLogger('urllib3').setLevel(logging.ERROR)
        logging.getLogger('elasticsearch').setLevel(logging.ERROR)
        log_format = '{"level": "%(levelname)s", "time": "%(asctime)s", "process": "%(process)d", ' \
                     '"thread": "%(thread)d", "name": "%(name)s", "data": %(message)s}'
        other_log_format = '%(levelname)-10s|%(asctime)s|%(process)d|%(thread)d| %(name)s --- %(message)s'
        logger = ElasticSearchHandler(
            level=logging.INFO, index='test-index').get_elastic_logger('test-logger', log_format)
        other_logger = ElasticSearchHandler(
            level=logging.INFO, index='test-index-other').get_elastic_logger('test-logger-other',
                                                                             other_log_format)
        for _ in range(5):
            other_logger.info('Hello, world')
            log_json(f"message {datetime.now().strftime('%d-%m-%Y %H:%M:%S%Z')}")
        for _ in range(5):
            other_logger.info('Hello, world!')
            log_json(f"message {datetime.now().strftime('%d-%m-%Y %H:%M:%S%Z')}", comment='comment')

Requirements
------------

* elasticsearch7
