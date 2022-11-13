import argparse
import json
import os.path
import re

def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', action='store_true', default=False, dest='json_enable')
    parser.add_argument('--path', default='./access.log', dest='logs_path')
    parser.add_argument('--output', default='output', dest='output_file_name')
    
    args = parser.parse_args()
    
    config = {
        'json': args.json_enable,
        'path': args.logs_path,
        'output': args.output_file_name,
    }

    return config

def parse_log(log):
    pattern = (
        r'(?P<remote_addr>[.\d]*) - (?P<remote_user>.*) \[(?P<time_local>.*)] ' +
        r'\"(?P<request>.*)\" (?P<response_status>\d\d\d) (?P<bytes_sent>\d*|-) ' +
        r'\"(?P<http_referer>.*)\" \"(?P<http_user_agent>.*)\" \"(?P<gzip_ratio>.*)\"'
    )
    
    return re.search(pattern, log).groupdict()

def parse_request(request):
    pattern = r'(?P<method>.*) (?P<url>\S*) (?P<headers>.*)'
    
    return re.search(pattern, request).groupdict()

def parse_log_file(path):
    requests = []
    uniq_requests = {}
    
    with open(path, 'r') as f:
        for log in f:
            parsed_log = parse_log(log)
            requests.append(parsed_log)
            
            request = parsed_log['request']
            uniq_requests[request] = uniq_requests.get(request, 0) + 1
    
    return requests, uniq_requests

def calc_uniq_requests_count(uniq_requests):
    count = len(uniq_requests.keys())
    result = [{
        'COUNT': count
    }]
    
    return result

def calc_amount_of_requests_by_type(uniq_requests):
    methods = {}
    for req in uniq_requests.keys():
        method = parse_request(req)['method']
        methods[method] = methods.get(method, 0) + 1
    
    result = []
    for method, count in methods.items():
        data = {
            'METHOD': method,
            'COUNT': count
        }
        result.append(data)
    
    return result

def calc_most_frequent_requests(uniq_requests, count):
    result = []
    most_frequent_requests = sorted(uniq_requests.items(), key=lambda x: x[1], reverse=True)[:count]
    for request in most_frequent_requests:
        data = {
            'URL': parse_request(request[0])['url'],
            'COUNT': request[1]
        }
        result.append(data)
    
    return result

def calc_most_frequent_4XX_requests(requests, count):
    result = []
    XX_requests = [request for request in requests if request['response_status'].startswith('4')]
    most_frequent_requests = sorted(XX_requests,
                                    key=lambda x: x['bytes_sent'],
                                    reverse=True)[:count]
    for request in most_frequent_requests:
        data = {
            'IP': request['remote_addr'],
            'STATUS': request['response_status'],
            'SIZE': request['bytes_sent'],
            'URL': parse_request(request['request'])['url'],
        }
        result.append(data)
    
    return result

def calc_most_frequent_5XX_requests_by_ip(requests, count):
    result = []
    XX_requests = [request for request in requests if request['response_status'].startswith('5')]
    
    most_frequent_ip = {}
    for request in XX_requests:
        ip = request['remote_addr']
        most_frequent_ip[ip] = most_frequent_ip.get(ip, 0) + 1
    
    top_list_ip = sorted(most_frequent_ip.items(), key=lambda x: x[1], reverse=True)[:count]
    for ip, count in top_list_ip:
        data = {
            'IP': ip, 
            'COUNT': count
        }
        result.append(data)
    
    return result

def calc_stat(requests, uniq_requests):
    stat = {}
    
    stat['COMMON AMOUNT OF REQUESTS'] = calc_uniq_requests_count(uniq_requests)
    stat['AMOUNT OF REQUESTS BY TYPES'] = calc_amount_of_requests_by_type(uniq_requests)
    stat['10 MOST FREQUENT REQUESTS'] = calc_most_frequent_requests(uniq_requests, count=10)
    stat['5 MOST FREQUENT REQUESTS WITH 4XX STATUS CODE'] = calc_most_frequent_4XX_requests(requests, count=5)
    stat['5 USERS BY REQUESTS WITH 5XX STATUS CODE'] = calc_most_frequent_5XX_requests_by_ip(requests, count=5)
    
    return stat

def store(stat, to, need_json):
    with open(f'{to}.txt', 'w') as f:
        for event, data in stat.items():
            f.write(event + '\n')
            for dict in data:
                for key, value in dict.items():
                    f.write(f'{str(key)}={str(value)}; ')
                f.write('\n')
            f.write('\n')

    if need_json:
        with open(f'{to}.json', 'w') as f:
            json.dump(stat, f)

if __name__== '__main__':
    config = get_config()
    requests, uniq_requests = parse_log_file(config['path'])
    stat = calc_stat(requests, uniq_requests)
    store(stat, to=config['output'], need_json=config['json'])
