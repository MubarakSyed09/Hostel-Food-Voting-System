"""
Hostel Student Voting Portal
Strictly limited to scanning QR code, viewing dishes, choosing food item, and submitting vote.
"""

from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

from theme import *
from database import (
    get_all_students, 
    get_active_polls, 
    get_all_polls, 
    get_poll_by_id, 
    cast_vote
)
from qr_manager import CameraQRScannerDialog
from animations import PulsingTimerBadge, ConfettiCelebrationCanvas

class StudentView(ctk.CTkFrame):
    
    def __init__(self, parent, on_logout):
        super().__init__(parent, fg_color=COLOR_BG_MAIN)
        self.parent = parent
        self.on_logout = on_logout
        
        self.students = get_all_students()
        self.current_student = self.students[0] if self.students else None
        
        self.selected_poll_id = None
        self.current_poll = None
        self.selected_dish_id = tk.IntVar(value=-1)
        self.dish_cards = {}
        
        self.setup_ui()
        
    def setup_ui(self):
        # 1. Top Navbar
        navbar = ctk.CTkFrame(self, fg_color=COLOR_BG_CARD, height=65, corner_radius=0, border_width=1, border_color=COLOR_BORDER_LIGHT)
        navbar.pack(fill="x", side="top")
        navbar.pack_propagate(False)
        
        # Left Student identity
        brand_frame = ctk.CTkFrame(navbar, fg_color="transparent")
        brand_frame.pack(side="left", padx=25)
        
        icon_lbl = ctk.CTkLabel(brand_frame, text="🎓", font=("Segoe UI", 24))
        icon_lbl.pack(side="left", padx=(0, 10))
        
        title_lbl = ctk.CTkLabel(brand_frame, text="Hostel Student Food Poll", font=FONT_TITLE, text_color=COLOR_PRIMARY_DARK)
        title_lbl.pack(side="left")
        
        # Center: Student Selector
        center_frame = ctk.CTkFrame(navbar, fg_color="transparent")
        center_frame.pack(side="left", padx=30)
        
        ctk.CTkLabel(center_frame, text="Logged in as:", font=FONT_CAPTION_BOLD, text_color=COLOR_TEXT_MUTED).pack(side="left", padx=(0, 6))
        
        student_options = [f"{s['student_id']} - {s['name']} (Room {s['room_no']})" for s in self.students]
        self.student_var = ctk.StringVar(value=student_options[0] if student_options else "")
        self.student_menu = ctk.CTkOptionMenu(
            center_frame,
            values=student_options[:30],
            variable=self.student_var,
            fg_color=COLOR_LIGHT_ACCENT,
            text_color=COLOR_DEEP_OCEAN,
            button_color=COLOR_PRIMARY,
            button_hover_color=COLOR_PRIMARY_HOVER,
            width=280,
            command=self.on_student_changed
        )
        self.student_menu.pack(side="left")
        
        # Right actions
        nav_right = ctk.CTkFrame(navbar, fg_color="transparent")
        nav_right.pack(side="right", padx=25)
        
        logout_btn = ctk.CTkButton(
            nav_right,
            text="🚪 Back to Roles",
            font=FONT_BODY,
            fg_color="#F1F5F9",
            hover_color="#E2E8F0",
            text_color=COLOR_TEXT_MAIN,
            corner_radius=CORNER_RADIUS_BUTTON,
            width=120,
            command=self.on_logout
        )
        logout_btn.pack(side="right")
        
        # 2. Main Scrollable Container
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True, padx=25, pady=(15, 20))
        
        # Section A: QR Scanning & Quick Selection Banner
        self.setup_scan_banner()
        
        # Section B: Active Poll Content Area (Rendered dynamically)
        self.poll_content_frame = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        self.poll_content_frame.pack(fill="both", expand=True)
        
        # Auto-load the first active poll if available
        active = get_active_polls()
        if active:
            self.load_poll(active[0]['id'])
        else:
            all_polls = get_all_polls()
            if all_polls:
                self.load_poll(all_polls[0]['id'])
            else:
                self.show_no_polls()
                
    def setup_scan_banner(self):
        banner = ctk.CTkFrame(
            self.scroll_container, 
            fg_color=COLOR_BG_CARD, 
            border_width=1, 
            border_color=COLOR_BORDER, 
            corner_radius=CORNER_RADIUS_CARD
        )
        banner.pack(fill="x", pady=(0, 15))
        
        top_row = ctk.CTkFrame(banner, fg_color="transparent")
        top_row.pack(fill="x", padx=20, pady=12)
        
        # Left title
        b_left = ctk.CTkFrame(top_row, fg_color="transparent")
        b_left.pack(side="left")
        ctk.CTkLabel(b_left, text="📱 Scan Cook's Food QR Code", font=FONT_SUBTITLE, text_color=COLOR_PRIMARY_DARK).pack(anchor="w")
        ctk.CTkLabel(b_left, text="Use camera to scan QR displayed at the mess or select active meal poll below", font=FONT_CAPTION, text_color=COLOR_TEXT_MUTED).pack(anchor="w")
        
        # Right action buttons
        b_right = ctk.CTkFrame(top_row, fg_color="transparent")
        b_right.pack(side="right")
        
        # Live camera scan button
        scan_btn = ctk.CTkButton(
            b_right,
            text="📷 Scan QR with Camera",
            font=FONT_BODY_BOLD,
            fg_color=COLOR_PRIMARY_DARK,
            hover_color=COLOR_DEEP_OCEAN,
            text_color="#FFFFFF",
            corner_radius=CORNER_RADIUS_BUTTON,
            height=36,
            command=self.open_camera_scanner
        )
        scan_btn.pack(side="right", padx=(10, 0))
        
        # Quick poll selector dropdown
        polls = get_all_polls()
        poll_titles = [f"{p['meal_type'].upper()}: {p['title']} ({p['id']})" for p in polls] if polls else ["No polls available"]
        self.poll_select_var = ctk.StringVar(value=poll_titles[0] if poll_titles else "")
        self.poll_select_menu = ctk.CTkOptionMenu(
            b_right,
            values=poll_titles,
            variable=self.poll_select_var,
            fg_color=COLOR_LIGHT_ACCENT,
            text_color=COLOR_DEEP_OCEAN,
            button_color=COLOR_PRIMARY,
            button_hover_color=COLOR_PRIMARY_HOVER,
            width=280,
            command=self.on_poll_dropdown_selected
        )
        self.poll_select_menu.pack(side="right")
        
    def on_student_changed(self, val):
        student_id = val.split(" - ")[0].strip()
        for s in self.students:
            if s['student_id'] == student_id:
                self.current_student = s
                break
        # Re-render current poll to refresh student's voting status
        if self.selected_poll_id:
            self.load_poll(self.selected_poll_id)
            
    def on_poll_dropdown_selected(self, val):
        if "(" in val and ")" in val:
            poll_id = val.split("(")[-1].replace(")", "").strip()
            self.load_poll(poll_id)
            
    def open_camera_scanner(self):
        CameraQRScannerDialog(self, on_detected_callback=self.on_qr_detected)
        
    def on_qr_detected(self, poll_id):
        self.load_poll(poll_id)
        
    def show_no_polls(self):
        for w in self.poll_content_frame.winfo_children():
            w.destroy()
        msg_card = ctk.CTkFrame(self.poll_content_frame, fg_color=COLOR_BG_CARD, border_width=1, border_color=COLOR_BORDER, corner_radius=CORNER_RADIUS_CARD)
        msg_card.pack(fill="x", pady=20)
        ctk.CTkLabel(msg_card, text="🍽️ No Active Food Polls Right Now", font=FONT_TITLE, text_color=COLOR_PRIMARY_DARK).pack(pady=(30, 8))
        ctk.CTkLabel(msg_card, text="The hostel cook hasn't published a meal poll yet. Please check back when kitchen announces the QR code!", font=FONT_BODY, text_color=COLOR_TEXT_MUTED).pack(pady=(0, 30))
        
    def load_poll(self, poll_id):
        self.selected_poll_id = poll_id
        self.current_poll = get_poll_by_id(poll_id)
        
        for w in self.poll_content_frame.winfo_children():
            w.destroy()
            
        if not self.current_poll:
            ctk.CTkLabel(self.poll_content_frame, text=f"Poll '{poll_id}' not found.", font=FONT_BODY, text_color=COLOR_DANGER).pack(pady=20)
            return
            
        poll = self.current_poll
        is_active = poll['status'] == 'ACTIVE'
        
        # 1. Header Banner
        banner_bg = COLOR_LIGHT_ACCENT if is_active else "#FEE2E2"
        banner_border = COLOR_BORDER if is_active else "#FECACA"
        
        header = ctk.CTkFrame(self.poll_content_frame, fg_color=banner_bg, border_width=1, border_color=banner_border, corner_radius=CORNER_RADIUS_CARD)
        header.pack(fill="x", pady=(0, 15))
        
        h_top = ctk.CTkFrame(header, fg_color="transparent")
        h_top.pack(fill="x", padx=20, pady=(15, 6))
        
        title_box = ctk.CTkFrame(h_top, fg_color="transparent")
        title_box.pack(side="left")
        
        meal_pill = ctk.CTkFrame(title_box, fg_color=COLOR_PRIMARY_DARK, corner_radius=CORNER_RADIUS_PILL)
        meal_pill.pack(side="left", padx=(0, 10))
        ctk.CTkLabel(meal_pill, text=poll['meal_type'].upper(), font=FONT_CAPTION_BOLD, text_color="#FFFFFF").pack(padx=10, pady=2)
        
        ctk.CTkLabel(title_box, text=poll['title'], font=FONT_TITLE, text_color=COLOR_PRIMARY_DARK).pack(side="left")
        
        # Countdown Timer
        if is_active:
            timer = PulsingTimerBadge(
                h_top, 
                expires_at_iso=poll['expires_at'], 
                on_expire_callback=lambda: self.load_poll(poll_id)
            )
            timer.pack(side="right")
        else:
            closed_badge = ctk.CTkFrame(h_top, fg_color=COLOR_DANGER, corner_radius=CORNER_RADIUS_PILL)
            closed_badge.pack(side="right")
            ctk.CTkLabel(closed_badge, text="🔒 VOTING CLOSED (EXPIRED)", font=FONT_CAPTION_BOLD, text_color="#FFFFFF").pack(padx=12, pady=4)
            
        # Sub-info
        ctk.CTkLabel(
            header,
            text=f"📅 Date: {poll['date']}  •  Cook Incharge: {poll['created_by']}  •  Poll ID: {poll['id']}",
            font=FONT_BODY,
            text_color=COLOR_DEEP_OCEAN
        ).pack(anchor="w", padx=20, pady=(0, 4))
        
        if poll.get('notes'):
            ctk.CTkLabel(
                header,
                text=f"Kitchen Note: \"{poll['notes']}\"",
                font=FONT_CAPTION,
                text_color=COLOR_TEXT_MUTED
            ).pack(anchor="w", padx=20, pady=(0, 15))
            
        # 2. Check if this student already voted
        has_voted, voted_dish_name = self.check_if_voted(poll_id, self.current_student['student_id'])
        
        if has_voted:
            voted_card = ctk.CTkFrame(self.poll_content_frame, fg_color=COLOR_SUCCESS_LIGHT, border_width=1, border_color=COLOR_SUCCESS, corner_radius=CORNER_RADIUS_CARD)
            voted_card.pack(fill="x", pady=(0, 15))
            
            v_row = ctk.CTkFrame(voted_card, fg_color="transparent")
            v_row.pack(fill="x", padx=20, pady=12)
            
            ctk.CTkLabel(v_row, text="✅ YOU HAVE ALREADY POLLED FOR THIS MEAL", font=FONT_HEADING, text_color="#065F46").pack(side="left")
            ctk.CTkLabel(v_row, text=f"Your Selected Choice: {voted_dish_name}", font=FONT_BODY_BOLD, text_color="#047857").pack(side="right")
            
        elif not is_active:
            exp_card = ctk.CTkFrame(self.poll_content_frame, fg_color="#FEE2E2", border_width=1, border_color=COLOR_DANGER, corner_radius=CORNER_RADIUS_CARD)
            exp_card.pack(fill="x", pady=(0, 15))
            ctk.CTkLabel(exp_card, text="⚠️ Voting window has ended! The kitchen staff is currently preparing the winning dish.", font=FONT_BODY_BOLD, text_color=COLOR_DANGER).pack(pady=12)
            
        # 3. Candidate Dishes Grid
        dishes_header = ctk.CTkFrame(self.poll_content_frame, fg_color="transparent")
        dishes_header.pack(fill="x", pady=(5, 8))
        ctk.CTkLabel(dishes_header, text="🍽️ Available Dishes (Cook's Options)", font=FONT_SUBTITLE, text_color=COLOR_PRIMARY_DARK).pack(side="left")
        ctk.CTkLabel(dishes_header, text="Select 1 food item of your choice", font=FONT_BODY, text_color=COLOR_TEXT_MUTED).pack(side="right")
        
        self.selected_dish_id.set(-1)
        self.dish_cards.clear()
        
        dishes = poll.get('dishes', [])
        for d in dishes:
            self.create_dish_option_card(d, is_active and not has_voted)
            
        # 4. Submit Vote Action Button
        if is_active and not has_voted:
            btn_frame = ctk.CTkFrame(self.poll_content_frame, fg_color="transparent")
            btn_frame.pack(fill="x", pady=(20, 15))
            
            self.vote_btn = ctk.CTkButton(
                btn_frame,
                text="🗳️ Submit My Food Vote",
                font=FONT_TITLE,
                fg_color=COLOR_PRIMARY_DARK,
                hover_color=COLOR_DEEP_OCEAN,
                text_color="#FFFFFF",
                height=52,
                corner_radius=CORNER_RADIUS_CARD,
                command=self.submit_vote
            )
            self.vote_btn.pack(fill="x")
            
    def create_dish_option_card(self, dish, can_select):
        d_id = dish['id']
        
        card = ctk.CTkFrame(
            self.poll_content_frame,
            fg_color=COLOR_BG_CARD,
            border_width=1,
            border_color=COLOR_BORDER,
            corner_radius=CORNER_RADIUS_CARD
        )
        card.pack(fill="x", pady=6)
        self.dish_cards[d_id] = card
        
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=12)
        
        # Radio button
        if can_select:
            radio = ctk.CTkRadioButton(
                row,
                text="",
                value=d_id,
                variable=self.selected_dish_id,
                fg_color=COLOR_PRIMARY,
                border_color=COLOR_PRIMARY_DARK,
                hover_color=COLOR_PRIMARY_HOVER,
                width=24,
                command=lambda: self.highlight_selected_dish(d_id)
            )
            radio.pack(side="left", padx=(0, 15))
            
            # Clicking entire card selects dish
            card.bind("<Button-1>", lambda e, did=d_id: self.select_dish_by_id(did))
            row.bind("<Button-1>", lambda e, did=d_id: self.select_dish_by_id(did))
            
        # Category Badge
        cat = dish.get('category', 'Veg')
        badge_bg = COLOR_SUCCESS_LIGHT if cat == 'Veg' else (COLOR_DANGER_LIGHT if cat == 'Non-Veg' else COLOR_SPECIAL_LIGHT)
        badge_fg = COLOR_SUCCESS if cat == 'Veg' else (COLOR_DANGER if cat == 'Non-Veg' else COLOR_SPECIAL)
        badge = ctk.CTkFrame(row, fg_color=badge_bg, corner_radius=8)
        badge.pack(side="left", padx=(0, 12))
        ctk.CTkLabel(badge, text=cat.upper(), font=FONT_CAPTION_BOLD, text_color=badge_fg).pack(padx=8, pady=2)
        
        # Dish details
        details_box = ctk.CTkFrame(row, fg_color="transparent")
        details_box.pack(side="left", fill="x", expand=True)
        
        name_lbl = ctk.CTkLabel(details_box, text=dish['name'], font=FONT_BODY_BOLD, text_color=COLOR_TEXT_MAIN, anchor="w")
        name_lbl.pack(fill="x")
        
        if dish.get('description'):
            desc_lbl = ctk.CTkLabel(details_box, text=dish['description'], font=FONT_CAPTION, text_color=COLOR_TEXT_MUTED, anchor="w")
            desc_lbl.pack(fill="x")
            
        # Calories & Allergens
        right_box = ctk.CTkFrame(row, fg_color="transparent")
        right_box.pack(side="right", padx=(10, 0))
        
        if dish.get('calories'):
            ctk.CTkLabel(right_box, text=f"🔥 {dish['calories']} kcal", font=FONT_CAPTION_BOLD, text_color=COLOR_TEXT_BLUE).pack(anchor="e")
        if dish.get('allergens') and dish['allergens'] != 'None':
            ctk.CTkLabel(right_box, text=f"⚠️ {dish['allergens']}", font=FONT_CAPTION, text_color=COLOR_WARNING).pack(anchor="e")
            
    def select_dish_by_id(self, dish_id):
        self.selected_dish_id.set(dish_id)
        self.highlight_selected_dish(dish_id)
        
    def highlight_selected_dish(self, chosen_id):
        for did, card in self.dish_cards.items():
            if did == chosen_id:
                card.configure(border_color=COLOR_PRIMARY, border_width=2, fg_color=COLOR_LIGHT_ACCENT)
            else:
                card.configure(border_color=COLOR_BORDER, border_width=1, fg_color=COLOR_BG_CARD)
                
    def check_if_voted(self, poll_id, student_id):
        from database import get_connection
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
        SELECT d.name FROM votes v 
        JOIN dishes d ON v.dish_id = d.id 
        WHERE v.poll_id = ? AND v.student_id = ?
        """, (poll_id, student_id))
        row = c.fetchone()
        conn.close()
        if row:
            return True, row[0]
        return False, None
        
    def submit_vote(self):
        dish_id = self.selected_dish_id.get()
        if dish_id <= 0:
            messagebox.showwarning("Choice Required", "Please tap or click to choose a food item before voting.")
            return
            
        student_id = self.current_student['student_id']
        poll_id = self.selected_poll_id
        
        # Cast vote in DB
        success, msg = cast_vote(poll_id, student_id, dish_id)
        
        if success:
            # Trigger celebration confetti animation
            ConfettiCelebrationCanvas(self)
            # Reload poll to show updated state
            self.parent.after(400, lambda: self.load_poll(poll_id))
        else:
            messagebox.showerror("Voting Failed", msg)
