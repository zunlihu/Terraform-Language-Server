import logging

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    fh = logging.FileHandler('generateJSON.log')
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(handler)
    return logger