#written by Ben Phillips - 21067833

import mysql.connector, dbfunc
from datetime import datetime

db_name = dbfunc.db


def countrooms(cursor):
    rooms = ["Standard", "Double", "Family"]
    multiplyer = [0.3, 0.5, 0.2]
    max_rooms = {
        'Aberdeen': 80, 
        'Belfast': 80,
        'Birmingham': 90,
        'Bristol': 90,
        'Cardiff': 80,
        'Edinburgh': 90,
        'Glasgow': 100,
        'London': 120,
        'Manchester': 110,
        'New Castle': 80,
        'Norwich': 80,
        'Nottingham': 100,
        'Oxford': 80,
        'Plymouth': 80,
        'Swansea': 80,
    }
    cursor.execute("SELECT cities FROM Accommodation;")
    data = cursor.fetchall()
    cities = []
    for city in data:
        city = str(city).strip("(")
        city = str(city).strip(")")
        city = str(city).strip(",")
        city = str(city).strip("'")
        cities.append(city)
    print("Retrieved cities")
    for city in cities:
        for room in rooms:
            cursor.execute("UPDATE Accommodation SET numof" + room.lower() + "rooms = %s WHERE cities = %s;", (max_rooms[city] * multiplyer[rooms.index(room)], city))
            room_count = max_rooms[city] * multiplyer[rooms.index(room)]
            cursor.execute("SELECT * FROM Bookings WHERE city = %s AND roomtype = %s;", (city, room))
            raw_data = cursor.fetchall()
            if raw_data != []:
                for data in raw_data:
                    checkin = datetime.strptime(data[3], '%Y-%m-%d')
                    checkout = datetime.strptime(data[4], '%Y-%m-%d')
                    label = "numof" + room.lower() + "rooms"
                    if (checkin - datetime.now()).days < 0 and (checkout - datetime.now()).days >= -1:
                        room_count = room_count - 1
                        cursor.execute("UPDATE Accommodation SET " + label + " = %s WHERE cities = %s;", (room_count, city))
                    else:
                        cursor.execute("UPDATE Accommodation SET " + label + " = %s WHERE cities = %s;", (room_count, city))


def add_user(firstname, surname, email, password, number, address, \
        postcode):
    conn = dbfunc.getConnection()
    if (conn != None):
        if (conn.is_connected()):
            print("MySQL connection established.")
            cursor = conn.cursor()
            cursor.execute("USE " + db_name + ";")
            cursor.execute("INSERT INTO Users (email, firstname, surname, password, \
                number, address, postcode) VALUES (%s, %s, %s, %s, %s, %s, %s);", (email, \
                    firstname, surname, password, number, address, postcode))
            print("User " + email + " added")
            conn.commit()
            cursor.close()
            conn.close()
        else:
            print("Database connection error.")
    else:
        print("dbfunc error.")


def update_user(new_email, firstname, surname, password, number, address, postcode, old_email):
    conn = dbfunc.getConnection()
    if (conn != None):
        if (conn.is_connected()):
            print("MySQL connection established.")
            cursor = conn.cursor()
            cursor.execute("USE " + db_name + ";")
            details = [new_email, firstname, surname, password, number, address, postcode]
            details_str = ["email", "firstname", "surname", "password", "number", "address", "postcode"]
            c = 0
            for detail in details:
                cursor.execute("UPDATE Users SET " + details_str[c] + " = %s WHERE email = %s;", (detail, old_email))
                c = c + 1
            #cursor.execute("UPDATE Users SET email = %s, SET firstname = %s, SET surname = %s, SET password = %s, \
                #SET number = %s, SET address = %s, SET postcode = %s WHERE email = %s;", (new_email, firstname, surname, \
                    #password, number, address, postcode, old_email))
            print("User " + old_email + " updated")
            conn.commit()
            cursor.close()
            conn.close()
        else:
            print("Database connection error.")
    else:
        print("dbfunc error.")


def retrieve_user(email):
    conn = dbfunc.getConnection()
    if (conn != None):
        if (conn.is_connected()):
            print("MySQL connection established.")
            cursor = conn.cursor()
            cursor.execute("USE " + db_name + ";")
            cursor.execute("SELECT * FROM Users WHERE email = %s;", (email, ))
            data = cursor.fetchall()
            if data != []:
                print("User " + email + " retrieved")
                dic = {
                    "email": data[0][0],
                    "firstname": data[0][1],
                    "surname": data[0][2],
                    "password": data[0][3],
                    "number": data[0][4],
                    "address": data[0][5],
                    "postcode": data[0][6],
                    "usertype": data[0][7],
                }
            else:
                print("Email not in database")
                dic = False
            cursor.close()
            conn.close()
            return dic
        else:
            print("Database connection error.")
    else:
        print("dbfunc error.")
        

def retrieve_all_users():
    conn = dbfunc.getConnection()
    if (conn != None):
        if (conn.is_connected()):
            print("MySQL connection established.")
            cursor = conn.cursor()
            cursor.execute("USE " + db_name + ";")
            cursor.execute("SELECT * FROM Users;")
            data = cursor.fetchall()
            users = []            
            if data != []:
                print("Users retrieved")
                for i in range(0, len(data)):
                    dic = {
                        "email": data[i][0],
                        "firstname": data[i][1],
                        "surname": data[i][2],
                        "password": data[i][3],
                        "number": data[i][4],
                        "address": data[i][5],
                        "postcode": data[i][6],
                        "usertype": data[i][7],
                    }
                    users.append(dic)
            else:
                print("No users in database")
                dic = False
            cursor.close()
            conn.close()
            return users
        else:
            print("Database connection error.")
    else:
        print("dbfunc error.")


def delete_user(email):
    conn = dbfunc.getConnection()
    if (conn != None):
        if (conn.is_connected()):
            print("MySQL connection established.")
            cursor = conn.cursor()
            cursor.execute("USE " + db_name + ";")
            cursor.execute("DELETE FROM Users WHERE email = %s;", (email, ))
            print("User " + email + " deleted")
            conn.commit()
            cursor.close()
            conn.close()
        else:
            print("Database connection error.")
    else:
        print("dbfunc error.")


def create_user_table():
    conn = dbfunc.getConnection()
    if (conn != None):
        if (conn.is_connected()):
            print("MySQL connection established.")
            cursor = conn.cursor()
            cursor.execute("USE " + db_name + ";")
            cursor.execute("CREATE TABLE Users (email VARCHAR(255) NOT NULL UNIQUE PRIMARY KEY, \
                firstname VARCHAR(40) NOT NULL, surname VARCHAR(40) NOT NULL, \
                    password VARCHAR(128) NOT NULL, number VARCHAR(30) NOT NULL, address VARCHAR(255) NOT NULL, \
                        postcode VARCHAR(16) NOT NULL, usertype VARCHAR(8) DEFAULT 'standard');")
            print("User table created")
            conn.commit()
            cursor.close()
            conn.close()
        else:
            print("Database connection error.")
    else:
        print("dbfunc error.")


def delete_user_table():
    conn = dbfunc.getConnection()
    print("\033[1;31;40m\nARE YOU SURE YOU WANT TO DELETE THE USERS TABLE?\033[0;37;40m")
    user_input = input("Enter 'yes' to confirm deletion: ").lower()
    if (user_input == 'yes'):
        if (conn != None):
            if (conn.is_connected()):
                print("MySQL connection established.")
                cursor = conn.cursor()
                cursor.execute("USE " + db_name + ";")
                cursor.execute("DROP TABLE Users;")
                print("User table deleted")
                conn.commit()
                cursor.close()
                conn.close()
            else:
                print("Database connection error.")
        else:
            print("dbfunc error.")
    else:
        print("Table deletion confirmation not accepted")


def retrieve_accommodation_cities():
    conn = dbfunc.getConnection()
    if (conn != None):
        if (conn.is_connected()):
            print("MySQL connection established.")
            cursor = conn.cursor()
            cursor.execute("USE " + db_name + ";")
            cursor.execute("SELECT cities FROM Accommodation;")
            data = cursor.fetchall()
            cities = []
            for city in data:
                city = str(city).strip("(")
                city = str(city).strip(")")
                city = str(city).strip(",")
                city = str(city).strip("'")
                cities.append(city)
            print("Retrieved cities")
            cursor.close()
            conn.close()
            return cities
        else:
            print("Database connection error.")
    else:  
        print("dbfunc error.")


def retrieve_all_accommodation():
    conn = dbfunc.getConnection()
    if (conn != None):
        if (conn.is_connected()):
            print("MySQL connection established.")
            cursor = conn.cursor()
            cursor.execute("USE " + db_name + ";")
            cursor.execute("SELECT * FROM Accommodation;")
            raw_data = cursor.fetchall()
            data = []
            for i in range(0, len(raw_data)):
                dic = {
                    "city": raw_data[i][0],
                    "numofstandardrooms": raw_data[i][1],
                    "numofdoublerooms": raw_data[i][2],
                    "numoffamilyrooms": raw_data[i][3],
                    "peakrate": raw_data[i][4],
                    "offpeakrate": raw_data[i][5],
                }
                data.append(dic)
            cursor.close()
            conn.close()
            return data
        else:
            print("Database connection error.")
    else:  
        print("dbfunc error.")


def retrieve_accommodation(city):
    conn = dbfunc.getConnection()
    if (conn != None):
        if (conn.is_connected()):
            print("MySQL connection established.")
            cursor = conn.cursor()
            cursor.execute("USE " + db_name + ";")
            cursor.execute("SELECT * FROM Accommodation WHERE cities = %s;", (city, ))
            data = cursor.fetchall()
            dic = {
                "city": data[0][0],
                "numofstandardrooms": data[0][1],
                "numofdoublerooms": data[0][2],
                "numoffamilyrooms": data[0][3],
                "peakrate": data[0][4],
                "offpeakrate": data[0][5],
            }
            print(f"Retrieved city: {city}, number of rooms: s {dic['numofstandardrooms']} d {dic['numofdoublerooms']} f {dic['numoffamilyrooms']}, \
                peak rate: {dic['peakrate']}, off peak rate: {dic['offpeakrate']}")
            cursor.close()
            conn.close()
            return dic
        else:
            print("Database connection error.")
    else:  
        print("dbfunc error.")


def create_accommodation_table():
    conn = dbfunc.getConnection()
    if (conn != None):
        if (conn.is_connected()):
            print("MySQL connection established.")
            cursor = conn.cursor()
            cursor.execute("USE " + db_name + ";")
            cursor.execute("CREATE TABLE Accommodation (cities VARCHAR(16) NOT NULL UNIQUE PRIMARY KEY, \
                numofstandardrooms INT, numofdoublerooms INT, numoffamilyrooms INT, peakrate INT, offpeakrate INT);")
            cursor.execute("INSERT INTO Accommodation (cities, numofstandardrooms, numofdoublerooms, \
                numoffamilyrooms, peakrate, offpeakrate) VALUES ('Aberdeen', 80 * 0.3, 80 * 0.5, 80 * 0.2, 140, 60), ('Belfast', 80 * 0.3, 80 * 0.5, 80 * 0.2, 130, 60), \
                    ('Birmingham', 90 * 0.3, 90 * 0.5, 90 * 0.2, 150, 70), ('Bristol', 90 * 0.3, 90 * 0.5, 90 * 0.2, 140, 70), \
                        ('Cardiff', 80 * 0.3, 80 * 0.5, 80 * 0.2, 120, 60), ('Edinburgh', 90 * 0.3, 90 * 0.5, 90 * 0.2, 160, 70), ('Glasgow', 100 * 0.3, 100 * 0.5, 100 * 0.2, 150, 70), \
                            ('London', 120 * 0.3, 120 * 0.5, 120 * 0.2, 200, 80), ('Manchester', 110 * 0.3, 110 * 0.5, 110 * 0.2, 180, 80), ('New Castle', 80 * 0.3, 80 * 0.5, 80 * 0.2, 100, 60), \
                                ('Norwich', 80 * 0.3, 80 * 0.5, 80 * 0.2, 100, 60), ('Nottingham', 100 * 0.3, 100 * 0.5, 100 * 0.2, 120, 70), ('Oxford', 80 * 0.3, 80 * 0.5, 80 * 0.2, 180, 70), \
                                    ('Plymouth', 80 * 0.3, 80 * 0.5, 80 * 0.2, 180, 50), ('Swansea', 80 * 0.3, 80 * 0.5, 80 * 0.2, 120, 50)")
            print("Accommodation table created")
            conn.commit()
            cursor.close()
            conn.close()
        else:
            print("Database connection error.")
    else:  
        print("dbfunc error.")


def delete_accommodation_table():
    conn = dbfunc.getConnection()
    print("\033[1;31;40m\nARE YOU SURE YOU WANT TO DELETE THE ACCOMMODATION TABLE?\033[0;37;40m")
    user_input = input("Enter 'yes' to confirm deletion: ").lower()
    if (user_input == 'yes'):
        if (conn != None):
            if (conn.is_connected()):
                print("MySQL connection established.")
                cursor = conn.cursor()
                cursor.execute("USE " + db_name + ";")
                cursor.execute("DROP TABLE Accommodation;")
                print("Accommodation table deleted")
                conn.commit()
                cursor.close()
                conn.close()
            else:
                print("Database connection error.")
        else:
            print("dbfunc error.")
    else:
        print("Table deletion confirmation not accepted")


def delete_hotel(city):
    conn = dbfunc.getConnection()
    if (conn != None):
        if (conn.is_connected()):
            print("MySQL connection established.")
            cursor = conn.cursor()
            cursor.execute("USE " + db_name + ";")
            cursor.execute("DELETE FROM Accommodation WHERE cities = %s;", (city, ))
            print(city + " successfully deleted")
            conn.commit()
            cursor.close()
            conn.close()
        else:
            print("Database connection error.")
    else:  
        print("dbfunc error.")


def add_hotel(city, maxrooms, peakrate, offpeakrate):
    conn = dbfunc.getConnection()
    if (conn != None):
        if (conn.is_connected()):
            print("MySQL connection established.")
            cursor = conn.cursor()
            cursor.execute("USE " + db_name + ";")
            cursor.execute("INSERT INTO Accommodation (cities, numofstandardrooms, numofdoublerooms, numoffamilyrooms, peakrate, offpeakrate) VALUES (%s, \
                %s, %s, %s, %s, %s);", (city, int(maxrooms * 0.3), int(maxrooms * 0.5), int(maxrooms * 0.2), peakrate, offpeakrate))
            print(city + " successfully created")
            conn.commit()
            cursor.close()
            conn.close()
        else:
            print("Database connection error.")
    else:  
        print("dbfunc error.")


def update_hotel(city, maxrooms, peakrate, offpeakrate):
    conn = dbfunc.getConnection()
    if (conn != None):
        if (conn.is_connected()):
            print("MySQL connection established.")
            cursor = conn.cursor()
            cursor.execute("USE " + db_name + ";")
            cursor.execute("UPDATE Accommodation SET numofstandardrooms = %s, numofdoublerooms = %s, numoffamilyrooms = %s, peakrate = %s, offpeakrate = %s WHERE cities = %s;", \
                (int(maxrooms * 0.3), int(maxrooms * 0.5), int(maxrooms * 0.2), peakrate, offpeakrate, city))
            print(city + " successfully updated")
            conn.commit()
            cursor.close()
            conn.close()
        else:
            print("Database connection error.")
    else:  
        print("dbfunc error.")


def create_booking_table():
    conn = dbfunc.getConnection()
    if (conn != None):
        if (conn.is_connected()):
            print("MySQL connection established.")
            cursor = conn.cursor()
            cursor.execute("USE " + db_name + ";")
            cursor.execute("CREATE TABLE Bookings (bookingID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, email VARCHAR(255), FOREIGN KEY (email) \
                REFERENCES Users (email) ON DELETE SET NULL ON UPDATE CASCADE, city VARCHAR(16) NOT NULL, \
                checkindate VARCHAR(16) NOT NULL, checkoutdate VARCHAR(16) NOT NULL, numofguests INT NOT NULL, roomtype VARCHAR(16) NOT NULL, totalprice INT NOT NULL, \
                    datecreated VARCHAR(16) NOT NULL);")
            print("Booking table created")
            conn.commit()
            cursor.close()
            conn.close()
        else:
            print("Database connection error.")
    else:  
        print("dbfunc error.")


def delete_booking_table():
    conn = dbfunc.getConnection()
    print("\033[1;31;40m\nARE YOU SURE YOU WANT TO DELETE THE BOOKING TABLE?\033[0;37;40m")
    user_input = input("Enter 'yes' to confirm deletion: ").lower()
    if (user_input == 'yes'):
        if (conn != None):
            if (conn.is_connected()):
                print("MySQL connection established.")
                cursor = conn.cursor()
                cursor.execute("USE " + db_name + ";")
                cursor.execute("DROP TABLE Bookings;")
                print("Booking table deleted")
                conn.commit()
                cursor.close()
                conn.close()
            else:
                print("Database connection error.")
        else:
            print("dbfunc error.")
    else:
        print("Table deletion confirmation not accepted")


def make_booking(email, city, checkindate, checkoutdate, numofguests, roomtype, price, datecreated):
    conn = dbfunc.getConnection()
    if (conn != None):
        if (conn.is_connected()):
            print("MySQL connection established.")
            cursor = conn.cursor()
            cursor.execute("USE " + db_name + ";")
            cursor.execute("INSERT INTO Bookings (email, city, checkindate, checkoutdate, numofguests, roomtype, totalprice, datecreated) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (email, city, checkindate, checkoutdate, numofguests, roomtype, price, datecreated))
            print("Booking created")
            countrooms(cursor)
            conn.commit()
            cursor.close()
            conn.close()
        else:
            print("Database connection error.")
    else:
        print("dbfunc error.")


def retrieve_all_bookings():
    conn = dbfunc.getConnection()
    if (conn != None):
        if (conn.is_connected()):
            print("MySQL connection established.")
            cursor = conn.cursor()
            cursor.execute("USE " + db_name + ";")
            cursor.execute("SELECT * FROM Bookings;")
            raw_data = cursor.fetchall()
            if raw_data != []:
                print("Booking retrieved")
                data = []
                for i in range(0, len(raw_data)):
                    dic = {
                        "bookingID": raw_data[i][0],
                        "email": raw_data[i][1],
                        "city": raw_data[i][2],
                        "checkindate": raw_data[i][3],
                        "checkoutdate": raw_data[i][4],
                        "guestnum": raw_data[i][5],
                        "roomtype": raw_data[i][6],
                        "price": raw_data[i][7],
                        "datecreated": raw_data[i][8],
                    }
                    data.append(dic)
            else:
                print("No bookings found")
                data = False
            cursor.close()
            conn.close()
            return data
        else:
            print("Database connection error.")
    else:
        print("dbfunc error.")


def retrieve_filtered_bookings(data):
    conn = dbfunc.getConnection()
    if (conn != None):
        if (conn.is_connected()):
            print("MySQL connection established.")
            cursor = conn.cursor()
            cursor.execute("USE " + db_name + ";")
            cursor.execute("SELECT * FROM Bookings;")
            first_raw_data = cursor.fetchall()
            if first_raw_data != []:
                first_data = []
                for i in range(0, len(first_raw_data)):
                    first_dic = {
                        "bookingID": first_raw_data[i][0],
                        "email": first_raw_data[i][1],
                        "city": first_raw_data[i][2],
                        "checkindate": first_raw_data[i][3],
                        "checkoutdate": first_raw_data[i][4],
                        "guestnum": first_raw_data[i][5],
                        "roomtype": first_raw_data[i][6],
                        "price": first_raw_data[i][7],
                        "datecreated": first_raw_data[i][8],
                    }
                    first_data.append(first_dic)
            else:
                print("No bookings found")
                first_data = False
            extra = ""
            if data[0] == "all" and data[1] == "" and data[2] == "" and data[3] == "" and data[4] == "":
                extra = ""
            else:
                if first_data != False:
                    needand = False
                    all_ids = []
                    if data[0] != "all":
                        extra = " WHERE"
                        extra = extra + " city = '" + data[0] + "'"
                        needand = True

                    if data[1] != "" or data[2] != "":
                        ids_to_keep = []
                        if data[1] != "":
                            checkinfrom = datetime.strptime(data[1], '%Y-%m-%d')                            
                            for d in first_data:
                                checkin = datetime.strptime(d["checkindate"], '%Y-%m-%d')
                                if (checkinfrom - checkin).days <= 0:
                                    ids_to_keep.append(d["bookingID"])
                        if data[2] != "":
                            checkinto = datetime.strptime(data[2], '%Y-%m-%d')
                            for d in first_data:
                                checkin = datetime.strptime(d["checkindate"], '%Y-%m-%d')
                                if (checkinto - checkin).days > -1:
                                    ids_to_keep.append(d["bookingID"])
                        if data[1] != "" and data[2] != "":
                            ids = ids_to_keep
                            ids_to_keep = []
                            for base_id in ids:
                                once = False
                                done = False
                                for id in ids:
                                    if once == True and base_id == id:
                                        ids_to_keep.append(base_id)
                                        done = True
                                    if base_id == id and done != True:
                                        once = True                        
                        for id in ids_to_keep:
                            all_ids.append(id)
                            
                    if data[3] != "" or data[4] != "":
                        ids_to_keep = []
                        if data[3] != "":
                            bookingmadefrom = datetime.strptime(data[3], '%Y-%m-%d')                            
                            for d in first_data:
                                datecreated = datetime.strptime(d["datecreated"], '%Y-%m-%d')
                                if (bookingmadefrom - datecreated).days <= 0:
                                    ids_to_keep.append(d["bookingID"])
                        if data[4] != "":
                            bookingmadeto = datetime.strptime(data[4], '%Y-%m-%d')
                            for d in first_data:
                                datecreated = datetime.strptime(d["datecreated"], '%Y-%m-%d')
                                if (bookingmadeto - datecreated).days > -1:
                                    ids_to_keep.append(d["bookingID"])
                        if data[3] != "" and data[4] != "":
                            ids = ids_to_keep
                            ids_to_keep = []
                            for base_id in ids:
                                once = False
                                done = False
                                for id in ids:
                                    if once == True and base_id == id:
                                        ids_to_keep.append(base_id)
                                        done = True
                                    if base_id == id and done != True:
                                        once = True
                        for id in ids_to_keep:
                            if id not in all_ids:
                                all_ids.append(id)
                        
                    if data[1] != "" or data[2] != "" or data[3] != "" or data[4] != "":
                        if all_ids != []:
                            if data[0] == 'all':
                                extra = " WHERE"
                            if needand:
                                extra = extra + " AND"
                            extra = extra + " bookingID in ("
                            i = 0
                            for id in range(0, len(all_ids)):
                                i = i + 1
                                extra = extra + str(all_ids[id])
                                if id < (len(all_ids) - 1):
                                    extra = extra + ", "
                            extra = extra + ")"      
                        else:
                            if data[0] == 'all':
                                extra = " WHERE"
                            if needand:
                                extra = extra + " AND"
                            extra = extra + " bookingID in (10000000000000000000000)"
            print(extra)
            cursor.execute("SELECT * FROM Bookings" + extra + ";")
            raw_data = cursor.fetchall()
            if raw_data != []:
                print("Booking retrieved")
                data = []
                for i in range(0, len(raw_data)):
                    dic = {
                        "bookingID": raw_data[i][0],
                        "email": raw_data[i][1],
                        "city": raw_data[i][2],
                        "checkindate": raw_data[i][3],
                        "checkoutdate": raw_data[i][4],
                        "guestnum": raw_data[i][5],
                        "roomtype": raw_data[i][6],
                        "price": raw_data[i][7],
                        "datecreated": raw_data[i][8],
                    }
                    data.append(dic)
            else:
                print("No bookings found")
                data = []
            cursor.close()
            conn.close()
            return data
        else:
            print("Database connection error.")
    else:
        print("dbfunc error.")


def retrieve_booking(email):
    conn = dbfunc.getConnection()
    if (conn != None):
        if (conn.is_connected()):
            print("MySQL connection established.")
            cursor = conn.cursor()
            cursor.execute("USE " + db_name + ";")
            cursor.execute("SELECT * FROM Bookings WHERE email = %s;", (email,))
            raw_data = cursor.fetchall()
            if raw_data != []:
                print("Booking retrieved")
                data = []
                for i in range(0, len(raw_data)):
                    dic = {
                        "bookingID": raw_data[i][0],
                        "email": raw_data[i][1],
                        "city": raw_data[i][2],
                        "checkindate": raw_data[i][3],
                        "checkoutdate": raw_data[i][4],
                        "guestnum": raw_data[i][5],
                        "roomtype": raw_data[i][6],
                        "price": raw_data[i][7],
                        "datecreated": raw_data[i][8],
                    }
                    data.append(dic)
            else:
                print("No bookings found")
                data = False
            cursor.close()
            conn.close()
            return data
        else:
            print("Database connection error.")
    else:
        print("dbfunc error.")


def cancel_booking(bookingID, email):
    conn = dbfunc.getConnection()
    if (conn != None):
        if (conn.is_connected()):
            print("MySQL connection established.")
            cursor = conn.cursor()
            cursor.execute("USE " + db_name + ";")
            cursor.execute("SELECT * FROM Bookings WHERE bookingID = %s AND email = %s;", (bookingID, email))
            raw_data = cursor.fetchall()
            for data in raw_data:
                print(data)
            if raw_data == []:
                data = False
                print("No bookings were found")
            else:
                data = {
                    "bookingID": raw_data[0][0],
                    "email": raw_data[0][1],
                    "city": raw_data[0][2],
                    "checkindate": raw_data[0][3],
                    "checkoutdate": raw_data[0][4],
                    "guestnum": raw_data[0][5],
                    "roomtype": raw_data[0][6],
                    "price": raw_data[0][7],
                    "datecreated": raw_data[0][8],
                    }
                cursor.execute("DELETE FROM Bookings WHERE bookingID = %s AND email = %s;", (bookingID, email))
                print("Bookings deleted")
            countrooms(cursor)
            conn.commit()
            cursor.close()
            conn.close()
            return data
        else:
            print("Database connection error.")
    else:
        print("dbfunc error.")


def cancel_booking_admin(bookingID):
    conn = dbfunc.getConnection()
    if (conn != None):
        if (conn.is_connected()):
            print("MySQL connection established.")
            cursor = conn.cursor()
            cursor.execute("USE " + db_name + ";")
            cursor.execute("SELECT * FROM Bookings WHERE bookingID = %s;", (bookingID,))
            raw_data = cursor.fetchall()
            for data in raw_data:
                print(data)
            if raw_data == []:
                data = False
                print("No bookings were found")
            else:
                data = {
                    "bookingID": raw_data[0][0],
                    "email": raw_data[0][1],
                    "city": raw_data[0][2],
                    "checkindate": raw_data[0][3],
                    "checkoutdate": raw_data[0][4],
                    "guestnum": raw_data[0][5],
                    "roomtype": raw_data[0][6],
                    "price": raw_data[0][7],
                    "datecreated": raw_data[0][8],
                    }
                cursor.execute("DELETE FROM Bookings WHERE bookingID = %s;", (bookingID,))
                print("Bookings deleted")
            countrooms(cursor)
            conn.commit()
            cursor.close()
            conn.close()
            return data
        else:
            print("Database connection error.")
    else:
        print("dbfunc error.")


def check_room_count():
    conn = dbfunc.getConnection()
    if (conn != None):
        if (conn.is_connected()):
            print("MySQL connection established.")
            cursor = conn.cursor()
            cursor.execute("USE " + db_name + ";")
            countrooms(cursor)
            conn.commit()
            cursor.close()
            conn.close()
        else:
            print("Database connection error.")
    else:
        print("dbfunc error.")