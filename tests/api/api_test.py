import requests


if __name__ == '__main__':
    pwd = 'maple809427'
    username = 'mwish'
    test_url = 'http://localhost:5000/api/test'
    h1 = 'req1.html'
    resp = requests.get(test_url, auth=(username, pwd))
    print(resp.content)

    pwd2 = "maplewish"
    resp = requests.get(test_url, auth=(username, pwd2))
    print(resp.content)
