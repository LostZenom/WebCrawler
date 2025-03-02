import json, csv, time, requests
from googlesearch import search
from concurrent.futures import ThreadPoolExecutor
from os import linesep, system

half_length = 33

system("title " + "Web-Crawler")
print('\033[94m' + '██     ██ ███████ ██████   ██████ ██████   █████  ██     ██ ██      '[:half_length] + '\033[97m' + '██     ██ ███████ ██████   ██████ ██████   █████  ██     ██ ██      '[half_length:])
print('\033[94m' + '██     ██ ██      ██   ██ ██      ██   ██ ██   ██ ██     ██ ██      '[:half_length] + '\033[97m' + '██     ██ ██      ██   ██ ██      ██   ██ ██   ██ ██     ██ ██      '[half_length:])
print('\033[94m' + '██  █  ██ █████   ██████  ██      ██████  ███████ ██  █  ██ ██      '[:half_length] + '\033[97m' + '██  █  ██ █████   ██████  ██      ██████  ███████ ██  █  ██ ██      '[half_length:])
print('\033[94m' + '██ ███ ██ ██      ██   ██ ██      ██   ██ ██   ██ ██ ███ ██ ██      '[:half_length] + '\033[97m' + '██ ███ ██ ██      ██   ██ ██      ██   ██ ██   ██ ██ ███ ██ ██      '[half_length:])
print('\033[94m' + ' ███ ███  ███████ ██████   ██████ ██   ██ ██   ██  ███ ███  ███████'[:half_length] + '\033[97m' + ' ███ ███  ███████ ██████   ██████ ██   ██ ██   ██  ███ ███  ███████'[half_length:])
print('\033[94m' + '==================================================================='[:half_length] + '\033[97m' + '==================================================================='[half_length:])

keyword = input("[CONSOLE] Enter Your Keyword: ")
proxe = int(input("[CONSOLE] Use Proxylist [1] Yes [2] No: "))


keywords = [keyword]


urls = []


proxy_list = []


if proxe == 1:
    if not proxy_list:
        print("No results found for this proxy.")
elif proxe == 2:
    with open('urls.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for i in urls:
            writer.writerow(i)


def prox_session():
    
    proxy_url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    response = requests.get(proxy_url)

    try:
        if response.status_code == 200:
            file_lines = response.text.split('\n')
            for line in file_lines:
                proxy = line.strip()
                if proxy:
                    proxy_list.append({'http': f'http://{proxy}'})

        return proxy_list
    
    except Exception as e:
        print(e)
        return 0, []

proxies = prox_session()
print(json.dumps(proxies, indent=2))

def search_google(keyword, proxy):
    result_count = 0
    try:
        sResult = list(search(keyword, proxy=proxy, num_results=100))
        for i in sResult: urls.append(i), print(i)
        result_count = len(urls)
        return result_count, urls
    except Exception as e:
        print(f'Error: in search_google() | {e}')
        return 0, []

def display_progress(keyword, num_results):
    print(f"Search results for '{keyword}': {num_results}")


with ThreadPoolExecutor() as executor:
    results = []
    for keyword in keywords:
        if proxe == '1':
            for proxy in prox_session():
                results.append(executor.submit(search_google, keyword, proxy))
                time.sleep(1) 
        else:
            results.append(executor.submit(search_google, keyword, None))
            time.sleep(1) 


    for i in results:
        result_count, result_urls = i.result()
        if result_count > 0:
            urls.append(result_urls)
            display_progress(keyword, result_count)
        else:
            print("No results found for this proxy.")
        time.sleep(1)


with open('urls.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f, lineterminator='\n')
    for i in urls:
        writer.writerow([i])
