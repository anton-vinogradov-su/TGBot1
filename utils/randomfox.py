import requests

def fox():
    url = 'https://randomfox.ca/floof'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['image']
    else:
        return 'Error: Failed to get random image from Fox API'

if __name__ == '__main__':
    print(fox())