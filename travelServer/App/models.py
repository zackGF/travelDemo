from datetime import datetime
from passlib.apps import custom_app_context

from App import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.Integer, unique=True)
    password = db.Column(db.String(255))
    status = db.Column(db.Boolean, default=True)
    c_time = db.Column(db.DateTime, default=datetime.now)

    attrorder = db.relationship("Attrorder",backref = "user")
    hotelorder = db.relationship("Hotelorder",backref = "user")

    # 密码加密
    def hash_password(self, password):
        self.password = custom_app_context.encrypt(password)

    # 密码认证
    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)


class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    info = db.Column(db.String(1000))
    price = db.Column(db.Integer)
    picture_link = db.Column(db.String(500))
    c_time = db.Column(db.DateTime, default=datetime.now)

    hotelorder = db.relationship("Hotelorder",backref="hotel")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "info": self.info,
            "price": self.price,
            "picture": self.picture_link,
            "c_time": self.c_time
        }


class Attractions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    info = db.Column(db.String(1000))
    price = db.Column(db.Integer)
    picture_link = db.Column(db.String(500))
    c_time = db.Column(db.DateTime, default=datetime.now)

    attrorder = db.relationship("Attrorder",backref="attractions")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "info": self.info,
            "price": self.price,
            "picture": self.picture_link,
            "c_time": self.c_time
        }

# 景点订单
class Attrorder(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    attr_id = db.Column(db.Integer,db.ForeignKey('attractions.id'))
    user_phone = db.Column(db.Integer)
    info = db.Column(db.String(128))
    order_status = db.Column(db.Boolean,default=True)
    c_time = db.Column(db.DateTime, default=datetime.now)
    def to_dict(self):
        return {
            "id":self.id,
            "user_phone":self.user_phone,
            "info":self.info,
            "c_time":self.c_time
        }

# 酒店订单
class Hotelorder(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))
    user_phone = db.Column(db.Integer)
    info = db.Column(db.String(128))
    order_status = db.Column(db.Boolean, default=True)
    c_time = db.Column(db.DateTime, default=datetime.now)
    def to_dict(self):
        return {
            "id":self.id,
            "user_phone":self.user_phone,
            "info":self.info,
            "c_time":self.c_time
        }

# 景点评论
class Attrcomm(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    attr_id = db.Column(db.Integer,db.ForeignKey('attractions.id'))
    user_phone = db.Column(db.Integer)
    info = db.Column(db.String(500))    # 留言信息
    attrname = db.Column(db.String(128))    # 景点名称
    c_time = db.Column(db.DateTime, default=datetime.now)
    def to_dict(self):
        return {
            "id":self.id,
            "user_phone":self.user_phone,
            "text":self.info,
            "attr_":self.attr_id,
            "attrname":self.attrname,
            "c_time":self.c_time
        }



# 酒店评论
class Hotelcomm(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))
    user_phone = db.Column(db.Integer)
    info = db.Column(db.String(500))  # 留言信息
    hotelname = db.Column(db.String(128))  # 景点名称
    c_time = db.Column(db.DateTime, default=datetime.now)
    def to_dict(self):
        return {
            "id":self.id,
            "user_phone":self.user_phone,
            "text":self.info,
            "hotel_":self.hotel_id,
            "hotelname":self.hotelname,
            "c_time":self.c_time
        }



