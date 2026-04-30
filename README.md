# Hotel Management System

A simple command-line based Hotel Management System built using **Python** and **SQLite3**. This project helps manage hotel operations such as room booking, guest management, billing, payments, and room availability using a single Python file. 

---

## Features

### User Authentication

* Admin Login
* Staff Login
* Role-based user system
* Default users included

### Room Management

* Add rooms
* View rooms
* Update room status
* Delete rooms
* Room categories:

  * Standard
  * Deluxe
  * Suite
* Room status:

  * Available
  * Occupied
  * Cleaning
  * Maintenance

### Guest Management

* Add guest details
* View all guests
* Search guests using:

  * Name
  * Phone number
  * ID proof

### Booking System

* Check available rooms
* Book rooms
* Check-out guests
* Cancel bookings

### Billing System

* Generate hotel bills
* GST calculation (18%)
* Room charges
* Food charges
* Laundry charges

### Payment System

* Record payments
* Payment methods:

  * Cash
  * Card
  * UPI

### Database

Uses SQLite database with the following tables:

* users
* rooms
* guests
* bookings
* bills
* payments

---

# Technologies Used

* Python 3
* SQLite3

---

# Project Structure

```bash
Hotel-Management-System/
│
├── main.py
├── hotel.db
└── README.md
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/hotel-management-system.git
```

## 2. Navigate to Project Folder

```bash
cd hotel-management-system
```

## 3. Run the Program

```bash
python main.py
```

---

# Default Login Credentials

## Admin

```text
Username: admin
Password: admin123
```

## Staff

```text
Username: staff
Password: staff123
```

---

# Database Tables

## users

Stores login credentials and roles.

## rooms

Stores room details and availability.

## guests

Stores guest information.

## bookings

Stores room booking details.

## bills

Stores billing information.

## payments

Stores payment records.

---

# How It Works

1. User logs into the system
2. Admin/Staff accesses the main menu
3. Rooms and guests can be managed
4. Rooms can be booked or checked out
5. Bills can be generated
6. Payments can be recorded

---

# Sample Menu

```text
===== HOTEL MANAGEMENT SYSTEM =====

1. Add Room
2. View Rooms
3. Update Room Status
4. Delete Room
5. Add Guest
6. View Guests
7. Search Guest
8. Check Available Rooms
9. Book Room
10. Check-Out
11. Cancel Booking
12. Generate Bill
13. Make Payment
14. Exit
```

---

# Future Improvements

* Password encryption
* Forgot password functionality
* GUI using Tkinter or PyQt
* Web version using Flask/Django
* Email invoice generation
* Room service management
* Employee management
* Reports and analytics
* Online booking support

---

# Learning Concepts Used

* Python Functions
* SQLite Database
* CRUD Operations
* User Authentication
* File Handling
* Loops and Conditions
* Modular Programming

---

# License

This project is licensed under the MIT License.

---

# Author

Developed using Python and SQLite as a beginner-friendly hotel management project.
