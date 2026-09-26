"""
Main Application Entry Point
Hostel Mess Smart Food Voting System (100% Pure Python - Zero HTML/CSS/JS)
Baby Blue Theme, Smooth Animations, QR Generator & Camera Scanner, Role-Based Access Control.
"""

import sys
import os
import threading
import time
import customtkinter as ctk

from theme import *
from database import init_db, check_and_update_expiries
from animations import FrameTransitionManager
from views.login_view import LoginView
from views.cook_view import CookView
from views.student_view import StudentView
from views.admin_view import AdminView

class HostelVotingApp(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        
        # Configure App Window
        self.title("Hostel Mess Smart Food Voting System • [Baby Blue Edition]")
        self.geometry("1140x740")
        self.minsize(1020, 640)
        self.configure(fg_color=COLOR_BG_MAIN)
        
        # Appearance Mode
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")
        
        # Initialize SQLite Database & Sample Data
        init_db()
        
        # Main View Container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        
        self.current_view = None
        
        # Background Poll Expiry Monitor Thread
        self.is_running = True
        self.expiry_thread = threading.Thread(target=self.expiry_monitor_loop, daemon=True)
        self.expiry_thread.start()
        
        # Show Login View Initially
        self.show_login()
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def switch_view(self, new_view_class, *args, **kwargs):
        """Smooth animated transition to a new view"""
        old_view = self.current_view
        
        # Instantiate new view
        new_view = new_view_class(self.container, *args, **kwargs)
        
        if old_view is not None:
            # Animate slide transition
            FrameTransitionManager.slide_in(
                new_view, 
                direction="right", 
                duration_ms=220, 
                steps=12,
                callback=lambda: old_view.destroy()
            )
        else:
            new_view.place(relx=0, rely=0, relwidth=1, relheight=1)
            
        self.current_view = new_view
        
    def show_login(self):
        self.switch_view(LoginView, on_role_selected=self.on_role_selected)
        
    def show_cook(self):
        self.switch_view(CookView, on_logout=self.show_login)
        
    def show_student(self):
        self.switch_view(StudentView, on_logout=self.show_login)
        
    def show_admin(self):
        self.switch_view(AdminView, on_logout=self.show_login)
        
    def on_role_selected(self, role):
        if role == "cook":
            self.show_cook()
        elif role == "student":
            self.show_student()
        elif role == "admin":
            self.show_admin()
            
    def expiry_monitor_loop(self):
        """Continuously checks if any active poll has reached its expiry time"""
        while self.is_running:
            try:
                check_and_update_expiries()
            except Exception:
                pass
            time.sleep(5)
            
    def on_close(self):
        self.is_running = False
        self.destroy()

if __name__ == "__main__":
    app = HostelVotingApp()
    app.mainloop()
