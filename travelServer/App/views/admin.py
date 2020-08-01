import time

from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify

from App.config import basedir,base_server
from App.models import *
from functools import wraps

admin = Blueprint('admin', __name__)


def admin_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_id" not in session:
            return "<script>alert('请先登录');history.go(-1)</script>"
        return f(*args, **kwargs)

    return decorated_function


# 管理员主页面
@admin.route("/adminHome")
@admin_login
def adminIndex():
    user_obj = User.query.all()
    return render_template("admin/home.html", userList=user_obj)


# 管理员登录     get
@admin.route("/login")
def adminLogin_get():
    if "admin_id" in session:
        return redirect(url_for("admin.adminIndex"))
    return render_template("admin/login.html")


# 管理员登录   post
@admin.route("/login", methods=["POST"])
def adminLogin_post():
    admin = request.form["admin-account"]
    pwd = request.form["admin-pwd"]
    if admin == "admin" and pwd == "admin":
        session["admin_id"] = admin
        return redirect(url_for("admin.adminIndex"))
    return render_template("admin/login.html", warning="账户密码错误")


# 管理员退出
@admin.route("/logout")
def adminLogout():
    session.pop('admin_id', None)
    return redirect(url_for("admin.adminLogin_get"))


# 管理员 用户管理
# 封禁用户
@admin.route("/userBan")
@admin_login
def admin_userBan():
    userid = request.args["userid"]
    user_obj = User.query.filter_by(id=userid).first()
    if user_obj:
        user_obj.status = False;
        db.session.commit()
        return redirect(url_for("admin.adminIndex"))
    return jsonify({"msg": "Error！This account does not exist"})


# 激活用户
@admin.route("/userAct")
@admin_login
def admin_userAct():
    userid = request.args["userid"]
    user_obj = User.query.filter_by(id=userid).first()
    if user_obj:
        user_obj.status = True;
        db.session.commit()
        return redirect(url_for("admin.adminIndex"))
    return jsonify({"msg": "Error！This account does not exist"})


# 酒店管理
@admin.route("/adminHotel")
@admin_login
def adminHotel():
    hotel_obj = Hotel.query.all()
    return render_template("admin/hotel.html", hotelList=hotel_obj)


# 添加酒店 get
@admin.route("/adminHotel_add")
@admin_login
def hotelAdd_get():
    return render_template("admin/hotel/add.html")


# 酒店添加 post
@admin.route("/adminHotel_add", methods=["POST"])
def hotelAdd_post():
    name = request.form["hotelname"]
    price = request.form["hotelprice"]
    picture = request.files["hotelpicture"]
    info = request.form["hotelinfo"]
    if name == "" and price == "" and picture == "" and info == "":
        return render_template("admin/hotel/add.html", warning="所有都不能为空！")
    # 上传的文件夹
    upload = basedir+'/App/static/images/up_picture/'
    # 给文件名加前缀
    randname = time.strftime("%Y%m%d%H%M%S-", time.localtime())
    # 上传至本地的路径
    image = upload+ randname + picture.filename
    # 保存至本地
    picture.save(image)
    # 存入数据库的图片路径
    picture_link = base_server+'/static/images/up_picture/' + randname + picture.filename
    hotel_obj = Hotel(name=name,price=price,picture_link=picture_link,info=info)
    db.session.add(hotel_obj)
    db.session.commit()
    return redirect(url_for("admin.adminHotel"))


# 酒店信息修改    get
@admin.route("/adminHotel_mod")
@admin_login
def hotelMod_get():
    hotelId = request.args["hotelid"]
    hotel_obj = Hotel.query.filter_by(id=hotelId).first()
    if not hotel_obj:
        return jsonify({"msg": "Error！This Hotel dose not exist"})
    return render_template("admin/hotel/mod.html", hotelInfo=hotel_obj)


# 酒店信息修改  post
@admin.route("/adminHotel_mod", methods=["POST"])
def hotelMod_post():
    hotelId = request.form["hotelid"]
    name = request.form["hotelname"]
    price = request.form["hotelprice"]
    picture = request.form["hotelpicture"]
    info = request.form["hotelinfo"]
    hotel_obj = Hotel.query.filter_by(id=hotelId).first()
    if not hotel_obj:
        return jsonify({"msg": "Error！This Hotel dose not exist"})
    hotel_obj.name = name;
    hotel_obj.price = price;
    hotel_obj.picture_link = picture;
    hotel_obj.info = info;
    db.session.commit()
    return redirect(url_for("admin.adminHotel"))


# 酒店信息删除    get
@admin.route("/adminHotel_del/<int:hotelid>")
@admin_login
def hotelDel(hotelid):
    hotel_obj = Hotel.query.filter_by(id=hotelid).first()
    if hotel_obj:
        db.session.delete(hotel_obj)
        db.session.commit()
        return redirect(url_for("admin.adminHotel"))
    return jsonify({"msg": "Error！This Hotel dose not exist"})


# -----------------------------
# 景点管理
@admin.route("/adminAttractions")
@admin_login
def adminAttractions():
    attractions_obj = Attractions.query.all()
    return render_template("admin/attractions.html", attractionsList=attractions_obj)


# 添加景点 get
@admin.route("/adminAttractions_add")
@admin_login
def attractionsAdd_get():
    return render_template("admin/attractions/add.html")


# 景点添加 post
@admin.route("/adminAttractions_add", methods=["POST"])
def attractionsAdd_post():
    name = request.form["attractionsname"]
    price = request.form["attractionsprice"]
    picture = request.files["attractionspicture"]
    info = request.form["attractionsinfo"]

    if name == "" and price == "" and picture == "" and info == "":
        return render_template("admin/attractions/add.html", warning="所有都不能为空！")

    # 上传的文件夹
    upload = basedir + '/App/static/images/up_picture/attractions/'
    # 给文件名加前缀
    randname = time.strftime("%Y%m%d%H%M%S-", time.localtime())
    # 上传至本地的路径
    image = upload + randname + picture.filename
    # 保存至本地
    picture.save(image)
    # 存入数据库的图片路径
    picture_link = base_server+'/static/images/up_picture/attractions/' + randname + picture.filename

    attractions_obj = Attractions(name=name, price=price, picture_link=picture_link, info=info)
    db.session.add(attractions_obj)
    db.session.commit()
    return redirect(url_for("admin.adminAttractions"))


# 景点信息修改    get
@admin.route("/adminAttractions_mod")
@admin_login
def attractionsMod_get():
    attractionsId = request.args["attractionsid"]
    attractions_obj = Attractions.query.filter_by(id=attractionsId).first()
    if not attractions_obj:
        return jsonify({"msg": "Error！This Attractions dose not exist"})
    return render_template("admin/attractions/mod.html", attractionsInfo=attractions_obj)


# 景点信息修改  post
@admin.route("/adminAttractions_mod", methods=["POST"])
def attractionsMod_post():
    attractionsId = request.form["attractionsid"]
    name = request.form["attractionsname"]
    price = request.form["attractionsprice"]
    picture = request.form["attractionspicture"]
    info = request.form["attractionsinfo"]
    attractions_obj = Attractions.query.filter_by(id=attractionsId).first()
    if not attractions_obj:
        return jsonify({"msg": "Error！This Attractions dose not exist"})
    attractions_obj.name = name;
    attractions_obj.price = price;
    attractions_obj.picture_link = picture;
    attractions_obj.info = info;
    db.session.commit()
    return redirect(url_for("admin.adminAttractions"))


# 景点信息删除    get
@admin.route("/adminAttractions_del/<int:attractionsid>")
@admin_login
def attractionsDel(attractionsid):
    attractions_obj = Attractions.query.filter_by(id=attractionsid).first()
    if attractions_obj:
        db.session.delete(attractions_obj)
        db.session.commit()
        return redirect(url_for("admin.adminAttractions"))
    return jsonify({"msg": "Error！This Attractions dose not exist"})

# 景点评论
@admin.route("/attrcomms")
@admin_login
def attrComm():
    attr_obj = Attrcomm.query.all()
    return render_template("admin/comms/attractions.html",comm_list = attr_obj)

# 删除景点评论
@admin.route("/attrBan")
@admin_login
def attrBan():
    attrid = request.args["commid"]
    obj = Attrcomm.query.filter_by(id=attrid).first()
    if obj:
        db.session.delete(obj)
        db.session.commit()
        return redirect(url_for("admin.attrComm"))
    return "<script>alert('删除失败');history.go(-1)</script>"


# 酒店评论
@admin.route("/hotelcomms")
@admin_login
def hotelComm():
    hotel_obj = Hotelcomm.query.all()
    return render_template("admin/comms/hotel.html",comm_list = hotel_obj)
# 删除酒店评论
@admin.route("/hotelBan")
@admin_login
def hotelBan():
    hotelid = request.args["commid"]
    obj = Hotelcomm.query.filter_by(id=hotelid).first()
    if obj:
        db.session.delete(obj)
        db.session.commit()
        return redirect(url_for("admin.hotelComm"))
    return "<script>alert('删除失败');history.go(-1)</script>"






