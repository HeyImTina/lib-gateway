# coding:utf-8
from _socket import inet_ntoa, inet_aton

from app.model import db
from datetime import datetime


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(50))
    ip = db.Column(db.String(16))
    port = db.Column(db.Integer)
    created_time = db.Column(db.DateTime(), default=datetime.now)

    @property
    def address(self):
        return ":".join([self.ip, str(self.port)])
