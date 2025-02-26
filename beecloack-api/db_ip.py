from ipaddress import ip_address, ip_network
import pygeoip

ip_db = pygeoip.GeoIP('/var/www/beecloack_ru_usr/data/www/beecloack.ru/beecloack/beecloack-api/maxmind4.dat')

google_full = ['64.68.80.0/21',
                '64.233.160.0/19',
                '66.102.0.0/20',
                '66.249.64.0/19',
                '72.14.192.0/18',
                '74.125.0.0/16',
                '209.85.128.0/17',
                '216.239.32.0/19']

fb_full = ['31.13.24.0/21',
            '31.13.64.0/19',
            '31.13.64.0/24',
            '31.13.69.0/24',
            '31.13.70.0/24',
            '31.13.71.0/24',
            '31.13.72.0/24',
            '31.13.73.0/24',
            '31.13.75.0/24',
            '31.13.76.0/24',
            '31.13.77.0/24',
            '31.13.78.0/24',
            '31.13.79.0/24',
            '31.13.80.0/24',
            '66.220.144.0/20',
            '66.220.144.0/21',
            '66.220.149.11/16',
            '66.220.152.0/21',
            '66.220.158.11/16',
            '66.220.159.0/24',
            '69.63.176.0/21',
            '69.63.176.0/24',
            '69.63.184.0/21',
            '69.171.224.0/19',
            '69.171.224.0/20',
            '69.171.224.37/16',
            '69.171.229.11/16',
            '69.171.239.0/24',
            '69.171.240.0/20',
            '69.171.242.11/16',
            '69.171.255.0/24',
            '74.119.76.0/22',
            '173.252.64.0/19',
            '173.252.70.0/24',
            '173.252.96.0/19',
            '204.15.20.0/22']

yandex_full = ['77.88.0.0/18',
                '87.250.224.0/19',
                '93.158.128.0/18',
                '95.108.128.0/17',
                '213.180.192.0/19']

user_agent_stop = ['google',
                    'yahoo',
                    'yandex',
                    'webalta',
                    'aport',
                    'rambler',
                    'mail',
                    'msn',
                    'bot',
                    'curl',
                    'wget',
                    'python',
                    'php',
                    'crawl',
                    'httrack',
                    'spider',
                    'agent',
                    'metric',
                    'http',
                    'fetch',
                    'read',
                    'scrap']


def check_ip(ip):
    for row in google_full:
        if ip_address(ip) in ip_network(row, False):
            return True
    for row in yandex_full:
        if ip_address(ip) in ip_network(row, False):
            return True
    for row in fb_full:
        if ip_address(ip) in ip_network(row, False):
            return True
    return False


def check_user_agent(string):
    # Если юзер-агент пустой
    if string == '':
        return True
    # Если в юзер-агенте есть слова из стоп-листа
    for row in user_agent_stop:
        if row in string.lower():
            return True
    return False


def check_ip_geo(ip):
    return ip_db.country_code_by_addr(ip)


def check_allow_geo(list, ip):
    for country in list:
        if country.upper() == check_ip_geo(ip):
            return True
    return False

