import requests
from user_agents import parse
from db_ip import check_ip_geo


def click(data):
    info = {
        "login": data["login"],
        "ip": data["ip"],
        "country": check_ip_geo(data["ip"]),
        "useragent": data["ua"],
        "referrer": data["ref"],
        "device": parse(data["ua"]),
        "filter": data["filter"],
        "page": data["page"],
        "description": data["descr"],
    }
    url = "http://beecloack.ru/setstatistic"
    r = requests.post(url, data=info)
    # print(r.text)


stats = {
    "ip": "27.80.215.114",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36 OPR/87.0.4390.36",
    "ref": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
    "login": "test",
    "page": "White",
    "filter": "VPN/PROXY",
    "descr": "Тест",
}

# click(stats)
