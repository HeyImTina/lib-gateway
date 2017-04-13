# coding:utf-8
import json

from flask import request, jsonify
from flask_login import login_user, logout_user, current_user, login_required

from app.api_1_0 import api
from app.model import db
from app.model.service import Service
from app.model.user import admin_required, User
from app.util.utils import reload_service, redirect_backend_service


@api.route('/')
def hello_world():
    return 'Hello World!'


@api.route("/login", methods=['POST'])
def login():
    name = request.form.get("name")
    password = request.form.get("password")
    user = User.query.filter_by(name=name).first()
    if user and user.verify_password(password):
        login_user(user)
        return json.dumps({
            "code": 0,
            "data": user.json()
        })
    return json.dumps({
        "code": 1,
        "msg": "login fail!"
    })


@api.route("/logout")
def logout():
    logout_user(current_user)
    return json.dumps({
        "code": 0,
        "msg": "ok"
    })


@api.route("/service/add")
def service_add():
    db.session.add(Service(
        service_name=request.args.get("service_name"),
        ip=request.args.get("ip"),
        port=request.args.get("port"),
    ))
    db.session.commit()
    reload_service()
    return json.dumps({
        "code": 0,
        "msg": "ok"
    })


@api.route("/service/delete")
def service_delete():
    ret = Service.query.filter_by(id=request.args.get("id")).first()
    if ret:
        db.session.delete(ret)
        db.session.commit()
        reload_service()
    return json.dumps({
        "code": 0,
        "msg": "ok"
    })


@api.route("/service/reload")
def service_reload():
    reload_service()
    return json.dumps({
        "code": 0,
        "msg": "ok"
    })


@api.route("/ebook/edit", methods=['POST'])
@admin_required
def ebook_edit():
    res = redirect_backend_service("ebook", "/api/v1.0/ebook/edit")
    return jsonify(res.text)


@api.route("/ebook/add", methods=['POST'])
@admin_required
def ebook_add():
    res = redirect_backend_service("ebook", "/api/v1.0/ebook/add")
    return jsonify(res.text)


@api.route("/ebook/delete")
@admin_required
def ebook_delete():
    res = redirect_backend_service("ebook", "/api/v1.0/ebook/delete")
    return jsonify(res.text)


@api.route("/ebook/list")
@login_required
def ebook_list():
    res = redirect_backend_service("ebook", "/api/v1.0/ebook/list")
    return jsonify(res.text)


@api.route("/ebook/<book_id>")
@login_required
def ebook(book_id):
    res = redirect_backend_service("ebook", "/api/v1.0/ebook/{id}".format(id=book_id))
    return jsonify(res.text)


@api.route("/comment/add", methods=['POST'])
@login_required
def comment_add():
    res = redirect_backend_service("comment", "/api/v1.0/comment/add")
    return jsonify(res.text)


@api.route("/comment/delete")
@admin_required
def comment_delete():
    res = redirect_backend_service("comment", "/api/v1.0/comment/delete")
    return jsonify(res.text)


@api.route("/comment/list")
@login_required
def comment_list():
    res = redirect_backend_service("comment", "/api/v1.0/comment/list")
    return jsonify(res.text)


@api.route("/pbook/add", methods=['POST'])
@admin_required
def pbook_add():
    res = redirect_backend_service("pbook", "/api/v1.0/pbook/add")
    return jsonify(res.text)


@api.route("/pbook/delete")
@admin_required
def pbook_delete():
    res = redirect_backend_service("pbook", "/api/v1.0/pbook/delete")
    return jsonify(res.text)


@api.route("/pbook/list")
@login_required
def pbook_list():
    res = redirect_backend_service("pbook", "/api/v1.0/pbook/list")
    return jsonify(res.text)


@api.route("/pbook/<book_id>")
@login_required
def pbook(book_id):
    res = redirect_backend_service("pbook", "/api/v1.0/pbook/{book_id}".format(book_id=book_id))
    return jsonify(res.text)

