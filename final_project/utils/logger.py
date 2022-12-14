import logging

class Logger:
    logger = logging.getLogger('test')
    
    def log_request(self, url, expected_status=200):
        self.logger.info(
            f"""
            ########################
            REQUEST: {url}
            EXPECTED STATUS: {expected_status}
            """)

    def log_response(self, response):
        self.logger.info(
            f"""
            RESPONSE STATUS: {response.status_code}
            RESPONSE HEADERS: {response.headers}
            RESPONSE CONTENT: {response.text}
            
            """)
