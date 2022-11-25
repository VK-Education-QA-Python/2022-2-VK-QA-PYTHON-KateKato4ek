import logging

logger = logging.getLogger('test')

class Logger:
    
    def log_request(self, url):
        logger.info(
            f"""
            ########################
            REQUEST: {url}
            """)

    def log_response(self, response):
        logger.info(
            f"""
            RESPONSE STATUS: {response.status_code}
            RESPONSE HEADERS: {response.headers}
            RESPONSE CONTENT: {response.text}
            
            """)
