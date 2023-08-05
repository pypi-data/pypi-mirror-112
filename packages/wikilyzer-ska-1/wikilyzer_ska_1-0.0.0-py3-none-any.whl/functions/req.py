import requests

def req(*defx1):
    try:
        return requests.Session().get(url=defx1[0], params=defx1[1]).json()
    except:
        pass