import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hostel_mess.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Students Table (Hostel Roster)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        room_no TEXT NOT NULL,
        block TEXT NOT NULL,
        department TEXT NOT NULL,
        phone TEXT
    )
    """)
    
    # 2. Polls / QR Sessions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS polls (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        date TEXT NOT NULL,
        meal_type TEXT NOT NULL,
        created_at TEXT NOT NULL,
        expires_at TEXT NOT NULL,
        created_by TEXT NOT NULL,
        status TEXT NOT NULL,
        notes TEXT,
        qr_image_path TEXT
    )
    """)
    
    # 3. Dishes (Limited options provided by cook)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dishes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        poll_id TEXT NOT NULL,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        calories INTEGER DEFAULT 0,
        allergens TEXT DEFAULT 'None',
        FOREIGN KEY (poll_id) REFERENCES polls (id) ON DELETE CASCADE
    )
    """)
    
    # 4. Votes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        poll_id TEXT NOT NULL,
        student_id TEXT NOT NULL,
        dish_id INTEGER NOT NULL,
        voted_at TEXT NOT NULL,
        UNIQUE(poll_id, student_id),
        FOREIGN KEY (poll_id) REFERENCES polls (id) ON DELETE CASCADE,
        FOREIGN KEY (student_id) REFERENCES students (student_id),
        FOREIGN KEY (dish_id) REFERENCES dishes (id)
    )
    """)
    
    # 5. Audit Log (Admin Visibility)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        action TEXT NOT NULL,
        performed_by TEXT NOT NULL,
        details TEXT NOT NULL
    )
    """)
    
    conn.commit()
    
    # Seed data if students table is empty
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    if count == 0:
        seed_data(cursor, conn)
        
    conn.close()

def seed_data(cursor, conn):
    # Pre-populate 40 hostel students
    students = [
        ("H2024-101", "Aarav Sharma", "A-101", "Block A", "Computer Science", "+91 98765 43210"),
        ("H2024-102", "Ananya Verma", "B-204", "Block B", "Electronics & Comm", "+91 98765 43211"),
        ("H2024-103", "Rohan Mehta", "A-102", "Block A", "Mechanical Eng", "+91 98765 43212"),
        ("H2024-104", "Diya Patel", "B-205", "Block B", "Biotechnology", "+91 98765 43213"),
        ("H2024-105", "Kabir Nair", "A-103", "Block A", "Computer Science", "+91 98765 43214"),
        ("H2024-106", "Sneha Iyer", "B-206", "Block B", "Civil Engineering", "+91 98765 43215"),
        ("H2024-107", "Vikram Rathore", "A-104", "Block A", "Data Science", "+91 98765 43216"),
        ("H2024-108", "Pooja Reddy", "B-207", "Block B", "Chemical Eng", "+91 98765 43217"),
        ("H2024-109", "Arjun Das", "A-105", "Block A", "Computer Science", "+91 98765 43218"),
        ("H2024-110", "Meera Kulkarni", "B-208", "Block B", "Electrical Eng", "+91 98765 43219"),
        ("H2024-111", "Aditya Joshi", "A-106", "Block A", "Mechanical Eng", "+91 98765 43220"),
        ("H2024-112", "Ishita Bose", "B-209", "Block B", "Information Tech", "+91 98765 43221"),
        ("H2024-113", "Siddharth Rao", "A-107", "Block A", "Computer Science", "+91 98765 43222"),
        ("H2024-114", "Tanvi Sengupta", "B-210", "Block B", "Biotechnology", "+91 98765 43223"),
        ("H2024-115", "Karan Malhotra", "A-108", "Block A", "Data Science", "+91 98765 43224"),
        ("H2024-116", "Rhea Nambiar", "B-211", "Block B", "Electronics & Comm", "+91 98765 43225"),
        ("H2024-117", "Gaurav Singh", "A-109", "Block A", "Civil Engineering", "+91 98765 43226"),
        ("H2024-118", "Priya Chawla", "B-212", "Block B", "Computer Science", "+91 98765 43227"),
        ("H2024-119", "Manish Pandey", "A-110", "Block A", "Mechanical Eng", "+91 98765 43228"),
        ("H2024-120", "Divya Menon", "B-213", "Block B", "Chemical Eng", "+91 98765 43229"),
        ("H2024-121", "Nikhil Chopra", "A-111", "Block A", "Information Tech", "+91 98765 43230"),
        ("H2024-122", "Kavya Sundaram", "B-214", "Block B", "Electrical Eng", "+91 98765 43231"),
        ("H2024-123", "Varun Bhatia", "A-112", "Block A", "Computer Science", "+91 98765 43232"),
        ("H2024-124", "Simran Kaur", "B-215", "Block B", "Data Science", "+91 98765 43233"),
        ("H2024-125", "Harsh Vardhan", "A-113", "Block A", "Mechanical Eng", "+91 98765 43234"),
        ("H2024-126", "Ayesha Siddiqui", "B-216", "Block B", "Electronics & Comm", "+91 98765 43235"),
        ("H2024-127", "Prateek Deshmukh", "A-114", "Block A", "Civil Engineering", "+91 98765 43236"),
        ("H2024-128", "Shruti Pillai", "B-217", "Block B", "Biotechnology", "+91 98765 43237"),
        ("H2024-129", "Abhishek Tiwari", "A-115", "Block A", "Computer Science", "+91 98765 43238"),
        ("H2024-130", "Neha Saxena", "B-218", "Block B", "Information Tech", "+91 98765 43239")
    ]
    cursor.executemany("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)", students)
    
    # Pre-seed a sample today's active poll
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    expiry_time = (now + timedelta(hours=3, minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
    poll_id_active = f"POLL-{now.strftime('%Y%m%d')}-LUNCH"
    
    cursor.execute("""
    INSERT INTO polls VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        poll_id_active,
        "Sunday Special Lunch Selection",
        today_str,
        "Lunch",
        now.strftime("%Y-%m-%d %H:%M:%S"),
        expiry_time,
        "Head Chef Suresh",
        "ACTIVE",
        "Please select your lunch preference before 1:30 PM for kitchen preparation.",
        ""
    ))
    
    # Dishes for active poll
    active_dishes = [
        (poll_id_active, "Paneer Butter Masala & Garlic Naan", "Veg", "Rich creamy tomato gravy with cottage cheese & clay oven naan", 520, "Dairy, Gluten"),
        (poll_id_active, "Hyderabadi Dum Biryani with Mirchi Salan", "Special", "Authentic slow-cooked spiced basmati rice with raita", 650, "Dairy"),
        (poll_id_active, "South Indian Veg Thali with Crisp Dosa", "Veg", "Steamed rice, sambar, rasam, curd, poriyal & roast dosa", 480, "None"),
        (poll_id_active, "Grilled Veggie Pasta & Cheesy Garlic Bread", "Veg", "Penne in creamy alfredo sauce with herb-infused butter bread", 580, "Dairy, Gluten")
    ]
    cursor.executemany("""
    INSERT INTO dishes (poll_id, name, category, description, calories, allergens)
    VALUES (?, ?, ?, ?, ?, ?)
    """, active_dishes)
    
    # Pre-seed some votes for active poll from first 14 students
    cursor.execute("SELECT id, name FROM dishes WHERE poll_id = ?", (poll_id_active,))
    dish_rows = cursor.fetchall()
    if dish_rows:
        dish_map = {row['name']: row['id'] for row in dish_rows}
        sample_votes = [
            (poll_id_active, "H2024-101", dish_map.get("Hyderabadi Dum Biryani with Mirchi Salan", 2), (now - timedelta(minutes=45)).strftime("%Y-%m-%d %H:%M:%S")),
            (poll_id_active, "H2024-102", dish_map.get("Paneer Butter Masala & Garlic Naan", 1), (now - timedelta(minutes=40)).strftime("%Y-%m-%d %H:%M:%S")),
            (poll_id_active, "H2024-103", dish_map.get("Hyderabadi Dum Biryani with Mirchi Salan", 2), (now - timedelta(minutes=35)).strftime("%Y-%m-%d %H:%M:%S")),
            (poll_id_active, "H2024-104", dish_map.get("South Indian Veg Thali with Crisp Dosa", 3), (now - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")),
            (poll_id_active, "H2024-105", dish_map.get("Hyderabadi Dum Biryani with Mirchi Salan", 2), (now - timedelta(minutes=25)).strftime("%Y-%m-%d %H:%M:%S")),
            (poll_id_active, "H2024-106", dish_map.get("Grilled Veggie Pasta & Cheesy Garlic Bread", 4), (now - timedelta(minutes=20)).strftime("%Y-%m-%d %H:%M:%S")),
            (poll_id_active, "H2024-107", dish_map.get("Hyderabadi Dum Biryani with Mirchi Salan", 2), (now - timedelta(minutes=18)).strftime("%Y-%m-%d %H:%M:%S")),
            (poll_id_active, "H2024-108", dish_map.get("Paneer Butter Masala & Garlic Naan", 1), (now - timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")),
            (poll_id_active, "H2024-109", dish_map.get("Hyderabadi Dum Biryani with Mirchi Salan", 2), (now - timedelta(minutes=12)).strftime("%Y-%m-%d %H:%M:%S")),
            (poll_id_active, "H2024-110", dish_map.get("South Indian Veg Thali with Crisp Dosa", 3), (now - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")),
            (poll_id_active, "H2024-111", dish_map.get("Paneer Butter Masala & Garlic Naan", 1), (now - timedelta(minutes=8)).strftime("%Y-%m-%d %H:%M:%S")),
            (poll_id_active, "H2024-112", dish_map.get("Hyderabadi Dum Biryani with Mirchi Salan", 2), (now - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")),
            (poll_id_active, "H2024-113", dish_map.get("Grilled Veggie Pasta & Cheesy Garlic Bread", 4), (now - timedelta(minutes=3)).strftime("%Y-%m-%d %H:%M:%S")),
            (poll_id_active, "H2024-114", dish_map.get("Hyderabadi Dum Biryani with Mirchi Salan", 2), (now - timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S"))
        ]
        cursor.executemany("""
        INSERT INTO votes (poll_id, student_id, dish_id, voted_at)
        VALUES (?, ?, ?, ?)
        """, sample_votes)
        
    # Pre-seed a past expired poll (Yesterday's Dinner) so cook & admin can see completed analytics
    yesterday = now - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    yesterday_created = yesterday.replace(hour=16, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")
    yesterday_expired = yesterday.replace(hour=19, minute=30, second=0).strftime("%Y-%m-%d %H:%M:%S")
    past_poll_id = f"POLL-{yesterday.strftime('%Y%m%d')}-DINNER"
    
    cursor.execute("""
    INSERT INTO polls VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        past_poll_id,
        "Friday Night Dinner Choice",
        yesterday_str,
        "Dinner",
        yesterday_created,
        yesterday_expired,
        "Head Chef Suresh",
        "EXPIRED",
        "Voting closed at 7:30 PM. Kitchen successfully prepared winner dish.",
        ""
    ))
    
    past_dishes = [
        (past_poll_id, "Dal Makhani & Jeera Rice", "Veg", "Slow-cooked black lentils with fragrant cumin rice", 450, "Dairy"),
        (past_poll_id, "Chole Bhature with Pickled Onion", "Special", "Spiced chickpea curry with puffed bread", 620, "Gluten"),
        (past_poll_id, "Veg Hakka Noodles & Manchurian", "Veg", "Wok-tossed noodles with vegetable dumplings in soya gravy", 510, "Gluten, Soya")
    ]
    cursor.executemany("""
    INSERT INTO dishes (poll_id, name, category, description, calories, allergens)
    VALUES (?, ?, ?, ?, ?, ?)
    """, past_dishes)
    
    # Audit log entry
    cursor.execute("""
    INSERT INTO audit_logs (timestamp, action, performed_by, details)
    VALUES (?, ?, ?, ?)
    """, (
        now.strftime("%Y-%m-%d %H:%M:%S"),
        "POLL_GENERATION",
        "Cook: Head Chef Suresh",
        f"Generated QR Code for '{poll_id_active}' (Sunday Special Lunch Selection) with 4 dish options. Expiry set to {expiry_time}."
    ))
    
    conn.commit()

def check_and_update_expiries():
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
    UPDATE polls 
    SET status = 'EXPIRED' 
    WHERE status = 'ACTIVE' AND expires_at <= ?
    """, (now_str,))
    
    if cursor.rowcount > 0:
        cursor.execute("""
        INSERT INTO audit_logs (timestamp, action, performed_by, details)
        VALUES (?, ?, ?, ?)
        """, (
            now_str,
            "POLL_EXPIRED",
            "System Automation",
            f"Automatically closed {cursor.rowcount} poll(s) that reached their scheduled expiry time."
        ))
        conn.commit()
    conn.close()

def get_all_polls():
    check_and_update_expiries()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM polls ORDER BY created_at DESC")
    polls = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return polls

def get_active_polls():
    check_and_update_expiries()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM polls WHERE status = 'ACTIVE' ORDER BY created_at DESC")
    polls = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return polls

def get_poll_by_id(poll_id):
    check_and_update_expiries()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM polls WHERE id = ?", (poll_id,))
    poll_row = cursor.fetchone()
    if not poll_row:
        conn.close()
        return None
    
    poll = dict(poll_row)
    
    cursor.execute("SELECT * FROM dishes WHERE poll_id = ?", (poll_id,))
    poll['dishes'] = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT COUNT(*) FROM votes WHERE poll_id = ?", (poll_id,))
    poll['total_votes'] = cursor.fetchone()[0]
    
    conn.close()
    return poll

def create_new_poll(title, meal_type, date_str, expires_at_str, dishes, notes="", created_by="Head Chef"):
    conn = get_connection()
    cursor = conn.cursor()
    
    now = datetime.now()
    created_at = now.strftime("%Y-%m-%d %H:%M:%S")
    clean_meal = meal_type.upper()
    date_code = date_str.replace("-", "")
    poll_id = f"POLL-{date_code}-{clean_meal[:3]}-{now.strftime('%H%M')}"
    
    cursor.execute("""
    INSERT INTO polls (id, title, date, meal_type, created_at, expires_at, created_by, status, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, 'ACTIVE', ?)
    """, (poll_id, title, date_str, meal_type, created_at, expires_at_str, created_by, notes))
    
    for dish in dishes:
        cursor.execute("""
        INSERT INTO dishes (poll_id, name, category, description, calories, allergens)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            poll_id,
            dish.get('name', 'Unnamed Dish'),
            dish.get('category', 'Veg'),
            dish.get('description', ''),
            dish.get('calories', 0),
            dish.get('allergens', 'None')
        ))
        
    cursor.execute("""
    INSERT INTO audit_logs (timestamp, action, performed_by, details)
    VALUES (?, ?, ?, ?)
    """, (
        created_at,
        "POLL_CREATED",
        f"Cook ({created_by})",
        f"Generated poll '{title}' (ID: {poll_id}) for {meal_type} on {date_str} with {len(dishes)} dishes. Expiry set to {expires_at_str}."
    ))
    
    conn.commit()
    conn.close()
    return poll_id

def cast_vote(poll_id, student_id, dish_id):
    check_and_update_expiries()
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Check poll status
    cursor.execute("SELECT * FROM polls WHERE id = ?", (poll_id,))
    poll = cursor.fetchone()
    if not poll:
        conn.close()
        return False, "Poll does not exist."
    if poll['status'] != 'ACTIVE':
        conn.close()
        return False, f"This poll is {poll['status']}. Voting is closed!"
    
    # 2. Check student existence
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id.strip(),))
    student = cursor.fetchone()
    if not student:
        conn.close()
        return False, f"Student ID '{student_id}' not found in Hostel Roster."
        
    # 3. Check if already voted
    cursor.execute("SELECT * FROM votes WHERE poll_id = ? AND student_id = ?", (poll_id, student_id.strip()))
    if cursor.fetchone():
        conn.close()
        return False, f"Student {student['name']} ({student_id}) has ALREADY voted in this poll!"
        
    # 4. Check dish validity
    cursor.execute("SELECT * FROM dishes WHERE id = ? AND poll_id = ?", (dish_id, poll_id))
    dish = cursor.fetchone()
    if not dish:
        conn.close()
        return False, "Selected dish is invalid for this poll."
        
    # 5. Insert vote
    voted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO votes (poll_id, student_id, dish_id, voted_at)
    VALUES (?, ?, ?, ?)
    """, (poll_id, student_id.strip(), dish_id, voted_at))
    
    cursor.execute("""
    INSERT INTO audit_logs (timestamp, action, performed_by, details)
    VALUES (?, ?, ?, ?)
    """, (
        voted_at,
        "VOTE_CAST",
        f"Student: {student['name']} ({student_id})",
        f"Cast vote for dish '{dish['name']}' in poll '{poll['title']}' (Room: {student['room_no']})."
    ))
    
    conn.commit()
    conn.close()
    return True, f"Vote successfully recorded for {dish['name']}!"

def get_poll_results(poll_id):
    check_and_update_expiries()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM polls WHERE id = ?", (poll_id,))
    poll_row = cursor.fetchone()
    if not poll_row:
        conn.close()
        return None
    poll = dict(poll_row)
    
    # Get total votes
    cursor.execute("SELECT COUNT(*) FROM votes WHERE poll_id = ?", (poll_id,))
    total_votes = cursor.fetchone()[0]
    poll['total_votes'] = total_votes
    
    # Get dish votes
    cursor.execute("""
    SELECT d.id, d.name, d.category, d.description, d.calories, d.allergens,
           COUNT(v.id) AS vote_count
    FROM dishes d
    LEFT JOIN votes v ON d.id = v.dish_id AND v.poll_id = d.poll_id
    WHERE d.poll_id = ?
    GROUP BY d.id
    ORDER BY vote_count DESC, d.name ASC
    """, (poll_id,))
    
    dishes = []
    max_votes = -1
    winner = None
    for row in cursor.fetchall():
        d = dict(row)
        pct = (d['vote_count'] / total_votes * 100) if total_votes > 0 else 0
        d['percentage'] = round(pct, 1)
        if d['vote_count'] > max_votes and d['vote_count'] > 0:
            max_votes = d['vote_count']
            winner = d['name']
        dishes.append(d)
        
    poll['dishes'] = dishes
    poll['winner'] = winner if total_votes > 0 else "No votes yet"
    conn.close()
    return poll

def get_admin_detailed_data(poll_id):
    check_and_update_expiries()
    conn = get_connection()
    cursor = conn.cursor()
    
    # Poll info
    cursor.execute("SELECT * FROM polls WHERE id = ?", (poll_id,))
    poll_row = cursor.fetchone()
    if not poll_row:
        conn.close()
        return None
    poll_info = dict(poll_row)
    
    # Total students in hostel
    cursor.execute("SELECT COUNT(*) FROM students")
    total_hostel_students = cursor.fetchone()[0]
    
    # Students who polled
    cursor.execute("""
    SELECT s.student_id, s.name, s.room_no, s.block, s.department,
           d.name AS chosen_dish, d.category AS dish_category, v.voted_at
    FROM votes v
    JOIN students s ON v.student_id = s.student_id
    JOIN dishes d ON v.dish_id = d.id
    WHERE v.poll_id = ?
    ORDER BY v.voted_at DESC
    """, (poll_id,))
    polled_students = [dict(row) for row in cursor.fetchall()]
    
    # Students who didn't poll
    cursor.execute("""
    SELECT s.student_id, s.name, s.room_no, s.block, s.department, s.phone
    FROM students s
    WHERE s.student_id NOT IN (
        SELECT student_id FROM votes WHERE poll_id = ?
    )
    ORDER BY s.room_no ASC
    """, (poll_id,))
    non_polled_students = [dict(row) for row in cursor.fetchall()]
    
    # Dish breakdown
    results = get_poll_results(poll_id)
    
    conn.close()
    return {
        "poll": poll_info,
        "total_hostel_students": total_hostel_students,
        "polled_count": len(polled_students),
        "non_polled_count": len(non_polled_students),
        "turnout_pct": round((len(polled_students) / total_hostel_students * 100), 1) if total_hostel_students > 0 else 0,
        "polled_students": polled_students,
        "non_polled_students": non_polled_students,
        "dish_results": results['dishes'] if results else [],
        "winner": results['winner'] if results else "None"
    }

def get_dishes_by_date(date_str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT p.id as poll_id, p.title, p.meal_type, p.status, p.expires_at, p.created_by,
           d.id as dish_id, d.name as dish_name, d.category, d.description, d.calories, d.allergens
    FROM polls p
    JOIN dishes d ON p.id = d.poll_id
    WHERE p.date = ?
    ORDER BY p.meal_type ASC, d.name ASC
    """, (date_str,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY student_id ASC")
    students = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return students

def get_audit_logs(limit=50):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT ?", (limit,))
    logs = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return logs

def close_poll_manually(poll_id, closed_by="Cook"):
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE polls SET status = 'CLOSED' WHERE id = ?", (poll_id,))
    cursor.execute("""
    INSERT INTO audit_logs (timestamp, action, performed_by, details)
    VALUES (?, ?, ?, ?)
    """, (
        now_str,
        "POLL_MANUALLY_CLOSED",
        closed_by,
        f"Poll '{poll_id}' was manually closed before expiry."
    ))
    conn.commit()
    conn.close()
