from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from app import db

class Users(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.String(500))
    name = db.Column("name", db.String(500))
    email = db.Column("email", db.String(500))
    password = db.Column("password", db.String(500))
    contact = db.Column("contact", db.String(500))
    address = db.Column("address", db.String(500))
    country = db.Column("country", db.String(500))
    gender = db.Column("gender", db.String(500))
    image = db.Column("image", db.String(500))
    referral_code = db.Column("referral_code", db.String(500))
    referrer = db.Column("referrer", db.String(500))
    Created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, name, email, password, user_id, contact, address, country, referrer, gender, referral_code, image):
        self.name = name
        self.email = email
        self.password = password
        self.user_id = user_id
        self.country = country
        self.contact = contact
        self.address = address
        self.referral_code = referral_code
        self.referrer = referrer
        self.gender = gender
        self.image = image


class Diamonds(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.String(500))
    amount = db.Column("amount", db.String(500))
    referral_code = db.Column("referral_code", db.String(500))
    #date = db.Column("date", db.String(500))
    #time = db.Column("time", db.String(500))
    #attendees = db.Column("attendees", db.String(500))
    Created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id, amount, referral_code):
        self.user_id = user_id
        self.amount = amount
        self.referral_code = referral_code

class Stake(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.String(500))
    amount = db.Column("amount", db.String(500))
    Created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id, amount):
        self.user_id = user_id
        self.amount = amount


class Notifications(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.String(500))
    message = db.Column("message", db.String(500))
    Created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message

class Team(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.String(500))
    name = db.Column("name", db.String(500))
    referrer = db.Column("referrer", db.String(500))
    Created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id, name, referrer):
        self.user_id = user_id
        self.name = name
        self.referrer = referrer


class LiveChat(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.String(500))
    subject = db.Column("subject", db.String(500))
    message = db.Column("message", db.String(500))
    Created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id, subject, message):
        self.user_id = user_id
        self.subject = subject
        self.message = message



class LiveChatRes(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.String(500))
    subject = db.Column("subject", db.String(500))
    message = db.Column("message", db.String(500))
    Created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id, subject, message):
        self.user_id = user_id
        self.subject = subject
        self.message = message




class DiamondTasks(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.String(500))
    dia1 = db.Column("dia1", db.String(500))
    dia2 = db.Column("dia2", db.String(500))
    dia3 = db.Column("dia3", db.String(500))
    dia4 = db.Column("dia4", db.String(500))
    task1 = db.Column("task1", db.String(500))
    task2 = db.Column("task2", db.String(500))
    task3 = db.Column("task3", db.String(500))
    task4 = db.Column("task4", db.String(500))
    Created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id, task1, task2, task3, task4, dia1, dia2, dia3, dia4):
        self.user_id = user_id
        self.dia1 = dia1
        self.dia2 = dia2
        self.dia3 = dia3
        self.dia4 = dia4
        self.task1 = task1
        self.task2 = task2
        self.task3 = task3
        self.task4 = task4

"""
class DiamondTask2(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.String(500))
    Created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id):
        self.user_id = user_id


class DiamondTask3(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.String(500))
    Created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id):
        self.user_id = user_id


class DiamondTask4(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.String(500))
    Created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id):
        self.user_id = user_id


"""
       
class Withdrawals(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.String(500))
    amount = db.Column("amount", db.String(500))
    address = db.Column("address", db.String(500))
    Created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id, amount, address):
        self.user_id = user_id
        self.amount= amount
        self.address = address