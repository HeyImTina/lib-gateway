import json
import random

from flask import request as flask_request
from requests import Session
from requests_futures.sessions import FuturesSession


def get_url(service_name, path, protocol='http'):
    if protocol == 'http':
        prefix = "http://"
    elif protocol == 'https':
        prefix = 'https://'
    else:
        prefix = ''
    return prefix + get_address(service_name) + path


def get_address(service_name):
    service_key = "SERVICES"
    from app import redis_store
    from app.model.service import Service
    ret = redis_store.hget(service_key, service_name)
    if ret:
        ret_lst = json.loads(ret)
        return random.choice(ret_lst)
    else:
        ret = Service.query.filter_by(service_name=service_name).all()
        print ret
        if ret:
            ret_lst = [x.address for x in ret]
            return random.choice(ret_lst)
        else:
            return None


def reload_service():
    service_key = "SERVICES"
    from app import redis_store
    from app.model.service import Service
    rets = Service.query.all()
    dct = {}
    for item in rets:
        if item.service_name in dct.keys():
            dct[item.service_name].append(item.address)
        else:
            dct[item.service_name] = [item.address]
    for key, value in dct.items():
        redis_store.hset(service_key, key, json.dumps(value))


def request(method, url, **kwargs):
    async = kwargs.get("async", False)
    if async:
        session = FuturesSession()
    else:
        session = Session()
    return session.request(method=method, url=url, **kwargs)


def get(url, **kwargs):
    return request('get', url, **kwargs)


def post(url, data=None, **kwargs):
    return request('post', url, data=data, **kwargs)


def redirect_backend_service(service_name, path):
    url = get_url(service_name, path)
    if flask_request.method == "POST":
        res = post(url, data=flask_request.form)
    else:
        res = get(url, params=flask_request.args)
    return res
