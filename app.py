from flask import Flask, render_template, url_for, session, request, jsonify, redirect
from app import models
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from datetime import timedelta
import hashlib as h
import json
from datetime import datetime
from flask_cors import CORS
from dateutil.parser import parse
import random
import string
from app import create_app, db
from src.app.models.models import (
  
    DiamondTasks,
    Diamonds,
    LiveChat,
    LiveChatRes,
    Notifications,
    Stake,
    Team,
    Users,
    
    Withdrawals,
)
from dotenv import load_dotenv


UPLOAD_FOLDER = 'uploads'  # Create a folder named 'uploads' in your Flask app directory

load_dotenv()

app = create_app(os.getenv("BOILERPLATE_ENV") or "dev")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.app_context().push()
app.permanent_session_lifetime = timedelta(weeks=1)
migrate = Migrate(app, db)


def hashblock(req):
    encoded_block = json.dumps(req, sort_keys=True).encode()
    block_encryption = h.sha256()
    block_encryption.update((encoded_block))
    return block_encryption.hexdigest()


# Function to generate a random referral code
def generate_referral_code(length=6):
    # Define the characters that can be in the code
    characters = string.ascii_uppercase + string.digits

    # Generate a random code by sampling from the character set
    code = "".join(random.choice(characters) for _ in range(length))

    return code


@app.route("/edit_user", methods=["POST"])
def edit_user():
    if request.method == "POST":
        country = request.form['country']
        gender = request.form['gender']
        address = request.form['address']
        user_id = request.form["user_id"]
        # Check if a file was uploaded
        if 'image' in request.files:
            image = request.files['image']
            # You can save the image to your server or process it as needed
            if image.filename != '':
                # Create an uploads folder if it doesn't exist
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])
                # Save the uploaded image to the uploads folder
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                image.save(image_path)

        

                account = Users.query.filter_by(user_id=user_id).first()
                if account:
                    account.country = country
                    account.address = address
                    account.gender = gender
                    account.image = image.filename
                    notif = Notifications(
                        user_id=user_id, message="Profile Updated Successifully"
                    )
                    db.session.add(notif)
                    db.session.commit()
                    return jsonify({"message": "success"})
            account = Users.query.filter_by(user_id=user_id).first()
            if account:
                account.country = country
                account.address = address
                account.gender = gender
               
                notif = Notifications(
                    user_id=user_id, message="Profile Updated Successifully"
                )
                db.session.add(notif)
                db.session.commit()
                return jsonify({"message": "success"})
        account = Users.query.filter_by(user_id=user_id).first()
        if account:
            account.country = country
            account.address = address
            account.gender = gender
         
            notif = Notifications(
                user_id=user_id, message="Profile Updated Successifully"
            )
            db.session.add(notif)
            db.session.commit()
            #print("duum")
            return jsonify({"message": "success"})

        return jsonify({"message": "issue"})


@app.route("/me", methods=["POST"])
def me():
    if request.method == "POST":
        data = request.get_json()
        user_id = data["user_id"]

        response = {}

        account = Users.query.filter_by(user_id=user_id).first()
        if account:
            response["name"] = account.name
            response["email"] = account.email
            response["contact"] = account.contact
            response["country"] = account.country
            response["address"] = account.address
            response["gender"] = account.gender
            response["image"] = "account.image"
            response["referral_code"] = account.referral_code
            response["referrer"] = "account.referrer"
            response["user_id"] = account.user_id
            print("goo0000")
            return jsonify({"me": response})
        print("no")
        return jsonify({"message": "issue"})


@app.route("/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        data = request.get_json()

        name = data["name"]
        email = data["email"]
        password = data["password"]
        contact = data["contact"]
        country = data["country"]
        state = data["state"]
        city = data["city"]
        address = data["address"]
        gender = data["gender"]
        referrer = data["referrer"]
        image = ""
        referral_code = generate_referral_code()

        user_id = hashblock(
            str(email) + str(password) + str(referral_code) + str(datetime.now())
        )

        account = Users.query.filter_by(email=email).first()
        if account:
            return jsonify({"message": "exist"})
        user = Users(
            name=name,
            email=email,
            password=password,
            contact=contact,
            country=country,
            address=address,
            gender=gender,
            image=image,
            referral_code=referral_code,
            referrer=referrer,
            user_id=user_id,
            state=state,
            city=city
        )

        ref_bounus = Diamonds.query.filter_by(referral_code=referrer).first()
        if ref_bounus:
            ref_bounus.amount = str(float(ref_bounus.amount) + 10)

        user_bounus = Diamonds(
            user_id=user_id, amount=str(10), referral_code=referral_code
        )
        user_stake = Stake(user_id=user_id, amount=str(0))
        user_team = Team(user_id=user_id, name=name, referrer=referrer)
        notif = Notifications(
            user_id=user_id,
            message="welcome to Mega Diamond Miner, your have been Rewarded with 10 Diamonds for joining Diamond Minner \
                              refer others with your referral code to get boununs of 10 more Diamonds for each referral",
        )
        diaadd = DiamondTasks(user_id=user_id,task1="",task2="",task3="",task4="", dia1="",dia2="",dia3="",dia4="")
        db.session.add(diaadd)
        db.session.add(user_stake)
        db.session.add(user_bounus)
        db.session.add(user)
        db.session.add(user_team)
        db.session.add(notif)

        db.session.commit()
        return jsonify({"message": "success", "user_id": user_id})


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        email = data["email"]
        password = data["password"]

        check_user = Users.query.filter_by(email=email, password=password).first()
        if check_user:
            #print("id", check_user.user_id, email, password)
            return jsonify({"message": "success", "user_id": check_user.user_id})
        print("not success")
        return jsonify({"message": "no_user"})


##########################################################################################
#
###########################################################################################


@app.route("/add_diamond", methods=["POST"])
def add_diamond():
    if request.method == "POST":
        data = request.get_json()
        user_id = data["user_id"]
        amount = data["amount"]
        dia = data["dia"]

        add_dia = Diamonds.query.filter_by(user_id=user_id).first()
        if add_dia:
            add_dia.amount = float(add_dia.amount) + float(amount)
            diatask = DiamondTasks.query.filter_by(user_id = user_id).first()
            if diatask:
                if int(dia) == 1:
                    diatask.dia1 = str(datetime.now())

                elif int(dia) == 2:
                    diatask.dia2 = str(datetime.now())

                elif int(dia) == 3:
                    diatask.dia3 = str(datetime.now())

                elif int(dia) == 4:
                    diatask.dia4 = str(datetime.now())

                elif int(dia) == 5:
                    diatask.task1 = str(datetime.now())

                elif int(dia) == 6:
                    diatask.task2 = str(datetime.now())

                elif int(dia) == 7:
                    diatask.task3 = str(datetime.now())

                elif int(dia) == 8:
                    diatask.task4 = str(datetime.now())

            db.session.commit()
            return jsonify({"message": "success"})
        print("not success")
        return jsonify({"message": "issue"})


@app.route("/add_stake", methods=["POST"])
def add_stake():
    if request.method == "POST":
        data = request.get_json()
        user_id = data["user_id"]
        amount = data["amount"]

        add_stake = Stake.query.filter_by(user_id=user_id).first()
        if add_stake:
            add_stake.amount = float(add_stake.amount) + float(amount)
            sub_dia = Diamonds.query.filter_by(user_id=user_id).first()
            subamount = float(sub_dia.amount)
            sub_dia.amount = subamount - float(amount)
            notif = Notifications(
                user_id=user_id,
                message=f"You have successully staked {str(float(add_stake.amount)+float(amount))} diamonds so far, your remaining Diamonds Non-staked is {subamount}",
            )
            db.session.add(notif)
            db.session.commit()
            return jsonify({"message": "success"})
        print("not success")
        return jsonify({"message": "issue"})


##########################################################################################
#
###########################################################################################


@app.route("/get_diamonds", methods=["POST"])
def get_diamonds():
    # if request.method == "POST":
    data = request.get_json()
    user_id = data["user_id"]
   

    get_dia = Diamonds.query.filter_by(user_id=user_id).first()
    
    amount = str(get_dia.amount)

    return jsonify({"amount": amount})
   
   


@app.route("/get_stake", methods=["POST"])
def get_stake():
    # if request.method == "POST":
    data = request.get_json()
    user_id = data["user_id"]
    response = []
    add_stake = Stake.query.filter_by(user_id=user_id).all()
    if add_stake:
        for st in add_stake:
            amount = " Diamonds:  " + str(st.amount)
            created = " Staked:  " + str(st.Created)
            response.append({"amount": amount, "created": created})
    return jsonify(response)
   


#############################################################################################
#
#############################################################################################


@app.route("/get_dia", methods=["POST"])
def get_dia():
    data = request.get_json()
    user_id = data["user_id"]

    staked = Stake.query.filter_by(user_id=user_id).first()
    
    task = DiamondTasks.query.filter_by(user_id=user_id).first()
    amount_dia = Diamonds.query.filter_by(user_id=user_id).first()
    amount_dia.amount
    response = {"dia1": True, "dia2": True, "dia3": True, "dia4": True, "task1": True, "task2": True, "task3": True, "task4": True, "amount": amount_dia.amount, "stake": staked.amount}
    now = datetime.now()

    # Calculate the difference of 24 hours
    difference = timedelta(seconds=10)

    if is_date(task.task1):
        date1 = parse(task.task1)

        if (now - date1) >= difference:
            response["task1"] = False
        else:
            response["task1"] = True

    if is_date(task.task2):
        date2 = parse(task.task2)

        if now - date2 >= difference:
            response["task2"] = False
        else:
            response["task2"] = True

    if is_date(task.task3):
        date3 = parse(task.task3)

        if now - date3 >= difference:
            response["task3"] = False
        else:
            response["task3"] = True

    if is_date(task.task4):
        date4 = parse(task.task4)

        if now - date4 >= difference:
            response["task4"] = False
        else:
            response["task4"] = True

    if is_date(task.dia1):
        date1 = parse(task.dia1)

        if (now - date1) >= difference:
            response["dia1"] = True
        else:
            response["dia1"] = False

    if is_date(task.dia2):
        date2 = parse(task.dia2)

        if now - date2 >= difference:
            response["dia2"] = True
        else:
            response["dia2"] = False

    if is_date(task.dia3):
        date3 = parse(task.dia3)

        if now - date3 >= difference:
            response["dia3"] = True
        else:
            response["dia3"] = False

    if is_date(task.dia4):
        date4 = parse(task.dia4)

        if now - date4 >= difference:
            response["dia4"] = True
        else:
            response["dia4"] = False
    
    
    return jsonify(response)




##############################################################################################
#
##############################################################################################


@app.route("/get_team", methods=["POST"])
def get_team():
    if request.method == "POST":

        data = request.get_json()
        user_id = data["user_id"]

        user_account = Users.query.filter_by(user_id=user_id).first()
        team = Team.query.filter_by(referrer=user_account.referral_code).all()

        response = []
        if team:
            for t_m in team:
                response.append({"name": t_m.name, "joined": t_m.Created})

        return jsonify(response)




@app.route("/get_notif", methods=["POST"])
def get_notif():
    if request.method == "POST":

        data = request.get_json()
        user_id = data["user_id"]

        ntf = Notifications.query.filter_by(user_id=user_id).all()

        response = []
        if ntf:
            for t_m in ntf:
                response.append({"message": t_m.message, "created": t_m.Created})

        return jsonify(response)


##############################################################################################
#
##############################################################################################


@app.route("/get_withdrawals", methods=["POST"])
def get_withdrawals():
    if request.method == "POST":
        data = request.get_json()
        user_id = data["user_id"]
        history = Withdrawals.query.filter_by(user_id=user_id).all()
        response = []
        if history:
            for t_m in history:
                response.append({"address": t_m.address, "amount": str(t_m.amount), "created": str(t_m.Created)})
        #print(response)
        return jsonify(response)


@app.route("/add_withdrawals", methods=["POST"])
def add_withdrawals():
    if request.method == "POST":
        data = request.get_json()
        user_id = data["user_id"]
        address = data["address"]
        dia_amt = data["amount"]
        diamonds = Diamonds.query.filter_by(user_id=user_id).first()
        user =  Users.query.filter_by(user_id=user_id).first()
        if float(dia_amt) <= float(diamonds.amount):
            history = Withdrawals(user_id=user_id, amount=dia_amt, address=address, name = user.name)
            diamonds.amount = float(diamonds.amount) - float(dia_amt)
            notif = Notifications(
                user_id=user_id,
                message=f"You have uccessully withdrew {str(float(dia_amt)*0.0246)}, equevalence of {dia_amt}",
            )
            db.session.add(notif)
            db.session.add(history)
            db.session.commit()

            return jsonify({"message": "success"})


##############################################################################################
#
##############################################################################################


@app.route("/add_chat", methods=["POST"])
def chat():
    if request.method == "POST":
        data = request.get_json()
        subject = data["subject"]
        message = data["message"]
        user_id = data["user_id"]
        user =  Users.query.filter_by(user_id=user_id).first()
        chatMessage = LiveChat(user_id=user_id, subject=subject, message=message, name=user.name)
        notif = Notifications(
                user_id=user_id,
                message=f"{subject} message sent successifully",
            )
        db.session.add(notif)
        db.session.add(chatMessage)
        db.session.commit()
        return jsonify({"message": "success"})


@app.route("/chatRes", methods=["POST"])
def chatRes():
    if request.method == "POST":
        
        message = request.form["response"]
        referral_code = session["referral_code"]
        user = Users.query.filter_by(referral_code=referral_code).first()
        res = LiveChatRes(user_id=user.user_id, message=message)
        notif = Notifications(
        user_id=user.user_id,
        message=f"{str(message)}",
        )
        db.session.add(notif)
        db.session.add(res)
        db.session.commit()
        return redirect(url_for('user', referral_code=referral_code))


@app.route("/user/<referral_code>")
def user(referral_code):
    session["referral_code"] = referral_code
    user = Users.query.filter_by(referral_code=referral_code).first()
    notifs = Notifications.query.filter_by(user_id=user.user_id).all()
    history = Withdrawals.query.filter_by(user_id=user.user_id).all()
    return render_template("user.html", user=user, history=history, notifs=notifs)

@app.route("/home")
def home():
    if "referral_code" in session:
        referral_code = session["referral_code"]
        user = Users.query.filter_by(referral_code=referral_code).first()
        history = Withdrawals.query.filter_by(user_id=user.user_id).all()
        diamonds = Diamonds.query.filter_by(user_id=user.user_id).first()
        stake = Stake.query.filter_by(user_id=user.user_id).first()
        return render_template("index.html", user=user, history=history, diamonds=diamonds.amount, stake=stake.amount)
    return render_template("index.html", user=[], history=[], diamond="", stake="")

@app.route("/retrieve", methods = ["POST"])
def retrieve():
    if request.method == "POST":
        referral_code = request.form["referral_code"]
        session.pop("referral_code", None)
        session["referral_code"] = referral_code
    return redirect(url_for('home'))



@app.route("/users")
def users():
    session.pop("referral_code", None)
    users = Users.query.all()
    return render_template("users.html", users=users)

@app.route("/complaints")
def complaints():
    complaints = LiveChat.query.all()
    return render_template("complaints.html", complaints=complaints)

@app.route("/wr")
def wr():
    wr = Withdrawals.query.all()
    return render_template("wr.html", wr=wr)

@app.route("/complaint/<user_id>/<created>")
def complaint(user_id,created):
    user = Users.query.filter_by(user_id=user_id).first()
    session["referral_code"] = user.referral_code
    complaint = LiveChat.query.filter_by(user_id=user_id, Created=created).first()
    return render_template("complaint.html", complaint=complaint)


@app.route("/admin_add_diamond", methods = ["POST"])
def admin_add_diamond():
    if request.method=="POST":
        amount = request.form["amount"]
        referral_code = session["referral_code"]
        user = Users.query.filter_by(referral_code=referral_code).first()
        add_dia = Diamonds.query.filter_by(user_id=user.user_id).first()
        if add_dia:
            add_dia.amount = float(add_dia.amount) + float(amount)
            notif = Notifications(
            user_id=user.user_id,
            message=f"Congratulations, Admin have added {str(amount)} diamonds to you.",
            )
            db.session.add(notif)
            db.session.commit()
            return redirect(url_for('user', referral_code=referral_code))

@app.route("/send_notif", methods = ["POST"])
def send_notif():
    if request.method=="POST":
        msg = request.form["notif"]
        referral_code = session["referral_code"]
        user = Users.query.filter_by(referral_code=referral_code).first()
        notif = Notifications(
            user_id=user.user_id,
            message=f"{msg}",
        )
        db.session.add(notif)
        db.session.commit()



def is_date(string, fuzzy=True):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except:
        return False

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=5000)
