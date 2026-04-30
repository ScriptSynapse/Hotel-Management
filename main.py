import sqlite3
from datetime import datetime

# ================= DATABASE CONNECTION =================

conn = sqlite3.connect("hotel.db")
cursor = conn.cursor()

# ================= CREATE TABLES =================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS rooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_number TEXT,
    room_type TEXT,
    status TEXT,
    price REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS guests (
    guest_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    id_proof TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    guest_id INTEGER,
    room_id INTEGER,
    check_in TEXT,
    check_out TEXT,
    booking_status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bills (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER,
    room_charge REAL,
    food_charge REAL,
    laundry_charge REAL,
    gst REAL,
    total REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_id INTEGER,
    payment_method TEXT,
    payment_status TEXT
)
""")

conn.commit()

# ================= DEFAULT USERS =================

cursor.execute("SELECT * FROM users WHERE username='admin'")
if not cursor.fetchone():
    cursor.execute(
        "INSERT INTO users(username, password, role) VALUES(?,?,?)",
        ("admin", "admin123", "Admin")
    )

cursor.execute("SELECT * FROM users WHERE username='staff'")
if not cursor.fetchone():
    cursor.execute(
        "INSERT INTO users(username, password, role) VALUES(?,?,?)",
        ("staff", "staff123", "Staff")
    )

conn.commit()

# ================= LOGIN SYSTEM =================

def login():
    print("\n===== HOTEL MANAGEMENT LOGIN =====")

    username = input("Username: ")
    password = input("Password: ")

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    if user:
        print(f"\nLogin Successful ({user[3]})")
        return True
    else:
        print("\nInvalid Username or Password")
        return False

# ================= ROOM MANAGEMENT =================

def add_room():
    room_number = input("Enter Room Number: ")
    room_type = input("Enter Room Type (Standard/Deluxe/Suite): ")
    price = float(input("Enter Room Price: "))

    cursor.execute(
        "INSERT INTO rooms(room_number, room_type, status, price) VALUES(?,?,?,?)",
        (room_number, room_type, "Available", price)
    )

    conn.commit()
    print("Room Added Successfully")


def view_rooms():
    cursor.execute("SELECT * FROM rooms")
    rooms = cursor.fetchall()

    print("\n===== ROOMS =====")

    for room in rooms:
        print(room)


def update_room_status():
    room_id = input("Enter Room ID: ")
    status = input("Enter Status (Available/Occupied/Cleaning/Maintenance): ")

    cursor.execute(
        "UPDATE rooms SET status=? WHERE room_id=?",
        (status, room_id)
    )

    conn.commit()
    print("Room Status Updated")


def delete_room():
    room_id = input("Enter Room ID to Delete: ")

    cursor.execute(
        "DELETE FROM rooms WHERE room_id=?",
        (room_id,)
    )

    conn.commit()
    print("Room Deleted Successfully")

# ================= GUEST MANAGEMENT =================

def add_guest():
    name = input("Enter Guest Name: ")
    phone = input("Enter Phone Number: ")
    id_proof = input("Enter ID Proof: ")

    cursor.execute(
        "INSERT INTO guests(name, phone, id_proof) VALUES(?,?,?)",
        (name, phone, id_proof)
    )

    conn.commit()
    print("Guest Added Successfully")


def view_guests():
    cursor.execute("SELECT * FROM guests")
    guests = cursor.fetchall()

    print("\n===== GUESTS =====")

    for guest in guests:
        print(guest)


def search_guest():
    keyword = input("Enter Name/Phone/ID Proof: ")

    cursor.execute("""
    SELECT * FROM guests
    WHERE name LIKE ?
    OR phone LIKE ?
    OR id_proof LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))

    guests = cursor.fetchall()

    for guest in guests:
        print(guest)

# ================= BOOKING SYSTEM =================

def check_available_rooms():
    cursor.execute(
        "SELECT * FROM rooms WHERE status='Available'"
    )

    rooms = cursor.fetchall()

    print("\n===== AVAILABLE ROOMS =====")

    for room in rooms:
        print(room)


def book_room():
    guest_id = input("Enter Guest ID: ")
    room_id = input("Enter Room ID: ")
    check_in = input("Enter Check-in Date: ")
    check_out = input("Enter Check-out Date: ")

    cursor.execute(
        "SELECT status FROM rooms WHERE room_id=?",
        (room_id,)
    )

    room = cursor.fetchone()

    if room and room[0] == "Available":

        cursor.execute("""
        INSERT INTO bookings
        (guest_id, room_id, check_in, check_out, booking_status)
        VALUES(?,?,?,?,?)
        """, (
            guest_id,
            room_id,
            check_in,
            check_out,
            "Booked"
        ))

        cursor.execute("""
        UPDATE rooms
        SET status='Occupied'
        WHERE room_id=?
        """, (room_id,))

        conn.commit()

        print("Room Booked Successfully")

    else:
        print("Room Not Available")


def check_out():
    booking_id = input("Enter Booking ID: ")

    cursor.execute("""
    SELECT room_id FROM bookings
    WHERE booking_id=?
    """, (booking_id,))

    room = cursor.fetchone()

    if room:

        room_id = room[0]

        cursor.execute("""
        UPDATE bookings
        SET booking_status='Checked-Out'
        WHERE booking_id=?
        """, (booking_id,))

        cursor.execute("""
        UPDATE rooms
        SET status='Available'
        WHERE room_id=?
        """, (room_id,))

        conn.commit()

        print("Check-Out Successful")

    else:
        print("Booking Not Found")


def cancel_booking():
    booking_id = input("Enter Booking ID: ")

    cursor.execute("""
    SELECT room_id FROM bookings
    WHERE booking_id=?
    """, (booking_id,))

    room = cursor.fetchone()

    if room:

        room_id = room[0]

        cursor.execute("""
        UPDATE bookings
        SET booking_status='Cancelled'
        WHERE booking_id=?
        """, (booking_id,))

        cursor.execute("""
        UPDATE rooms
        SET status='Available'
        WHERE room_id=?
        """, (room_id,))

        conn.commit()

        print("Booking Cancelled")

    else:
        print("Booking Not Found")

# ================= BILLING SYSTEM =================

def generate_bill():
    booking_id = input("Enter Booking ID: ")

    room_charge = float(input("Enter Room Charge: "))
    food_charge = float(input("Enter Food Charge: "))
    laundry_charge = float(input("Enter Laundry Charge: "))

    subtotal = room_charge + food_charge + laundry_charge
    gst = subtotal * 0.18
    total = subtotal + gst

    cursor.execute("""
    INSERT INTO bills
    (booking_id, room_charge, food_charge,
    laundry_charge, gst, total)
    VALUES(?,?,?,?,?,?)
    """, (
        booking_id,
        room_charge,
        food_charge,
        laundry_charge,
        gst,
        total
    ))

    conn.commit()

    print("\n===== BILL =====")
    print("Subtotal:", subtotal)
    print("GST (18%):", gst)
    print("Total:", total)

# ================= PAYMENT SYSTEM =================

def make_payment():
    bill_id = input("Enter Bill ID: ")

    method = input("Payment Method (Cash/Card/UPI): ")

    cursor.execute("""
    INSERT INTO payments
    (bill_id, payment_method, payment_status)
    VALUES(?,?,?)
    """, (
        bill_id,
        method,
        "Paid"
    ))

    conn.commit()

    print("Payment Successful")

# ================= MAIN MENU =================

def main_menu():

    while True:

        print("\n===== HOTEL MANAGEMENT SYSTEM =====")

        print("1. Add Room")
        print("2. View Rooms")
        print("3. Update Room Status")
        print("4. Delete Room")

        print("5. Add Guest")
        print("6. View Guests")
        print("7. Search Guest")

        print("8. Check Available Rooms")
        print("9. Book Room")
        print("10. Check-Out")
        print("11. Cancel Booking")

        print("12. Generate Bill")
        print("13. Make Payment")

        print("14. Exit")

        choice = input("\nEnter Your Choice: ")

        if choice == "1":
            add_room()

        elif choice == "2":
            view_rooms()

        elif choice == "3":
            update_room_status()

        elif choice == "4":
            delete_room()

        elif choice == "5":
            add_guest()

        elif choice == "6":
            view_guests()

        elif choice == "7":
            search_guest()

        elif choice == "8":
            check_available_rooms()

        elif choice == "9":
            book_room()

        elif choice == "10":
            check_out()

        elif choice == "11":
            cancel_booking()

        elif choice == "12":
            generate_bill()

        elif choice == "13":
            make_payment()

        elif choice == "14":
            print("Thank You")
            break

        else:
            print("Invalid Choice")

# ================= START PROGRAM =================

if login():
    main_menu()

conn.close()
