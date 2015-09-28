import logging

def configureLog(dir):

    LOGGER = logging.getLogger(__name__)
    hdlr = logging.FileHandler(dir + '/log/nao-elastic-river-rabbitmq.log')
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    LOGGER.addHandler(hdlr)
    ch.setFormatter(formatter)
    LOGGER.addHandler(ch)
    LOGGER.setLevel(logging.INFO)

    return LOGGER
