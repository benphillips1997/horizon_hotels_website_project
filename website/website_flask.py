#written by Ben Phillips - 21067833

from flask import Flask, jsonify, render_template, redirect, url_for, request, session
from passlib.hash import sha256_crypt
import mysql.connector, dbfunc, db_connection as db
from datetime import datetime, date, timedelta
import math

app = Flask(__name__)

app.secret_key = "Secret_Key"

db.check_room_count()


#pops temporary sessions used when booking
def pop_temp():
    tempsessions = ["tempcheckindate", "tempcheckoutdate", "tempguestnum", "tempcity", "tempstandardcost", "tempdoublecost", "tempfamilycost"]
    for temp in tempsessions:
        session.pop(temp, None)


@app.route('/')
def index():
    if "email" in session:
        loggedIn = True
    else: 
        loggedIn = False
    return render_template("index.html", loggedIn = loggedIn)


@app.route('/login')
def login():
    if "email" in session:
        loggedIn = True
    else: 
        loggedIn = False
    return render_template("login.html", loggedIn = loggedIn, message = False)


@app.route('/logout')
def logout():
    session.pop("email", None)
    return redirect(url_for("index"))


@app.route('/loginsubmit', methods = ['POST', 'GET'])
def loginsubmit():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        data = db.retrieve_user(email)
        if data != False:
            check_hash = sha256_crypt.verify(password, data["password"])
        if data != False and check_hash:
            session["email"] = email
            return redirect(url_for('account', name = data["firstname"]))
        else:
            print("Invalid credentials")
            return render_template("login.html", message = "Invalid credentials")
    else:
        email = request.args.get('email')
        password = request.args.get('password')
        data = db.retrieve_user(email)
        if data != False:
            check_hash = sha256_crypt.verify(password, data["password"])
        if data != False and check_hash:
            session["email"] = email
            return redirect(url_for('account', name = data["firstname"]))
        else:
            print("Invalid credentials")
            return render_template("login.html", message = "Invalid credentials")


@app.route('/booking')
def booking():
    if "email" in session:
        cities = db.retrieve_accommodation_cities()
        datetoday = date.today().strftime("%Y-%m-%d")
        datein90days = (date.today() + timedelta(days = 90)).strftime("%Y-%m-%d")
        datein120days = (date.today() + timedelta(days = 120)).strftime("%Y-%m-%d")
        return render_template("booking.html", citylist = cities, loggedIn = True, todaysdate = str(datetoday), in90days = str(datein90days), in120days = str(datein120days))
    else: 
        return render_template("login.html", message = "You must login to make a booking")


@app.route('/bookingsubmit', methods = ['POST', 'GET'])
def bookingsubmit():
    if "email" in session:
        loggedIn = True
    else: 
        loggedIn = False
    if request.method == 'POST':
        checkindate = request.form['checkindate']
        checkoutdate = request.form['checkoutdate']
        guestnum = int(request.form['guestnum'])
        guestnumdiv3 = int(guestnum / 3)
        city = request.form['citylist']
        numofdays = datetime.strptime(checkoutdate, '%Y-%m-%d') - datetime.strptime(checkindate, '%Y-%m-%d')
        days_in_advance = (datetime.strptime(checkindate, '%Y-%m-%d') - datetime.now()).days + 1
        data = db.retrieve_accommodation(city)
        if (datetime.strptime(checkindate, '%Y-%m-%d').month >= 4 and datetime.strptime(checkindate, '%Y-%m-%d').month <= 9):
            rate = int(data["peakrate"])
        else:
            rate = int(data["offpeakrate"])
        price = rate * numofdays.days
        if price == 0:
            price = rate
        standardroom = price
        if guestnum == 2:
            doubleroom = price + price * 0.3
        else:
            doubleroom = price + price * 0.2
        familyroom = price + price * 0.5
        discount = 1
        if days_in_advance > 80:
            discount *= 0.8
        elif days_in_advance > 60:
            discount *= 0.9
        elif days_in_advance > 45:
            discount *= 0.95
        standardroom *= discount
        doubleroom *= discount
        familyroom *= discount
        session["tempcheckindate"] = checkindate
        session["tempcheckoutdate"] = checkoutdate
        session["tempguestnum"] = guestnum
        session["tempcity"] = city
        session["tempstandardcost"] = standardroom
        session["tempdoublecost"] = doubleroom
        session["tempfamilycost"] = familyroom
        totalrooms = int(data["numofstandardrooms"]) + int(data["numofdoublerooms"]) + int(data["numoffamilyrooms"])
        if "currency" not in session:
            session["currency"] = "gbp"
        return render_template('bookingcheck.html', checkin = checkindate, checkout = checkoutdate, guestnum = guestnum, guestnumdiv3 = guestnumdiv3, \
            city = city, standardcost = int(standardroom), doublecost = int(doubleroom), familycost = int(familyroom), \
                numOfRooms = totalrooms, loggedIn = loggedIn, currency = session["currency"])
    else:
        checkindate = request.args.get('checkindate')
        checkoutdate = request.args.get('checkoutdate')
        guestnum = int(request.args.get('guestnum'))
        guestnumdiv3 = int(guestnum / 3)
        city = request.args.get('citylist')
        numofdays = datetime.strptime(checkoutdate, '%Y-%m-%d') - datetime.strptime(checkindate, '%Y-%m-%d')
        days_in_advance = (datetime.strptime(checkindate, '%Y-%m-%d') - datetime.now()).days + 1
        data = db.retrieve_accommodation(city)
        if (datetime.strptime(checkindate, '%Y-%m-%d').month >= 4 and datetime.strptime(checkindate, '%Y-%m-%d').month <= 9):
            rate = int(data["peakrate"])
        else:
            rate = int(data["offpeakrate"])
        price = rate * numofdays.days
        if price == 0:
            price = rate
        standardroom = price
        if guestnum == 2:
            doubleroom = price + price * 0.3
        else:
            doubleroom = price + price * 0.2
        familyroom = price + price * 0.5
        discount = 1
        if days_in_advance > 80:
            discount *= 0.8
        elif days_in_advance > 60:
            discount *= 0.9
        elif days_in_advance > 45:
            discount *= 0.95
        standardroom *= discount
        doubleroom *= discount
        familyroom *= discount
        session["tempcheckindate"] = checkindate
        session["tempcheckoutdate"] = checkoutdate
        session["tempguestnum"] = guestnum
        session["tempcity"] = city
        session["tempstandardcost"] = standardroom
        session["tempdoublecost"] = doubleroom
        session["tempfamilycost"] = familyroom
        totalrooms = int(data["numofstandardrooms"]) + int(data["numofdoublerooms"]) + int(data["numoffamilyrooms"])
        if "currency" not in session:
            session["currency"] = "gbp"
        return render_template('bookingcheck.html', checkin = checkindate, checkout = checkoutdate, guestnum = guestnum, guestnumdiv3 = guestnumdiv3, \
            city = city, standardcost = int(standardroom), doublecost = int(doubleroom), familycost = int(familyroom), \
                numOfRooms = totalrooms, loggedIn = loggedIn, currency = session["currency"])


@app.route('/bookingend', methods = ["POST", "GET"])
def bookingend():
    if "email" in session:
        if request.method == "POST":
            room = request.form["room"]
            date_created = datetime.now().strftime("%Y-%m-%d")
            print(date_created)
            try:
                checkindate = session["tempcheckindate"]
                checkoutdate = session["tempcheckoutdate"]
                numofguests = session["tempguestnum"]
                city = session["tempcity"]
                if room == "Standard":
                    price = session["tempstandardcost"]
                elif room == "Double":
                    price = session["tempdoublecost"]
                elif room == "Family":
                    price = session["tempfamilycost"]
                else: 
                    price = "Error"
                    print("Error getting price has occured")
                pop_temp()
            except:
                cities = db.retrieve_accommodation_cities()
                datetoday = date.today().strftime("%Y-%m-%d")
                datein90days = (date.today() + timedelta(days = 90)).strftime("%Y-%m-%d")
                datein120days = (date.today() + timedelta(days = 120)).strftime("%Y-%m-%d")
                return render_template("booking.html", citylist = cities, loggedIn = True, todaysdate = str(datetoday), \
                    in90days = str(datein90days), in120days = str(datein120days))
            cardholdername = request.form["cardholdername"]
            cardnum = request.form["cardnum"]
            expiry = request.form["expiry"]
            cvv = request.form["cvv"]
            data = db.retrieve_user(session["email"])
            db.make_booking(data["email"], city, checkindate, checkoutdate, numofguests, room, price, date_created)
            if "currency" not in session:
                session["currency"] = "gbp"
            return render_template("bookingend.html", loggedIn = True, checkin = checkindate, checkout = checkoutdate, guestnum = numofguests, \
                destination = city, room = room, price = int(price), currency = session["currency"])
        else:
            room = request.args.get("room")
            date_created = datetime.now().strftime("%Y-%m-%d")
            try:
                checkindate = session["tempcheckindate"]
                checkoutdate = session["tempcheckoutdate"]
                numofguests = session["tempguestnum"]
                city = session["tempcity"]
                if room == "Standard":
                    price = session["tempstandardcost"]
                elif room == "Double":
                    price = session["tempdoublecost"]
                elif room == "Family":
                    price = session["tempfamilycost"]
                else: 
                    price = "Error"
                    print("Error getting price has occured")
                pop_temp()
            except:
                cities = db.retrieve_accommodation_cities()
                datetoday = date.today().strftime("%Y-%m-%d")
                datein90days = (date.today() + timedelta(days = 90)).strftime("%Y-%m-%d")
                datein120days = (date.today() + timedelta(days = 120)).strftime("%Y-%m-%d")
                return render_template("booking.html", citylist = cities, loggedIn = True, todaysdate = str(datetoday), \
                    in90days = str(datein90days), in120days = str(datein120days))
            cardholdername = request.args.get("cardholdername")
            cardnum = request.args.get("cardnum")
            expiry = request.args.get("expiry")
            cvv = request.args.get("cvv")
            data = db.retrieve_user(session["email"])
            db.make_booking(data["email"], city, checkindate, checkoutdate, numofguests, room, price, date_created)
            if "currency" not in session:
                session["currency"] = "gbp"
            return render_template("bookingend.html", loggedIn = True, checkin = checkindate, checkout = checkoutdate, guestnum = numofguests, \
                destination = city, room = room, price = int(price), currency = session["currency"])


@app.route('/signup')
def signup():
    if "email" in session:
        loggedIn = True
    else: 
        loggedIn = False
    return render_template("signup.html", loggedIn = loggedIn, message = False)


@app.route('/signupsubmit', methods = ['POST', 'GET'])
def signupsubmit():
    if "email" in session:
        loggedIn = True
    else: 
        loggedIn = False
    if request.method == 'POST':
        firstname = request.form['firstname']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        pass_hash = sha256_crypt.hash(password)
        number = request.form['number']
        address = request.form['address']
        postcode = request.form['postcode']
        users = db.retrieve_all_users()
        duplicate = False
        if users != False:
            for user in users:
                if email == user["email"]:
                    duplicate = True        
        if duplicate:
            return render_template("signup.html", loggedIn = loggedIn, message = "There is already an account with that email address")
        db.add_user(firstname, surname, email, pass_hash, number, address, postcode)
        session["email"] = email
        return redirect(url_for('account'))
    else:
        firstname = request.args.get('firstname')
        surname = request.args.get('surname')
        email = request.args.get('email')
        password = request.args.get('password')
        pass_hash = sha256_crypt.hash(password)
        number = request.args.get('number')
        address = request.args.get('address')
        postcode = request.args.get('postcode')
        users = db.retrieve_all_users()
        duplicate = False
        if users != False:
            for user in users:
                if email == user["email"]:
                    duplicate = True        
        if duplicate:
            return render_template("signup.html", loggedIn = loggedIn, message = "There is already an account with that email address")
        db.add_user(firstname, surname, email, pass_hash, number, address, postcode)
        session["email"] = email
        return redirect(url_for('account'))


@app.route('/account')
def account():
    if "email" in session:
        data = db.retrieve_user(session["email"])
        usertype = data["usertype"]
        firstname = data["firstname"]
        return render_template("account.html", loggedIn = True, type = usertype, name = firstname)
    else: 
        return render_template("login.html", message = "You must login to access your account")


@app.route('/userbookings')
def userbookings():
    if "email" in session:
        bookings = db.retrieve_booking(session["email"])
        if "currency" not in session:
            session["currency"] = "gbp"
        return render_template("userbookings.html", loggedIn = True, bookings = bookings, m = False, message = False, currency = session["currency"], fee = False)
    else: 
        return render_template("login.html", loggedIn = False, message = "You must login to access that page")


@app.route('/adminbookings')
def adminbookings():
    user_data = db.retrieve_user(session["email"])
    if user_data["usertype"] == "admin":
        if "email" in session:
            bookings = db.retrieve_all_bookings()
            city_list = db.retrieve_accommodation_cities()
            if "currency" not in session:
                session["currency"] = "gbp"
            return render_template("adminbookings.html", loggedIn = True, bookings = bookings, cities = city_list,  currency = session["currency"])
        else:
            return render_template("login.html", loggedIn = False, message = "You must login to access that page")
    else:
        return redirect(url_for("account"))


@app.route('/adminhotels')
def adminhotels():
    user_data = db.retrieve_user(session["email"])
    if user_data["usertype"] == "admin":
        if "email" in session:
            hoteldata = db.retrieve_all_accommodation()
            if "currency" not in session:
                session["currency"] = "gbp"
            return render_template("adminhotels.html", loggedIn = True, hotellist = hoteldata, currency = session["currency"])
        else:
            return render_template("login.html", loggedIn = False, message = "You must login to access that page")
    else:
        return redirect(url_for("account"))


@app.route('/addhotel', methods = ["POST", "GET"])
def addhotel():
    if request.method == "POST":
        city = request.form["city"]
        maxrooms = request.form["rooms"]
        peakrate = request.form["peakrate"]
        offpeakrate = request.form["offpeakrate"]
        db.add_hotel(city, int(maxrooms), peakrate, offpeakrate)
        return redirect('adminhotels')
    else:
        city = request.args.get("city")
        maxrooms = request.args.get("rooms")
        peakrate = request.args.get("peakrate")
        offpeakrate = request.args.get("offpeakrate")
        db.add_hotel(city, int(maxrooms), peakrate, offpeakrate)
        return redirect('adminhotels')


@app.route('/updatehotel', methods = ["POST", "GET"])
def updatehotel():
    if request.method == "POST":
        city = request.form["cityselect"]
        maxrooms = request.form["rooms"]
        peakrate = request.form["peakrate"]
        offpeakrate = request.form["offpeakrate"]
        db.update_hotel(city, int(maxrooms), peakrate, offpeakrate)
        return redirect('adminhotels')
    else:
        city = request.args.get("cityselect")
        maxrooms = request.args.get("rooms")
        peakrate = request.args.get("peakrate")
        offpeakrate = request.args.get("offpeakrate")
        db.update_hotel(city, int(maxrooms), peakrate, offpeakrate)
        return redirect('adminhotels')


@app.route('/deletehotel', methods = ["POST", "GET"])
def deletehotel():
    if request.method == "POST":
        city = request.form["cityselect"]
        db.delete_hotel(city)
        return redirect('adminhotels')
    else:
        city = request.args.get("cityselect")
        db.delete_hotel(city)
        return redirect('adminhotels')


@app.route('/filter/', methods = ["POST", "GET"])
def filter():
    if request.method == "GET":
        q = request.args.get('q')
        data = q.split("_")
        filtered_data = db.retrieve_filtered_bookings(data)
        return jsonify(filtered_data)
    else:
        q = request.form['q']
        data = q.split("_")
        filtered_data = db.retrieve_filtered_bookings(data)
        return jsonify(filtered_data)


@app.route('/changecurrency/', methods = ["POST", "GET"])
def changecurrency():
    if request.method == "GET":
        q = request.args.get('q')
        q = q.split("_")
        session["currency"] = q[0]
        if len(q) > 1:
            if q[1] == "getbooking":
                data = db.retrieve_booking(session["email"])                
                return jsonify(data)
            elif q[1] == "getacc":
                data = db.retrieve_all_accommodation()
                return jsonify(data)
        else:
            return q[0]
    else:
        q = request.form['q']
        q = q.split("_")
        session["currency"] = q[0]
        if len(q) > 1:
            if q[1] == "getbooking":
                data = db.retrieve_booking(session["email"])                
                return jsonify(data)
            elif q[1] == "getacc":
                data = db.retrieve_all_accommodation()
                return jsonify(data)
        else:
            return q[0]


@app.route('/cancelbooking', methods = ["POST", "GET"])
def cancelbooking():
    if request.method == "POST":
        if "email" in session:
            bookingID = request.form["bookingID"]
            email = session["email"]
            data = db.cancel_booking(bookingID, email)
            if "currency" not in session:
                    session["currency"] = "gbp"
            if data != False:
                booked_date = datetime.strptime(data["checkindate"], "%Y-%m-%d")
                days_left = booked_date - datetime.now()
                days_left = int(days_left.days + 1)
                if days_left > 60:
                    fee = 0
                    extra_str = " no cancellation charge"
                elif days_left > 30:
                    fee = int(int(data["price"]) / 2)
                    extra_str = f" 50% of booking price will be charged - "
                elif days_left >= 0:
                    fee = int(data["price"])
                    extra_str = f" 100% of booking price will be charged - "
                else:
                    fee = ""
                    extra_str = ""
                bookings = db.retrieve_booking(session["email"])
                return render_template("userbookings.html", loggedIn = True, bookings = bookings, m = "Success", message = "Booking successfully deleted" + \
                    str(extra_str), currency = session["currency"], fee = fee)
            else:                
                bookings = db.retrieve_booking(session["email"])
                return render_template("userbookings.html", loggedIn = True, bookings = bookings, m = "Error", message = "That booking ID was not found", \
                    currency = session["currency"], fee = False)
        else: 
            return render_template("login.html", loggedIn = False, message = "You must login to access that page")
    else:
        if "email" in session:
            bookingID = request.args.get("bookingID")
            email = session["email"]
            data = db.cancel_booking(bookingID, email)
            if "currency" not in session:
                    session["currency"] = "gbp"
            if data != False:
                booked_date = datetime.strptime(data["checkindate"], "%Y-%m-%d")
                days_left = booked_date - datetime.now()
                days_left = int(days_left.days + 1)
                if days_left > 60:
                    fee = 0
                    extra_str = " no cancellation charge"
                elif days_left > 30:
                    fee = int(int(data["price"]) / 2)
                    extra_str = f" 50% of booking price will be charged - "
                elif days_left >= 0:
                    fee = int(data["price"])
                    extra_str = f" 100% of booking price will be charged - "
                else:
                    fee = ""
                    extra_str = ""
                bookings = db.retrieve_booking(session["email"])
                return render_template("userbookings.html", loggedIn = True, bookings = bookings, m = "Success", message = "Booking successfully deleted" + \
                    str(extra_str), currency = session["currency"], fee = fee)
            else:                
                bookings = db.retrieve_booking(session["email"])
                return render_template("userbookings.html", loggedIn = True, bookings = bookings, m = "Error", message = "That booking ID was not found", \
                    currency = session["currency"], fee = False)
        else: 
            return render_template("login.html", loggedIn = False, message = "You must login to access that page")


@app.route('/cancelbookingadmin', methods = ["POST", "GET"])
def cancelbookingadmin():
    if request.method == "POST":
        if "email" in session:
            bookingID = request.form["bookingID"]
            data = db.cancel_booking_admin(bookingID)
            bookings = db.retrieve_all_bookings()
            city_list = db.retrieve_accommodation_cities()
            return render_template("adminbookings.html", loggedIn = True, bookings = bookings, cities = city_list)
        else: 
            return render_template("login.html", loggedIn = False, message = "You must login to access that page")
    else:
        if "email" in session:
            bookingID = request.args.get("bookingID")
            data = db.cancel_booking_admin(bookingID)
            bookings = db.retrieve_all_bookings()
            city_list = db.retrieve_accommodation_cities()
            return render_template("adminbookings.html", loggedIn = True, bookings = bookings, cities = city_list)
        else: 
            return render_template("login.html", loggedIn = False, message = "You must login to access that page")


@app.route('/changedetails')
def changedetails():
    if "email" in session:
        return render_template("changedetails.html", loggedIn = True)
    else:
        return render_template("login.html", loggedIn = False, message = "You must login to access that page")


@app.route('/updatedetails', methods = ["POST", "GET"])
def updatedetails():
    if request.method == "POST":
        email = request.form["email"]
        firstname = request.form["firstname"]
        surname = request.form["surname"]
        password = request.form["password"]
        number = request.form["number"]
        address = request.form["address"]
        postcode = request.form["postcode"]
        confirmpassword = request.form["confirmpassword"]
        current_details = db.retrieve_user(session["email"])
        if not sha256_crypt.verify(confirmpassword, current_details["password"]):
            return render_template("changedetails.html", loggedIn = True, message = "Your password was incorrect")
        details = [email, firstname, surname, number, address, postcode]
        details_str = ["email", "firstname", "surname", "number", "address", "postcode"]        
        if password != "":
            pass_hash = sha256_crypt.hash(password)
        else:
            pass_hash = current_details["password"]
        for i in range(0, len(details)):
            if details[i] == "":
                details[i] = current_details[details_str[i]]
        db.update_user(details[0], details[1], details[2], pass_hash, details[3], details[4], details[5], session["email"])
        if email != "":
            session.pop("email", None)
            session["email"] = email
        return redirect(url_for('account'))
    else:
        email = request.args.get("email")
        firstname = request.args.get("firstname")
        surname = request.args.get("surname")
        password = request.args.get("password")
        number = request.args.get("number")
        address = request.args.get("address")
        postcode = request.args.get("postcode")
        confirmpassword = request.args.get("confirmpassword")
        current_details = db.retrieve_user(session["email"])
        if not sha256_crypt.verify(confirmpassword, current_details["password"]):
            return render_template("changedetails.html", loggedIn = True, message = "Your password was incorrect")
        details = [email, firstname, surname, number, address, postcode]
        details_str = ["email", "firstname", "surname", "number", "address", "postcode"]
        if password != "":
            pass_hash = sha256_crypt.hash(password)
        else:
            pass_hash = current_details["password"]
        for i in range(0, len(details)):
            if details[i] == "":
                details[i] = current_details[details_str[i]]
        db.update_user(details[0], details[1], details[2], pass_hash, details[3], details[4], details[5], session["email"])
        if email != "":
            session.pop("email", None)
            session["email"] = email
        return redirect(url_for('account'))


@app.route('/privacypolicy')
def privacypolicy():
    if "email" in session:
        loggedIn = True
    else: 
        loggedIn = False
    return render_template("privacypolicy.html", loggedIn = loggedIn)


@app.route('/contactus')
def contactus():
    if "email" in session:
        loggedIn = True
    else: 
        loggedIn = False
    return render_template("contactus.html", loggedIn = loggedIn)






if __name__ == '__main__':
    for i in range(13000, 18000):
      try:
         app.run(debug = True, port = i)
         break
      except OSError as e:
         print("Port {i} not available".format(i))