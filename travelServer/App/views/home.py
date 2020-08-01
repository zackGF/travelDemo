import re

from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask import Blueprint, request, jsonify, g
from App.models import *

home = Blueprint('home', __name__)

# token令牌
s = Serializer('phone', expires_in=300)
auth = HTTPTokenAuth('Bearer')


# auth的回调
@auth.verify_token
def verify_token(token):
    try:
        data = s.loads(token)
    except SignatureExpired:
        return False
    except BadSignature:
        return False
    except:
        return False
    if 'phone' in data:
        g.phone = data['phone']
        return True
    return False


@auth.error_handler
def error_handler():
    return jsonify({"code": 104, "msg": "没有权限"})


# 景点
@home.route('/')
def index():
    attr_obj = Attractions.query.all()
    return jsonify([attr.to_dict() for attr in attr_obj])


@home.route('/attrinfo')
def attrInfo():
    id = request.args["attr"]
    print(id)
    attr_obj = Attractions.query.filter_by(id=id).first()
    return jsonify({"code": 102, "msg": "success", "result": {
        "id":attr_obj.id,
        "name": attr_obj.name,
        "info": attr_obj.info,
        "price": attr_obj.price,
        "picture": attr_obj.picture_link,
        "c_time": attr_obj.c_time
    }})


# 酒店
@home.route('/hotel')
def hotel_index():
    hotel_obj = Hotel.query.all()
    return jsonify([hotel.to_dict() for hotel in hotel_obj])

@home.route('/hotelinfo')
def hotelInfo():
    id = request.args["hotel"]
    print(id)
    attr_obj = Hotel.query.filter_by(id=id).first()
    return jsonify({"code": 102, "msg": "success", "result": {
        "id":attr_obj.id,
        "name": attr_obj.name,
        "info": attr_obj.info,
        "price": attr_obj.price,
        "picture": attr_obj.picture_link,
        "c_time": attr_obj.c_time
    }})

@home.route("/login", methods=["POST"])
def userLogin():
    # 获取前端的值
    phone = request.json["phone"]
    password = request.json["password"]
    # 验证手机号是否为空
    if phone == "":
        return jsonify({"code": 104, "msg": "手机号码不能为空"})
    # 验证手机号     通过正则表达式
    phone_bat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
    phone_res = re.match(phone_bat, phone)
    if not phone_res:
        return jsonify({"code": 104, "msg": "手机号码格式不正确！"})
    # 验证 密码是否为空
    if password == "":
        return jsonify({"code": 104, "msg": "密码不能为空！"})
    user_obj = User.query.filter_by(phone=phone).first()
    if not user_obj:
        return jsonify({"code": 104, "msg": "此手机号不存在！"})
    if user_obj.verify_password(password):
        if user_obj.status:
            token = s.dumps({'phone': phone}).decode("utf-8")
            print(token)
            return jsonify({"code": 102, "msg": "成功", "user_token": token})
        return jsonify({"code": 105, "msg": "此账户已被禁封！"})
    return jsonify({"code": 104, "msg": "此账户密码不正确！"})


# 用户注册
@home.route("/register", methods=["POST"])
def userRegister():
    # 接收前端的值
    phone = request.json["phone"]  # 手机号码
    password1 = request.json["password1"]  # 密码
    password2 = request.json["password2"]  # 确认密码
    print(phone, password1, password2)
    # 验证手机号是否为空
    if phone == "":
        return jsonify({"code": 104, "msg": "手机号码不能为空"})

    # 验证手机号     通过正则表达式
    phone_bat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
    phone_res = re.match(phone_bat, phone)
    if not phone_res:
        return jsonify({"code": 104, "msg": "手机号码格式不正确！"})

    # 验证手机号是否已被注册
    if User.query.filter_by(phone=phone).first() is not None:
        return jsonify({"code": 104, "msg": "该手机号已被注册！"})

    # 验证 密码是否为空
    if password1 == "" and password2 == "":
        return jsonify({"code": 104, "msg": "密码不能为空！"})

    # 验证两次密码是否相同
    if password1 != password2:
        return jsonify({"code": 104, "msg": "两次输入的密码不同"})

    # 将数据插入数据库
    user_obj = User(phone=phone)
    user_obj.hash_password(password=password1)
    db.session.add(user_obj)
    db.session.commit()
    return jsonify({"code": 102, "msg": "注册成功", "result": user_obj.phone})


# 用户中心
@home.route("/center")
@auth.login_required
def userCenter():
    phone = g.phone
    user_obj = User.query.filter_by(phone=phone).first()
    if user_obj:
        return jsonify({"code": 102, "msg": "欢迎" + phone, "result": phone})
    return jsonify({"code": 104, "msg": "未知错误"})

# 用户评论  景点
@home.route("/showattr")
@auth.login_required
def userShowAttr():
    userphone = request.args['userphone']
    print(userphone)
    comm_obj = Attrcomm.query.filter_by(user_phone = userphone).all()
    print(comm_obj)
    return jsonify([comm.to_dict() for comm in comm_obj])

# 用户评论    酒店
@home.route("/showhotel")
@auth.login_required
def userShowHotel():
    userphone = request.args['userphone']
    comm_obj = Hotelcomm.query.filter_by(user_phone = userphone).all()
    return jsonify([comm.to_dict() for comm in comm_obj])

# 用户密码更改
@home.route("/changepwd", methods=["POST"])
@auth.login_required
def userChangePwd():
    phone = g.phone
    userphone = request.json["userphone"]
    password = request.json["newpassword"]
    if phone != userphone:
        return jsonify({"code": 104, "msg": "此手机号不存在"})
    if password == "":
        return jsonify({"code": 104, "msg": "密码不能为空！"})
    user_obj = User.query.filter_by(phone=userphone).first()
    user_obj.hash_password(password=password)
    db.session.commit()
    return jsonify({"code": 102, "msg": "修改成功!"})

#景点订单 post
@home.route("/attrorder",methods=["POST"])
@auth.login_required
def userAttrOrder():
    ramphone = g.phone
    attr_id = request.json["attractions"]
    userphone = request.json["userphone"]
    info = request.json["info"]
    if ramphone != userphone:
        return jsonify({"code": 104, "msg": "此手机号不存在"})
    if attr_id is None and attr_id=="":
        return jsonify({"code": 104, "msg": "未知错误"})
    user_obj = User.query.filter_by(phone=userphone).first()
    userid = user_obj.id    # 通过用户的手机号获取用户id

    attr_obj = Attractions.query.filter_by(id=attr_id).first()
    if attr_obj:
        attr_order_obj = Attrorder.query.filter_by(attr_id=attr_id,user_id=userid).first()
        if attr_order_obj:
            return jsonify({"code":103,"msg":"景点已添加"})
        attrOrder_obj = Attrorder(user_id=userid,attr_id=attr_id,user_phone=userphone,info=info)
        db.session.add(attrOrder_obj)
        db.session.commit()
        return jsonify({"code":102,"msg":"预订成功！","result":attrOrder_obj.user_phone})
    return jsonify({"code":104,"msg":"未找到此景点信息"})

#景点订单 get
@home.route("/attrorder")
@auth.login_required
def userAttrOrder_get():
    ramphone = g.phone
    userphone = request.args['phone']
    print(ramphone)
    print(userphone)
    if ramphone != userphone:
        return jsonify({"code": 104, "msg": "此手机号不存在"})
    order_obj = Attrorder.query.filter_by(user_phone=userphone).all()
    if order_obj:
        return jsonify([order.to_dict() for order in order_obj])
    return jsonify({"code":107,"msg":"无","result":"null"})


# 酒店订单
@home.route("/hotelorder",methods=["POST"])
@auth.login_required
def userHotelOrder():
    ramphone = g.phone
    hotel_id = request.json["hotel"]
    userphone = request.json["userphone"]
    info = request.json["info"]
    if ramphone != userphone:
        return jsonify({"code": 104, "msg": "此手机号不存在"})
    if hotel_id is None and hotel_id == "":
        return jsonify({"code": 104, "msg": "未知错误"})
    user_obj = User.query.filter_by(phone=userphone).first()
    userid = user_obj.id  # 通过用户的手机号获取用户id

    hotel_obj = Hotel.query.filter_by(id=hotel_id).first()
    if hotel_obj:
        hotel_order_obj = Hotelorder.query.filter_by(hotel_id=hotel_id, user_id=userid).first()
        if hotel_order_obj:
            return jsonify({"code": 103, "msg": "酒店已预定"})
        hotelOrder_obj = Hotelorder(user_id=userid, hotel_id=hotel_id, user_phone=userphone,info=info)
        db.session.add(hotelOrder_obj)
        db.session.commit()
        return jsonify({"code": 102, "msg": "酒店预订成功！", "result": hotelOrder_obj.user_phone})
    return jsonify({"code": 104, "msg": "未找到酒店信息"})

#酒店订单 get
@home.route("/hotelorder")
@auth.login_required
def userHotelOrder_get():
    ramphone = g.phone
    userphone = request.args['phone']
    print(ramphone)
    print(userphone)
    if ramphone != userphone:
        return jsonify({"code": 104, "msg": "此手机号不存在"})
    order_obj = Hotelorder.query.filter_by(user_phone=userphone).all()
    if order_obj:
        return jsonify([order.to_dict() for order in order_obj])
    return jsonify({"code":107,"msg":"无","result":"null"})

# 景点评论 get
@home.route("/attrcomm")
@auth.login_required
def userAttrComm_get():
    id = request.args["id"]
    comm_obj = Attrcomm.query.filter_by(attr_id=id).all()
    return jsonify([comm.to_dict() for comm in comm_obj])

# 景点评论 post
@home.route("/attrcomm",methods=["POST"])
@auth.login_required
# @auth.login_required
def userAttrComm_post():
    attr_id = request.json["attractions"]   # 景点id
    userphone = request.json["userphone"]   # 用户手机号
    info = request.json["textinfo"]             # 用户评论
    attrname = request.json["attrname"]     # 景点名称
    # print(attr_id+","+userphone+","+info+","+attrname)
    user_obj = User.query.filter_by(phone=userphone).first()
    if user_obj:
        user_id = user_obj.id                   # 用户id
        comm_obj = Attrcomm(user_id=user_id,attr_id=attr_id,user_phone=userphone,info=info,attrname=attrname)
        if comm_obj:
            db.session.add(comm_obj)
            db.session.commit()
            return jsonify({"code":102,"msg":"评论成功"})
        return jsonify({"code":104,"msg":"评论失败"})
    return jsonify({"code":104,"msg":"用户异常"})

# 酒店评论 get
@home.route("/hotelcomm")
@auth.login_required
def userHotelComm_get():
    id = request.args["id"]
    hotel_obj = Hotelcomm.query.filter_by(hotel_id=id).all()
    return jsonify([hotel.to_dict() for hotel in hotel_obj])

# 酒店评论 post
@home.route("/hotelcomm",methods=["POST"])
@auth.login_required
def userHotelComm_post():
    hotel_id = request.json["hotel"]  # 酒店id
    userphone = request.json["userphone"]  # 用户手机号
    info = request.json["textinfo"]  # 用户评论
    hotelname = request.json["hotelname"]  # 酒店名称
    # print(hotel_id + "," + userphone + "," + info + "," + hotelname)
    user_obj = User.query.filter_by(phone=userphone).first()
    if user_obj:
        user_id = user_obj.id  # 用户id
        comm_obj = Hotelcomm(user_id=user_id, hotel_id=hotel_id, user_phone=userphone, info=info, hotelname=hotelname)
        if comm_obj:
            db.session.add(comm_obj)
            db.session.commit()
            return jsonify({"code": 102, "msg": "评论成功"})
        return jsonify({"code": 104, "msg": "评论失败"})
    return jsonify({"code": 104, "msg": "用户异常"})




