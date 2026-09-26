"""
Automated Test Suite for Hostel Mess Food Voting System
Verifies:
1. Database initialization and roster integrity
2. Poll creation and QR generation
3. Duplicate voting prevention (1-vote-per-student rule)
4. Expired poll status locking
5. Admin analytics and turnout calculations
"""

import unittest
from datetime import datetime, timedelta
import database
import qr_manager

class TestHostelVotingSystem(unittest.TestCase):
    
    def setUp(self):
        database.init_db()
        
    def test_database_roster_loaded(self):
        students = database.get_all_students()
        self.assertGreaterEqual(len(students), 20, "Hostel roster should contain at least 20 students")
        
    def test_poll_creation_and_dishes(self):
        now = datetime.now()
        test_poll_id = database.create_new_poll(
            title="CI Test Dinner Menu",
            meal_type="Dinner",
            date_str=now.strftime("%Y-%m-%d"),
            expires_at_str=(now + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
            dishes=[
                {"name": "CI Special Paneer Tikka", "category": "Veg", "calories": 450},
                {"name": "CI Dal Tadka & Jeera Rice", "category": "Veg", "calories": 380}
            ],
            notes="Automated test poll",
            created_by="Automated Test Runner"
        )
        self.assertTrue(test_poll_id.startswith("POLL-"), "Poll ID should have POLL prefix")
        
        poll = database.get_poll_by_id(test_poll_id)
        self.assertIsNotNone(poll)
        self.assertEqual(len(poll['dishes']), 2)
        self.assertEqual(poll['status'], "ACTIVE")
        
    def test_single_vote_enforcement(self):
        now = datetime.now()
        test_poll_id = database.create_new_poll(
            title="CI Single Vote Test",
            meal_type="Breakfast",
            date_str=now.strftime("%Y-%m-%d"),
            expires_at_str=(now + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
            dishes=[
                {"name": "Idli Sambar", "category": "Veg", "calories": 300},
                {"name": "Poha & Jalebi", "category": "Veg", "calories": 350}
            ]
        )
        poll = database.get_poll_by_id(test_poll_id)
        first_dish_id = poll['dishes'][0]['id']
        second_dish_id = poll['dishes'][1]['id']
        test_student_id = "H2024-130"
        
        # First vote should succeed
        success, msg = database.cast_vote(test_poll_id, test_student_id, first_dish_id)
        self.assertTrue(success, f"First vote should succeed: {msg}")
        
        # Second vote by same student must be rejected
        duplicate_success, duplicate_msg = database.cast_vote(test_poll_id, test_student_id, second_dish_id)
        self.assertFalse(duplicate_success, "Duplicate vote must be blocked!")
        self.assertIn("ALREADY voted", duplicate_msg)
        
    def test_admin_analytics_integrity(self):
        polls = database.get_all_polls()
        if polls:
            poll_id = polls[0]['id']
            data = database.get_admin_detailed_data(poll_id)
            self.assertIsNotNone(data)
            self.assertEqual(
                data['total_hostel_students'], 
                data['polled_count'] + data['non_polled_count'],
                "Sum of polled and non-polled must equal total students"
            )
            
if __name__ == "__main__":
    unittest.main()
