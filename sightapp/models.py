from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# sightsee models

class Admin(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(255),nullable=False,unique=True)
    password = db.Column(db.String(255),nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)


class State(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False)
    # set relationship
    state_lgas = db.relationship('Lga',backref='state')
    state_resorts = db.relationship('Resort',backref='state_deets')


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    firstname = db.Column(db.String(255),nullable=False)
    lastname = db.Column(db.String(255),nullable=False)
    phone = db.Column(db.String(20),nullable=True)
    password = db.Column(db.String(255),nullable=False)
    bio = db.Column(db.Text,nullable=True)
    email = db.Column(db.String(255),nullable=False,unique=True)
    dp = db.Column(db.String(255))
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    status =db.Column(db.Enum('active','disabled'),nullable=False, server_default=("active"))

    # set relationship
    orders = db.relationship('Order',backref='user')
    comments = db.relationship('Comment',backref='user')


class Lga(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False)
    state_id = db.Column(db.Integer,db.ForeignKey('state.id'))
    # set relationship
    resorts = db.relationship('Resort',backref='lga')


class Order(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    order_date = db.Column(db.DateTime,default=datetime.utcnow)
    total_amount = db.Column(db.Numeric(10,2))
    status = db.Column(db.Enum('completed','pending','cancelled'),server_default=("pending"))
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    # set relationship
    payment = db.relationship('Payment',backref='order',uselist=False)
    details = db.relationship('OrderDetail',backref='theorder')


class Payment(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    payment_date = db.Column(db.DateTime,default=datetime.utcnow)
    amount = db.Column(db.Numeric(10,2))
    payment_method = db.Column(db.String(255))
    order_id = db.Column(db.Integer,db.ForeignKey('order.id'))


class Resort(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(255),nullable=False)
    phone = db.Column(db.String(20),nullable=True)
    description = db.Column(db.Text,nullable=True)
    cover_picture = db.Column(db.String(255))
    price = db.Column(db.Numeric(10,2))
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    status =db.Column(db.Enum('active','disabled'),nullable=False, server_default=("active")) 
    available = db.Column(db.Enum('active','disabled'),nullable=False,server_default='disabled')
    lga_id = db.Column(db.Integer,db.ForeignKey('lga.id'))
    state_id = db.Column(db.Integer,db.ForeignKey('state.id'))
    # set relationship
    resort_pictures = db.relationship('ResortPicture',backref='resort')
    order_details = db.relationship('OrderDetail',backref='resort')    
    comments = db.relationship('Comment',backref='resort')


class ResortPicture(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    picture_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    resort_id = db.Column(db.Integer,db.ForeignKey('resort.id'))


class OrderDetail(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    ticket_number = db.Column(db.String(255),nullable=False)
    price = db.Column(db.Numeric(10,2))
    ticket_status = db.Column(db.Enum('invalid','valid','used'),default='invalid')
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    order_id = db.Column(db.Integer,db.ForeignKey('order.id'))
    resort_id = db.Column(db.Integer,db.ForeignKey('resort.id'))


class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    resort_id = db.Column(db.Integer,db.ForeignKey('resort.id'))
    comment = db.Column(db.Text,nullable=False)
    status = db.Column(db.Enum('active','disabled'))
    created_at = db.Column(db.DateTime,default=datetime.utcnow)


