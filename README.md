# 🍽️ Hostel Mess Smart Food Voting System — Baby Blue Edition

![Python](https://img.shields.io/badge/Python-3.12-38BDF8?logo=python\&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-0284C7)
![Status](https://img.shields.io/badge/Status-In%20Development-F59E0B)

A **Pure Python desktop application** being developed to make hostel mess food selection smarter and more efficient through **QR-based food voting, automated poll expiry, live results, analytics, and role-based access**.

> 🚧 **Project Status: Under Development**
>
> The system is currently being developed and tested. Additional features, improvements, security enhancements, and UI refinements will be added in future versions.

---

## 🌟 Planned Key Features

### 👨‍🍳 Cook Portal — Kitchen Access

The Cook Portal will allow mess staff to create and manage food voting sessions.

* Create meal sessions for **Breakfast, Lunch, Snacks, and Dinner**
* Add **2–6 food options** for each meal
* Set a custom voting deadline
* Automatically close voting when the deadline expires
* Generate a **QR code poster** for students to scan
* View live voting results
* Display vote counts using animated progress bars
* Highlight the currently leading dish
* Manually lock a poll when cooking starts
* Maintain a historical record of created polls

---

### 🎓 Student Portal — Food Voting

The Student Portal will provide students with a simple way to participate in active food polls.

* Scan the mess QR code using an integrated camera
* Open active polls directly through a poll selector
* Authenticate using hostel **roll number / room number**
* Enforce a **one-vote-per-student** rule
* Display a live countdown until voting closes
* Automatically lock voting after expiry
* Display voting confirmation
* Provide a visual celebration animation after voting

---

### 🛡️ Admin Portal — Analytics & Management

The Admin Portal is planned as the central monitoring and management dashboard.

#### 📊 Turnout Analytics

The administrator will be able to view:

* Total students in the hostel roster
* Number of students who voted
* Number of students who did not vote
* Overall participation percentage

#### 👥 Student Ledger

The system will maintain student-wise voting information.

**Students who voted:**

* Roll number
* Name
* Room number
* Selected dish
* Vote timestamp

**Students who did not vote:**

* Roll number
* Name
* Room number
* Department
* Contact information

#### 🍴 Cook Dish History

The admin will be able to view historical information about:

* Meal sessions
* QR-generated polls
* Dishes added by the cook
* Voting dates and times
* Poll expiry information

#### 📈 Visual Analytics

Future versions will include Matplotlib-based charts such as:

* Participation donut chart
* Vote distribution bar chart
* Meal-wise voting statistics
* Historical participation trends

#### 📄 Reports & Audit

Planned administrative features include:

* Audit trail
* CSV report export
* Historical poll records
* Student participation reports

---

## 🎨 UI & Animation

The application is being designed with a **Baby Blue** visual theme.

### 🎨 Color Palette

* **Alice Blue:** `#F0F8FF`
* **Sky Blue:** `#38BDF8`
* **Deep Ocean Blue:** `#0284C7`

### ✨ Planned Animations

* Smooth page transitions
* Animated voting progress bars
* Pulsing countdown timer
* Countdown warning states
* QR scanning animation
* Confetti animation after successful voting
* Smooth dashboard interactions

---

## 🔐 Security & Access Control

Role-based access will be implemented for the three major users:

| Role       | Access                              |
| ---------- | ----------------------------------- |
| 👨‍🍳 Cook | Create and manage food polls        |
| 🎓 Student | View active polls and vote          |
| 🛡️ Admin  | View analytics, records and reports |

The Admin Portal will also be protected using an authentication mechanism. **Security features will be strengthened further during development.**

---

## 🛠️ Technology Stack

The project is being developed using **100% Python**.

| Technology      | Purpose            |
| --------------- | ------------------ |
| Python 3.12     | Core application   |
| CustomTkinter   | Modern desktop UI  |
| SQLite          | Local database     |
| OpenCV          | QR/camera scanning |
| QR Code Library | QR generation      |
| Matplotlib      | Analytics & charts |
| Tkinter Canvas  | Animations         |
| CSV             | Report generation  |

No HTML, CSS, or JavaScript is required for the desktop application.

---

## 📁 Planned Project Architecture

```text
newproject/
│
├── main.py                 # Application entry point & view routing
├── theme.py                # Baby blue theme & UI constants
├── database.py             # SQLite database & CRUD operations
├── animations.py           # UI animations & transitions
├── qr_manager.py           # QR generation & camera scanning
├── requirements.txt        # Python dependencies
├── run.bat                 # Windows launcher
│
└── views/
    ├── login_view.py       # Role selection & authentication
    ├── cook_view.py        # Cook portal
    ├── student_view.py     # Student voting portal
    └── admin_view.py       # Admin dashboard
```

> 📌 The architecture may change as development continues and new modules are introduced.

---

## 🚀 How to Run

### Method 1 — Windows Launcher

Once the project reaches a runnable stage:

```text
Double-click run.bat
```

### Method 2 — Terminal / PowerShell

```bash
python main.py
```

Or:

```powershell
& "C:\Users\megha\AppData\Local\Programs\Python\Python312\python.exe" main.py
```

> ⚠️ Running instructions may change as the project develops.

---

## 🗺️ Development Roadmap

### Phase 1 — Core System

* [x] Project structure
* [ ] Basic UI
* [ ] Role selection
* [ ] SQLite database
* [ ] Student roster

### Phase 2 — Cook Portal

* [ ] Meal creation
* [ ] Dish selection
* [ ] Poll expiry
* [ ] QR generation
* [ ] Live voting results

### Phase 3 — Student Portal

* [ ] QR scanning
* [ ] Student authentication
* [ ] One-vote-per-student validation
* [ ] Countdown timer
* [ ] Vote confirmation

### Phase 4 — Admin Dashboard

* [ ] Student participation analytics
* [ ] Voting ledger
* [ ] Cook dish history
* [ ] Matplotlib charts
* [ ] CSV reports
* [ ] Audit trail

### Phase 5 — Enhancement & Testing

* [ ] Improve security
* [ ] UI/UX refinement
* [ ] Performance optimization
* [ ] Error handling
* [ ] Testing
* [ ] Documentation
* [ ] Final deployment/release

---

## 🔮 Future Development

The project is planned to be expanded further with additional features such as:

* 📊 Advanced food preference analytics
* 📅 Meal-wise historical statistics
* 🔔 Poll expiry notifications
* 📱 Improved QR-based accessibility
* 🔐 Stronger authentication and security
* 📈 Food demand prediction using historical voting data
* 🤖 Intelligent meal recommendation features
* 🧾 Automated report generation
* ☁️ Possible centralized/cloud database support
* 👥 Support for multiple hostels or mess locations

---

## 📌 Project Status

**🚧 Currently Under Development**

This project is being actively developed. The features, architecture, interface, database design, and security mechanisms may change as new requirements are added and the system is tested.

The goal is to build a **reliable, user-friendly, and intelligent hostel mess voting platform** that reduces food wastage while giving students a convenient way to participate in meal selection.

---

## 👨‍💻 Development

**Hostel Mess Smart Food Voting System**

Built with ❤️ using **Python + CustomTkinter + SQLite**
