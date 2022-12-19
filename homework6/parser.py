import re

class Parser:
    def __init__(self, path):
        self.path = path
        
        self.requests = []
        self.uniq_requests = {}
        
    def parse_log(self, log):
        pattern = (
            r'(?P<remote_addr>[.\d]*) - (?P<remote_user>.*) \[(?P<time_local>.*)] ' +
            r'\"(?P<request>.*)\" (?P<response_status>\d\d\d) (?P<bytes_sent>\d*|-) ' +
            r'\"(?P<http_referer>.*)\" \"(?P<http_user_agent>.*)\" \"(?P<gzip_ratio>.*)\"'
        )
    
        return re.search(pattern, log).groupdict()
    
    def parse_request(self, request):
        pattern = r'(?P<method>.*) (?P<url>\S*) (?P<headers>.*)'
    
        return re.search(pattern, request).groupdict()
    
    def parse_log_file(self):
        with open(self.path, 'r') as f:
            for log in f:
                parsed_log = self.parse_log(log)
                self.requests.append(parsed_log)
                
                request = parsed_log['request']
                self.uniq_requests[request] = self.uniq_requests.get(request, 0) + 1
