# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, abort, redirect
from db_ip import check_user_agent, check_ip, check_ip_geo, check_allow_geo
from lic import check_license, decrypt, ex_key, ex_login
from scanner2 import check_ports
from stats import click
from loguru import logger

logger.add('api.log', rotation='500 MB', encoding='utf-8', level='DEBUG')
app = Flask(__name__)


'''
@app.errorhandler(404)
def handle_notfound(e):
    abort(403)

@app.errorhandler(500)
def handle_intsrverr(e):
    abort(403)
'''

@app.route('/', methods=["POST"])
def application():
    try:
        json = request.get_json()
    except:
        abort(403)
        
    logger.debug(json)
    logger.debug('[1] Check License')
    try:
        encoded = decrypt(json['transport'])
        key = ex_key(encoded)
        logger.debug(f'api_key: {key}')
    except Exception as decrypt_error:
        logger.exception(decrypt_error)
        return jsonify(status=0, error_text='Request Failed (01)')
    try:
        if not check_license(key):
            logger.debug('api_key not validated on the server')
            return jsonify(status=0, error_text='License Expired')
    except Exception as license_error:
        logger.exception(license_error)
        return jsonify(status=0, error_text='Request Failed (02)')

    try:
        stats = {
            'ip': json['ip'],
            'ua': json['user-agent'],
            'ref': json['referer'],
            'login': ex_login(encoded),
            'page': '',
            'filter': '',
            'descr': ''}
    except Exception as stats_e:
        logger.exception(stats_e)
    # logger.info(stats)
    logger.info('[2] Check Referrer')
    try:
        if json['referer']:
            logger.debug('Check Referrer Enabled')
            if json['cn_referer']:
                logger.debug(f'User set Referer: {json["cn_referer"]}')
                cn_referer = json['cn_referer']
                if cn_referer.lower() not in json['referer']:
                    logger.debug(f'Referer does not match or custom Referer. Redirect to White Page...')
                    stats.update({'page': 'White', 'filter': 'Referer', 'descr': 'Referer не соответствует заданному'})
                    click(stats)
                    return jsonify(status=1, redirect=1)
            else:
                if json['referer'] == 'none':
                    logger.debug('Referer empty. Redirect to White Page...')
                    stats.update({'page': 'White', 'filter': 'Referer', 'descr': 'Пустой Referer'})
                    click(stats)
                    return jsonify(status=1, redirect=1)
    except Exception as ref_error:
        logger.exception(ref_error)
        return jsonify(status=0, error_text='Request Failed (03)')

    logger.info('[3] Check User-Agent')
    try:
        if check_user_agent(str(json["user-agent"])):
            logger.debug('User Agent founded in black-list. Redirect to White Page...')
            stats.update({'page': 'White', 'filter': 'User-Agent', 'descr': 'User-Agent проверка не пройдена'})
            click(stats)
            return jsonify(status=1, redirect=1)
    except Exception as check_ua_error:
        logger.exception(check_ua_error)
        return jsonify(status=0, error_text='Request Failed (04)')

    logger.info('[4] Check IP')
    try:
        if check_ip(str(json["ip"])):
            logger.debug(f'IP {json["ip"]} found in black-list. Redirect to White Page...')
            stats.update({'page': 'White', 'filter': 'IP', 'descr': 'Проверка IP не пройдена'})
            click(stats)
            return jsonify(status=1, redirect=1)
    except Exception as check_ip_error:
        logger.exception(check_ip_error)
        return jsonify(status=0, error_text='Request Failed (05)')

    logger.info('[5] Check GEO in user filter')
    try:
        if json["blocked_method"] == 1:
            for country in json["country_list"].split(','):
                if country == check_ip_geo(json["ip"]):
                    logger.debug('GEO in black list. Redirect to White Page...')
                    stats.update({'page': 'White', 'filter': 'GEO', 'descr': 'Геолокация из списка запрещенных'})
                    click(stats)
                    return jsonify(status=1, redirect=1)

        elif json["blocked_method"] == 2:
            if check_allow_geo(json["country_list"].split(','), json['ip']):
                logger.debug('GEO in white list. Continue check...')
            else:
                logger.debug('GEO does not match in white list. Redirect to White Page...')
                stats.update({'page': 'White', 'filter': 'GEO', 'descr': 'Геолокация не из списка разрешенных'})
                click(stats)
                return jsonify(status=1, redirect=1)
        else:
            logger.error('Incorrect check GEO method')
            return jsonify(status=0, error_text='Request Failed (05)')

    except Exception as check_geo_error:
        logger.exception(check_geo_error)
        return jsonify(status=0, error_text='Request Failed (06)')

    logger.info('[5] Check IP in VPN/PROXY')
    if json['check_ip'] == 1:
        logger.debug('User set enable IP Check')
        try:
            if check_ports(json['ip']):
                logger.debug('VPN/Proxy Detected. Redirect to White Page... ')
                stats.update({'page': 'White', 'filter': 'VPN/PROXY', 'descr': 'Обнаружены средства анонимизации'})
                click(stats)
                return jsonify(status=1, redirect=1)
        except Exception as check_ip_error:
            logger.exception(check_ip_error)
            return jsonify(status=0, error_text='Request Failed (07)')


    logger.info('All checks passed. Redirect to Black Page...')
    stats.update({'page': 'Black', 'filter': '', 'descr': 'Проверки пройдены успешно'})
    click(stats)
    return jsonify(status=1, redirect=2)


if __name__ == '__main__':
    app.run(host='127.0.0.1:', port=5000)
