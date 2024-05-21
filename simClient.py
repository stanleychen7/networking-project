import argparse
import requests
import matplotlib.pyplot as plt
import random
import m3u8
import m3u8_To_MP4
from urllib.parse import urlparse

parser = argparse.ArgumentParser(description='Process URL for video API')
parser.add_argument('host', type=str, help='Host of the URL')
parser.add_argument('port', type=int, help='Port of the URL')
args = parser.parse_args()

url = f'http://{args.host}:{args.port}/api/videos'
response = requests.get(url)

def RequestVideoServer(title, location = ''):
    url = f'http://{args.host}:{args.port}/ld/video'
    headers = {'Content-Type': 'application/json'}
    data = {'title': title, 'location': location}
    response = requests.post(url, headers=headers, json=data)
    data = response.json()
    return data['url']

if response.status_code == 200:
    data = response.json()
else:
    print('Failed to get data:', response.status_code, response.text)

vids = []
for i in range(0, len(data)):
    vids.append(data[i]['title'])

States = [
    "AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "IA",
    "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO",
    "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI",
    "WV", "WY",
]

selection = input('Enter 1 to select a video or 2 to run tests: ')

if selection == '1':
    try:
        for i in range(0, len(vids)):
            video = data[i]
            services = ', '.join([service['hostname'] for service in video['VideoServices']])
            print(f'{i + 1}.{video["title"]} \nviews:{video["views"]}   Videoservices: {services}\n')
        n = int(input('Select a video to play: '))
        if n > 0 and n <= len(vids):
            print(f'You selected {vids[n - 1]}')
            url = RequestVideoServer(vids[n-1], "NY")
            playlist = m3u8.load(url)
            m3u8_To_MP4.multithread_download(url)
        else:
            print('Invalid selection. Please enter a valid number.')
    except ValueError:
        print('Invalid input. Please enter a number.')
elif selection == '2':
    test_selection = input('Enter number for test to run: ')
    servers_requests = {}
    if test_selection == '1':
        for i in range(0, 100):
            url = RequestVideoServer('test', 'NY')
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname
            port = parsed_url.port
            key = f'{hostname}:{port}'
            servers_requests[key] = servers_requests.get(key, 0) + 1
        print(servers_requests)
        plt.figure(figsize=(10, 6))
        plt.bar(servers_requests.keys(), servers_requests.values())
        plt.xlabel('Server')
        plt.ylabel('Request Count')
        plt.title('Request Count per Server')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    if test_selection == '2':
        for i in range(0, 100):
            url = RequestVideoServer('test', '')
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname
            port = parsed_url.port
            key = f'{hostname}:{port}'
            servers_requests[key] = servers_requests.get(key, 0) + 1
        print(servers_requests)
        plt.figure(figsize=(10, 6))
        plt.bar(servers_requests.keys(), servers_requests.values())
        plt.xlabel('Server')
        plt.ylabel('Request Count')
        plt.title('Request Count per Server')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    if test_selection == '3':
        for i in range(0, 1000):
            random_video_index = random.randint(0, len(data) - 1)
            video = data[random_video_index]
            url = RequestVideoServer(video['title'], '')
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname
            port = parsed_url.port
            key = f'{hostname}:{port}'
            servers_requests[key] = servers_requests.get(key, 0) + 1
        print(servers_requests)
        plt.figure(figsize=(10, 6))
        plt.bar(servers_requests.keys(), servers_requests.values())
        plt.xlabel('Server')
        plt.ylabel('Request Count')
        plt.title('Request Count per Server')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    if test_selection == '4':
        for i in range(0, 1000):
            random_video_index = random.randint(0, len(data) - 1)
            video = data[random_video_index]
            url = RequestVideoServer(video['title'], 'LA')
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname
            port = parsed_url.port
            key = f'{hostname}:{port}'
            servers_requests[key] = servers_requests.get(key, 0) + 1
        print(servers_requests)
        plt.figure(figsize=(10, 6))
        plt.bar(servers_requests.keys(), servers_requests.values())
        plt.xlabel('Server')
        plt.ylabel('Request Count')
        plt.title('Request Count per Server')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    if test_selection == '5':
        servers_states = {}
        for i in range(0, 1000):
            random_video_index = random.randint(0, len(data) - 1)
            video = data[random_video_index]
            state = random.choice(States)
            url = RequestVideoServer(video['title'], state)
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname
            port = parsed_url.port
            key = f'{hostname}:{port}'
            servers_requests[key] = servers_requests.get(key, 0) + 1
            servers_states.setdefault(key, {}).setdefault(state, 0)
            servers_states[key][state] += 1
        print(servers_requests)
        print(servers_states)
        plt.figure(figsize=(10, 6))
        plt.bar(servers_requests.keys(), servers_requests.values())
        plt.xlabel('Server')
        plt.ylabel('Request Count')
        plt.title('Request Count per Server')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        for server, state_counts in servers_states.items():
            plt.figure(figsize=(6, 4))
            plt.bar(state_counts.keys(), state_counts.values())
            plt.xlabel('State')
            plt.ylabel('Request Count')
            plt.title(f'Request Count per State for Server {server}')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
    pass
else:
    print('Invalid selection. Please enter 1 or 2.')


