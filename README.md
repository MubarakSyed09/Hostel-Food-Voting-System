# 🍽️ Hostel Mess Smart Food Voting System (Baby Blue Edition)

![Python](https://img.shields.io/badge/Python-3.12-38BDF8?logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-0284C7)
![Build](https://img.shields.io/badge/CI%20Tests-Passing-10B981)

A 100% **Pure Python** desktop application (Built without any HTML, CSS, or JavaScript) for intelligent hostel food voting via QR codes with automated time expiry, live analytics, and role-based permissions.


---

## 🌟 Key Features

### 👨‍🍳 Cook Portal (Restricted Kitchen Access)
* **Limited Dish Options**: Cook can define 2 to 6 food choices for any meal session (Breakfast, Lunch, Snacks, Dinner).
* **Automated Expiry Time**: Cook sets the exact deadline when voting closes (e.g. In 30 mins, 1 hour, 2 hours, custom).
* **Instant QR Poster Generation**: Generates a high-resolution, styled baby-blue QR code poster ready to print or project on the mess screen.
* **Live Results & Kitchen Tallies**: Watch votes update live with animated progress bars, leading dish winner highlight (👑), and option to manually lock the poll early once cooking starts.

### 🎓 Student Portal (Strict Polling Access)
* **Live Camera QR Scanner**: Integrated OpenCV webcam scanner with animated laser radar to scan QR codes physically displayed in the dining hall.
* **Quick Poll Selector**: Test active polls directly without camera.
* **Hostel Roster Authentication**: Select or enter student roll number / room number. Enforces **strict 1-vote-per-student** rule.
* **Pulsing Countdown Clock**: Live ticking indicator showing exact time remaining before the poll expires.
* **Celebration Confetti Animation**: Smooth canvas confetti particle simulation upon casting a vote!
* **Locked State**: Once the expiry timer hits zero, the poll automatically locks and shows an expired banner.

### 🛡️ Admin Portal (Master God-Mode Access)
* **Protected by Security PIN** (Default PIN: `admin123`).
* **Turnout Analytics**:
  * Total students in hostel roster.
  * Exactly how many polled vs how many didn't poll.
  * Turnout participation percentage.
* **Student-by-Student Ledger**:
  * **Polled Students**: Roll number, Name, Room number, Chosen dish, and Vote timestamp.
  * **Didn't Poll Students**: Roll number, Name, Room number, Department, and Contact Phone number.
* **Daily Cook Dishes Log**: Complete historical record of every QR generated and the exact dishes the cook added on any given day.
* **Visual Matplotlib Charts**:
  * Participation donut chart.
  * Horizontal vote distribution bar chart.
* **Audit Trail & CSV Export**: Download complete reports for records and compliance.

---

## 🎨 Theme & Animations
* **Baby Blue Palette**: Soft Alice Blue (`#F0F8FF`), Sky Blue (`#38BDF8`), and Deep Ocean accents (`#0284C7`).
* **Fluid Page Transitions**: Quadratic and cubic eased slide-in view transitions.
* **Animated Result Bars**: Smooth easing progress bars that count up dynamically.
* **Pulsing Countdown Timer**: Live ticking with color-shifting warning when time is low.
* **Confetti Celebration**: Dynamic particle physics simulation.

---

## 🚀 How to Run

### Method 1: Double-Click Launcher
Simply double-click the `run.bat` file in this folder.

### Method 2: Terminal / PowerShell
```bash
python main.py
```
Or with full path:
```powershell
& "C:\Users\megha\AppData\Local\Programs\Python\Python312\python.exe" main.py
```

---

## 📁 Project Architecture
```
newproject/
├── main.py             # Main application entry point & view router
├── theme.py            # Baby blue design system & style constants
├── database.py         # SQLite database schema, CRUD, and analytics
├── animations.py       # Slide transitions, animated progress bars, confetti
├── qr_manager.py       # QR code generator, poster builder & camera scanner
├── requirements.txt    # Python dependencies
├── run.bat             # Windows one-click launcher
└── views/
    ├── login_view.py   # Role selector (Cook, Student, Admin)
    ├── cook_view.py    # Cook portal
    ├── student_view.py # Student voting portal
    └── admin_view.py   # Admin master analytics dashboard
```
