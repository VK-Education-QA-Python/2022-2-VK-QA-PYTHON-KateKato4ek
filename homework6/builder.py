from model import (
    UniqRequestsCountTable,
    AmountOfRequestsByTypeTable,
    MostFrequentRequestsTable,
    MostFrequent4XXRequestsTable,
    MostFrequent5XXRequestsByIpTable
)

class MysqlBuilder():
    def __init__(self, client, parser):
        self.client = client
        self.parser = parser
    
    def calc_uniq_requests_count(self):
        count = len(self.parser.uniq_requests.keys())
        table = UniqRequestsCountTable(count=count)
        self.client.session.add(table)
        self.client.session.commit()
    
    def calc_amount_of_requests_by_type(self):
        methods = {}
        for req in self.parser.uniq_requests.keys():
            method = self.parser.parse_request(req)['method']
            methods[method] = methods.get(method, 0) + 1
              
        for method, count in methods.items():
            table = AmountOfRequestsByTypeTable(method=method, count=count)
            self.client.session.add(table)
        self.client.session.commit()
        
    def calc_most_frequent_requests(self, count):
        most_frequent_requests = sorted(self.parser.uniq_requests.items(), key=lambda x: x[1], reverse=True)[:count]
        
        for request in most_frequent_requests:
            url = self.parser.parse_request(request[0])['url']
            count = request[1]
            table = MostFrequentRequestsTable(url=url, count=count)
            self.client.session.add(table)
        self.client.session.commit()
    
    def calc_most_frequent_4XX_requests(self, count):
        XX_requests = [request for request in self.parser.requests if request['response_status'].startswith('4')]
        most_frequent_requests = sorted(XX_requests, key=lambda x: x['bytes_sent'], reverse=True)[:count]
        
        for request in most_frequent_requests:
            table = MostFrequent4XXRequestsTable(
                ip=request['remote_addr'],
                status=request['response_status'],
                size=request['bytes_sent'],
                url=self.parser.parse_request(request['request'])['url'],
            )
            self.client.session.add(table)
        self.client.session.commit()
    
    def calc_most_frequent_5XX_requests_by_ip(self, count):
        XX_requests = [request for request in self.parser.requests if request['response_status'].startswith('5')]
    
        most_frequent_ip = {}
        for request in XX_requests:
            ip = request['remote_addr']
            most_frequent_ip[ip] = most_frequent_ip.get(ip, 0) + 1
        
        top_list_ip = sorted(most_frequent_ip.items(), key=lambda x: x[1], reverse=True)[:count]
        for ip, count in top_list_ip:
            table = MostFrequent5XXRequestsByIpTable(ip=ip, count=count)
            self.client.session.add(table)
        self.client.session.commit()
