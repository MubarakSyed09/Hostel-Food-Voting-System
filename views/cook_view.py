"""
Hostel Cook Portal
Strictly limited to adding dishes, setting expiry time, generating QR code, and viewing poll results.
"""

import os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
from PIL import Image

from theme import *
from database import (
    create_new_poll, 
    get_all_polls, 
    get_poll_by_id, 
    get_poll_results, 
    close_poll_manually
)
from qr_manager import QRManager, QR_STORAGE_DIR
from animations import AnimatedProgressBar, PulsingTimerBadge

class CookView(ctk.CTkFrame):
    
    def __init__(self, parent, on_logout):
        super().__init__(parent, fg_color=COLOR_BG_MAIN)
        self.parent = parent
        self.on_logout = on_logout
        
        self.current_dishes = []
        self.active_timer_badge = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # 1. Top Navbar
        navbar = ctk.CTkFrame(self, fg_color=COLOR_BG_CARD, height=65, corner_radius=0, border_width=1, border_color=COLOR_BORDER_LIGHT)
        navbar.pack(fill="x", side="top")
        navbar.pack_propagate(False)
        
        # Left brand
        brand_frame = ctk.CTkFrame(navbar, fg_color="transparent")
        brand_frame.pack(side="left", padx=25)
        
        chef_icon = ctk.CTkLabel(brand_frame, text="👨‍🍳", font=("Segoe UI", 24))
        chef_icon.pack(side="left", padx=(0, 10))
        
        brand_title = ctk.CTkLabel(brand_frame, text="Hostel Kitchen Cook Portal", font=FONT_TITLE, text_color=COLOR_PRIMARY_DARK)
        brand_title.pack(side="left")
        
        role_pill = ctk.CTkFrame(brand_frame, fg_color=COLOR_LIGHT_ACCENT, corner_radius=CORNER_RADIUS_PILL)
        role_pill.pack(side="left", padx=12)
        role_pill_lbl = ctk.CTkLabel(role_pill, text="Chef Suresh (Mess Incharge)", font=FONT_CAPTION_BOLD, text_color=COLOR_DEEP_OCEAN)
        role_pill_lbl.pack(padx=10, pady=2)
        
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
        
        # 2. Main Tabview
        self.tabview = ctk.CTkTabview(
            self,
            fg_color="transparent",
            segmented_button_fg_color=COLOR_BG_CARD,
            segmented_button_selected_color=COLOR_PRIMARY,
            segmented_button_selected_hover_color=COLOR_PRIMARY_HOVER,
            segmented_button_unselected_color=COLOR_LIGHT_ACCENT,
            segmented_button_unselected_hover_color=COLOR_LIGHT_ACCENT_HOVER,
            text_color=COLOR_TEXT_MAIN,
            corner_radius=CORNER_RADIUS_CARD
        )
        self.tabview.pack(fill="both", expand=True, padx=25, pady=(15, 20))
        
        self.tab_create = self.tabview.add("➕  Create Food Poll & Generate QR")
        self.tab_results = self.tabview.add("📊  View Live & Past Results")
        
        self.setup_create_tab()
        self.setup_results_tab()
        
    def setup_create_tab(self):
        container = ctk.CTkScrollableFrame(self.tab_create, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Main form card
        form_card = ctk.CTkFrame(container, fg_color=COLOR_BG_CARD, border_width=1, border_color=COLOR_BORDER, corner_radius=CORNER_RADIUS_CARD)
        form_card.pack(fill="x", pady=(0, 15), padx=5)
        
        # Header of card
        f_header = ctk.CTkFrame(form_card, fg_color=COLOR_LIGHT_ACCENT, corner_radius=CORNER_RADIUS_CARD, height=45)
        f_header.pack(fill="x", padx=10, pady=10)
        f_header.pack_propagate(False)
        
        f_title = ctk.CTkLabel(f_header, text="📋 Step 1: Set Meal Session & Expiry Time", font=FONT_SUBTITLE, text_color=COLOR_PRIMARY_DARK)
        f_title.pack(side="left", padx=15)
        
        # Grid fields
        grid_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=10)
        
        # Row 1: Meal Type & Title
        r1 = ctk.CTkFrame(grid_frame, fg_color="transparent")
        r1.pack(fill="x", pady=6)
        
        c1 = ctk.CTkFrame(r1, fg_color="transparent")
        c1.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkLabel(c1, text="Meal Category *", font=FONT_BODY_BOLD, text_color=COLOR_TEXT_MAIN).pack(anchor="w")
        self.meal_type_var = ctk.StringVar(value="Lunch")
        self.meal_menu = ctk.CTkOptionMenu(
            c1, 
            values=["Breakfast", "Lunch", "Snacks", "Dinner"],
            variable=self.meal_type_var,
            fg_color=COLOR_LIGHT_ACCENT,
            text_color=COLOR_DEEP_OCEAN,
            button_color=COLOR_PRIMARY,
            button_hover_color=COLOR_PRIMARY_HOVER,
            corner_radius=CORNER_RADIUS_BUTTON
        )
        self.meal_menu.pack(fill="x", pady=(4, 0))
        
        c2 = ctk.CTkFrame(r1, fg_color="transparent")
        c2.pack(side="right", fill="x", expand=True, padx=(10, 0))
        ctk.CTkLabel(c2, text="Poll Title *", font=FONT_BODY_BOLD, text_color=COLOR_TEXT_MAIN).pack(anchor="w")
        self.title_entry = ctk.CTkEntry(
            c2,
            placeholder_text="e.g. Special Weekend Lunch Menu",
            fg_color=COLOR_BG_CARD_ALT,
            border_color=COLOR_BORDER,
            corner_radius=CORNER_RADIUS_BUTTON
        )
        self.title_entry.insert(0, f"Special Lunch Selection")
        self.title_entry.pack(fill="x", pady=(4, 0))
        
        # Row 2: Date & Expiry Presets
        r2 = ctk.CTkFrame(grid_frame, fg_color="transparent")
        r2.pack(fill="x", pady=6)
        
        c3 = ctk.CTkFrame(r2, fg_color="transparent")
        c3.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkLabel(c3, text="Date (YYYY-MM-DD) *", font=FONT_BODY_BOLD, text_color=COLOR_TEXT_MAIN).pack(anchor="w")
        self.date_entry = ctk.CTkEntry(
            c3,
            fg_color=COLOR_BG_CARD_ALT,
            border_color=COLOR_BORDER,
            corner_radius=CORNER_RADIUS_BUTTON
        )
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.pack(fill="x", pady=(4, 0))
        
        c4 = ctk.CTkFrame(r2, fg_color="transparent")
        c4.pack(side="right", fill="x", expand=True, padx=(10, 0))
        ctk.CTkLabel(c4, text="Voting Expiry Duration *", font=FONT_BODY_BOLD, text_color=COLOR_TEXT_MAIN).pack(anchor="w")
        
        self.expiry_duration_var = ctk.StringVar(value="In 2 Hours")
        self.expiry_menu = ctk.CTkOptionMenu(
            c4,
            values=["In 30 Minutes", "In 1 Hour", "In 2 Hours", "In 3 Hours", "In 5 Hours", "Tonight (8:00 PM)"],
            variable=self.expiry_duration_var,
            fg_color=COLOR_LIGHT_ACCENT,
            text_color=COLOR_DEEP_OCEAN,
            button_color=COLOR_PRIMARY,
            button_hover_color=COLOR_PRIMARY_HOVER,
            corner_radius=CORNER_RADIUS_BUTTON,
            command=self.update_expiry_preview
        )
        self.expiry_menu.pack(fill="x", pady=(4, 0))
        
        # Expiry preview notice
        self.expiry_preview_lbl = ctk.CTkLabel(
            form_card,
            text="⏳ Voting will automatically lock and calculate results at: ...",
            font=FONT_BODY_BOLD,
            text_color=COLOR_WARNING
        )
        self.expiry_preview_lbl.pack(pady=(4, 15))
        self.update_expiry_preview()
        
        # --- Step 2: Limited Options Dish Builder ---
        dishes_card = ctk.CTkFrame(container, fg_color=COLOR_BG_CARD, border_width=1, border_color=COLOR_BORDER, corner_radius=CORNER_RADIUS_CARD)
        dishes_card.pack(fill="x", pady=(0, 15), padx=5)
        
        d_header = ctk.CTkFrame(dishes_card, fg_color=COLOR_LIGHT_ACCENT, corner_radius=CORNER_RADIUS_CARD, height=45)
        d_header.pack(fill="x", padx=10, pady=10)
        d_header.pack_propagate(False)
        
        d_title = ctk.CTkLabel(d_header, text="🍲 Step 2: Add Limited Food Options (Cook's Choices)", font=FONT_SUBTITLE, text_color=COLOR_PRIMARY_DARK)
        d_title.pack(side="left", padx=15)
        
        limit_notice = ctk.CTkLabel(d_header, text="Limited to 2-6 choices", font=FONT_CAPTION_BOLD, text_color=COLOR_DEEP_OCEAN)
        limit_notice.pack(side="right", padx=15)
        
        # Add dish entry inputs
        input_row = ctk.CTkFrame(dishes_card, fg_color="transparent")
        input_row.pack(fill="x", padx=20, pady=10)
        
        self.dish_name_entry = ctk.CTkEntry(input_row, placeholder_text="Dish Name (e.g. Kadai Paneer & Kulcha)", fg_color=COLOR_BG_CARD_ALT, border_color=COLOR_BORDER, width=280)
        self.dish_name_entry.pack(side="left", padx=(0, 10))
        
        self.dish_cat_var = ctk.StringVar(value="Veg")
        self.dish_cat_menu = ctk.CTkOptionMenu(input_row, values=["Veg", "Non-Veg", "Special"], variable=self.dish_cat_var, fg_color=COLOR_LIGHT_ACCENT, text_color=COLOR_DEEP_OCEAN, button_color=COLOR_PRIMARY, width=110)
        self.dish_cat_menu.pack(side="left", padx=(0, 10))
        
        self.dish_cal_entry = ctk.CTkEntry(input_row, placeholder_text="Calories (e.g. 520)", fg_color=COLOR_BG_CARD_ALT, border_color=COLOR_BORDER, width=120)
        self.dish_cal_entry.pack(side="left", padx=(0, 10))
        
        add_btn = ctk.CTkButton(
            input_row,
            text="➕ Add Dish",
            font=FONT_BODY_BOLD,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT_MAIN,
            corner_radius=CORNER_RADIUS_BUTTON,
            width=110,
            command=self.add_dish_to_list
        )
        add_btn.pack(side="left")
        
        # List container for added dishes
        self.dishes_list_frame = ctk.CTkFrame(dishes_card, fg_color="transparent")
        self.dishes_list_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Pre-populate 3 default candidate dishes
        self.current_dishes = [
            {"name": "Paneer Butter Masala & Garlic Naan", "category": "Veg", "calories": 520, "description": "Fresh cottage cheese in makhani gravy"},
            {"name": "Hyderabadi Dum Biryani with Salan", "category": "Special", "calories": 650, "description": "Slow cooked basmati rice with spices"},
            {"name": "South Indian Feast & Crisp Roast Dosa", "category": "Veg", "calories": 480, "description": "Served with hot sambar and chutney"}
        ]
        self.render_dish_list()
        
        # --- Step 3: Big Publish & Generate QR Button ---
        pub_frame = ctk.CTkFrame(container, fg_color="transparent")
        pub_frame.pack(fill="x", pady=15, padx=5)
        
        self.generate_btn = ctk.CTkButton(
            pub_frame,
            text="🚀 Generate QR Code & Publish Poll to Students",
            font=FONT_TITLE,
            fg_color=COLOR_PRIMARY_DARK,
            hover_color=COLOR_DEEP_OCEAN,
            text_color="#FFFFFF",
            height=54,
            corner_radius=CORNER_RADIUS_CARD,
            command=self.publish_and_generate_qr
        )
        self.generate_btn.pack(fill="x")
        
    def render_dish_list(self):
        for widget in self.dishes_list_frame.winfo_children():
            widget.destroy()
            
        if not self.current_dishes:
            ctk.CTkLabel(self.dishes_list_frame, text="No dishes added yet. Please add at least 2 dishes above.", font=FONT_BODY, text_color=COLOR_TEXT_MUTED).pack(pady=10)
            return
            
        for idx, d in enumerate(self.current_dishes):
            row = ctk.CTkFrame(self.dishes_list_frame, fg_color=COLOR_BG_CARD_ALT, border_width=1, border_color=COLOR_BORDER_LIGHT, corner_radius=10, height=45)
            row.pack(fill="x", pady=4)
            row.pack_propagate(False)
            
            # Badge
            badge_color = COLOR_SUCCESS_LIGHT if d['category'] == 'Veg' else (COLOR_DANGER_LIGHT if d['category'] == 'Non-Veg' else COLOR_SPECIAL_LIGHT)
            badge_txt_color = COLOR_SUCCESS if d['category'] == 'Veg' else (COLOR_DANGER if d['category'] == 'Non-Veg' else COLOR_SPECIAL)
            badge = ctk.CTkFrame(row, fg_color=badge_color, corner_radius=10)
            badge.pack(side="left", padx=10)
            ctk.CTkLabel(badge, text=d['category'], font=FONT_CAPTION_BOLD, text_color=badge_txt_color).pack(padx=8, pady=2)
            
            # Dish Name
            ctk.CTkLabel(row, text=f"{idx+1}. {d['name']}", font=FONT_BODY_BOLD, text_color=COLOR_TEXT_MAIN).pack(side="left", padx=10)
            
            # Calories
            if d.get('calories'):
                ctk.CTkLabel(row, text=f"🔥 {d['calories']} kcal", font=FONT_CAPTION, text_color=COLOR_TEXT_MUTED).pack(side="left", padx=10)
                
            # Remove button
            del_btn = ctk.CTkButton(
                row,
                text="❌ Remove",
                font=FONT_CAPTION_BOLD,
                fg_color="#FEE2E2",
                hover_color="#FECACA",
                text_color=COLOR_DANGER,
                width=80,
                height=26,
                corner_radius=6,
                command=lambda i=idx: self.remove_dish(i)
            )
            del_btn.pack(side="right", padx=10)
            
    def add_dish_to_list(self):
        name = self.dish_name_entry.get().strip()
        if not name:
            messagebox.showwarning("Incomplete", "Please enter a dish name.")
            return
            
        if len(self.current_dishes) >= 6:
            messagebox.showwarning("Limit Reached", "Cook can provide a maximum of 6 limited food options.")
            return
            
        cat = self.dish_cat_var.get()
        cal = self.dish_cal_entry.get().strip()
        cal_val = int(cal) if cal.isdigit() else 450
        
        self.current_dishes.append({
            "name": name,
            "category": cat,
            "calories": cal_val,
            "description": f"Freshly prepared {cat.lower()} dish by mess kitchen"
        })
        
        self.dish_name_entry.delete(0, 'end')
        self.dish_cal_entry.delete(0, 'end')
        self.render_dish_list()
        
    def remove_dish(self, index):
        if len(self.current_dishes) <= 2:
            messagebox.showwarning("Minimum Required", "You must keep at least 2 food options for students to vote between!")
            return
        self.current_dishes.pop(index)
        self.render_dish_list()
        
    def get_expiry_datetime_str(self):
        now = datetime.now()
        choice = self.expiry_duration_var.get()
        if "30 Min" in choice:
            target = now + timedelta(minutes=30)
        elif "1 Hour" in choice:
            target = now + timedelta(hours=1)
        elif "2 Hours" in choice:
            target = now + timedelta(hours=2)
        elif "3 Hours" in choice:
            target = now + timedelta(hours=3)
        elif "5 Hours" in choice:
            target = now + timedelta(hours=5)
        elif "Tonight" in choice:
            target = now.replace(hour=20, minute=0, second=0)
            if target < now:
                target = target + timedelta(days=1)
        else:
            target = now + timedelta(hours=2)
        return target.strftime("%Y-%m-%d %H:%M:%S")
        
    def update_expiry_preview(self, *args):
        expiry_str = self.get_expiry_datetime_str()
        self.expiry_preview_lbl.configure(
            text=f"⏳ Voting will automatically lock and finalize at: {expiry_str}"
        )
        
    def publish_and_generate_qr(self):
        title = self.title_entry.get().strip()
        meal = self.meal_type_var.get()
        date_str = self.date_entry.get().strip()
        
        if not title:
            messagebox.showwarning("Validation Error", "Please provide a poll title.")
            return
            
        if len(self.current_dishes) < 2:
            messagebox.showwarning("Validation Error", "Please add at least 2 dishes for the students to choose from.")
            return
            
        expires_at_str = self.get_expiry_datetime_str()
        
        # Save to DB
        poll_id = create_new_poll(
            title=title,
            meal_type=meal,
            date_str=date_str,
            expires_at_str=expires_at_str,
            dishes=self.current_dishes,
            notes="Please vote before expiry time for fresh kitchen prep.",
            created_by="Chef Suresh (Head Cook)"
        )
        
        # Generate QR Poster
        poster_path = QRManager.generate_qr_image(
            poll_id=poll_id,
            title=title,
            meal_type=meal,
            expires_at=expires_at_str
        )
        
        # Show animated modal
        self.show_qr_success_dialog(poll_id, title, meal, expires_at_str, poster_path)
        self.load_polls_in_results()
        
    def show_qr_success_dialog(self, poll_id, title, meal, expires_at_str, poster_path):
        dlg = ctk.CTkToplevel(self)
        dlg.title(f"QR Code Generated: {poll_id}")
        dlg.geometry("500x680")
        dlg.configure(fg_color=COLOR_BG_CARD)
        dlg.transient(self)
        dlg.grab_set()
        
        # Header
        h = ctk.CTkFrame(dlg, fg_color=COLOR_LIGHT_ACCENT, height=55, corner_radius=0)
        h.pack(fill="x")
        ctk.CTkLabel(h, text="🎉 Poll & QR Code Created!", font=FONT_TITLE, text_color=COLOR_PRIMARY_DARK).pack(pady=12)
        
        # Poster Image
        if os.path.exists(poster_path):
            img_ctk = QRManager.get_ctk_image(poster_path, size=(320, 380))
            img_lbl = ctk.CTkLabel(dlg, image=img_ctk, text="")
            img_lbl.pack(pady=15)
            
        info = ctk.CTkLabel(
            dlg, 
            text=f"Poll ID: {poll_id}\nHostel students can scan this QR or select it in their portal.\nCloses at: {expires_at_str}", 
            font=FONT_BODY,
            text_color=COLOR_TEXT_MAIN,
            justify="center"
        )
        info.pack(pady=5)
        
        # Buttons
        b_frame = ctk.CTkFrame(dlg, fg_color="transparent")
        b_frame.pack(fill="x", padx=40, pady=15)
        
        save_btn = ctk.CTkButton(
            b_frame,
            text="💾 Save QR Poster File",
            font=FONT_BODY_BOLD,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT_MAIN,
            command=lambda: self.save_qr_as(poster_path)
        )
        save_btn.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        done_btn = ctk.CTkButton(
            b_frame,
            text="Done / View Results",
            font=FONT_BODY,
            fg_color="#E2E8F0",
            hover_color="#CBD5E1",
            text_color=COLOR_TEXT_MAIN,
            command=lambda: [dlg.destroy(), self.tabview.set("📊  View Live & Past Results")]
        )
        done_btn.pack(side="right", expand=True, fill="x", padx=(10, 0))
        
    def save_qr_as(self, source_path):
        target = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            initialfile=os.path.basename(source_path)
        )
        if target:
            import shutil
            shutil.copyfile(source_path, target)
            messagebox.showinfo("Saved", f"QR Poster saved successfully to:\n{target}")

    # --- TAB 2: RESULTS ---
    def setup_results_tab(self):
        container = ctk.CTkFrame(self.tab_results, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left pane: Poll selector
        left_pane = ctk.CTkFrame(container, fg_color=COLOR_BG_CARD, border_width=1, border_color=COLOR_BORDER, corner_radius=CORNER_RADIUS_CARD, width=320)
        left_pane.pack(side="left", fill="y", padx=(0, 10))
        left_pane.pack_propagate(False)
        
        lp_header = ctk.CTkFrame(left_pane, fg_color=COLOR_LIGHT_ACCENT, height=45, corner_radius=CORNER_RADIUS_CARD)
        lp_header.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(lp_header, text="📑 Your Generated Polls", font=FONT_SUBTITLE, text_color=COLOR_PRIMARY_DARK).pack(side="left", padx=15, pady=10)
        
        # Scrollable list of polls
        self.polls_scroll = ctk.CTkScrollableFrame(left_pane, fg_color="transparent")
        self.polls_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Right pane: Details & Animated Result Bars
        self.right_pane = ctk.CTkScrollableFrame(container, fg_color=COLOR_BG_CARD, border_width=1, border_color=COLOR_BORDER, corner_radius=CORNER_RADIUS_CARD)
        self.right_pane.pack(side="right", fill="both", expand=True)
        
        self.load_polls_in_results()
        
    def load_polls_in_results(self):
        for w in self.polls_scroll.winfo_children():
            w.destroy()
            
        polls = get_all_polls()
        if not polls:
            ctk.CTkLabel(self.polls_scroll, text="No polls found.", text_color=COLOR_TEXT_MUTED).pack(pady=20)
            return
            
        for p in polls:
            card = ctk.CTkFrame(self.polls_scroll, fg_color=COLOR_BG_CARD_ALT, border_width=1, border_color=COLOR_BORDER_LIGHT, corner_radius=10)
            card.pack(fill="x", pady=5)
            
            top_line = ctk.CTkFrame(card, fg_color="transparent")
            top_line.pack(fill="x", padx=10, pady=(8, 2))
            
            # Status badge
            is_active = p['status'] == 'ACTIVE'
            badge_bg = COLOR_SUCCESS_LIGHT if is_active else COLOR_DANGER_LIGHT
            badge_fg = COLOR_SUCCESS if is_active else COLOR_DANGER
            b = ctk.CTkFrame(top_line, fg_color=badge_bg, corner_radius=8)
            b.pack(side="left")
            ctk.CTkLabel(b, text=p['status'], font=FONT_CAPTION_BOLD, text_color=badge_fg).pack(padx=6, pady=1)
            
            ctk.CTkLabel(top_line, text=p['meal_type'].upper(), font=FONT_CAPTION_BOLD, text_color=COLOR_PRIMARY_DARK).pack(side="right")
            
            ctk.CTkLabel(card, text=p['title'], font=FONT_BODY_BOLD, text_color=COLOR_TEXT_MAIN, anchor="w").pack(fill="x", padx=10, pady=2)
            ctk.CTkLabel(card, text=f"📅 {p['date']} • ID: {p['id']}", font=FONT_CAPTION, text_color=COLOR_TEXT_MUTED, anchor="w").pack(fill="x", padx=10)
            
            view_btn = ctk.CTkButton(
                card,
                text="View Voting Results →",
                font=FONT_CAPTION_BOLD,
                fg_color=COLOR_LIGHT_ACCENT,
                hover_color=COLOR_LIGHT_ACCENT_HOVER,
                text_color=COLOR_DEEP_OCEAN,
                height=26,
                command=lambda pid=p['id']: self.display_poll_results(pid)
            )
            view_btn.pack(fill="x", padx=10, pady=(6, 8))
            
        # Display first poll by default
        if polls:
            self.display_poll_results(polls[0]['id'])
            
    def display_poll_results(self, poll_id):
        for w in self.right_pane.winfo_children():
            w.destroy()
            
        res = get_poll_results(poll_id)
        if not res:
            ctk.CTkLabel(self.right_pane, text="Poll data not found.").pack(pady=40)
            return
            
        # Top banner with live timer if active
        header_card = ctk.CTkFrame(self.right_pane, fg_color=COLOR_LIGHT_ACCENT, corner_radius=CORNER_RADIUS_CARD)
        header_card.pack(fill="x", padx=20, pady=(20, 15))
        
        head_top = ctk.CTkFrame(header_card, fg_color="transparent")
        head_top.pack(fill="x", padx=15, pady=(15, 5))
        
        ctk.CTkLabel(head_top, text=res['title'], font=FONT_TITLE, text_color=COLOR_PRIMARY_DARK).pack(side="left")
        
        # If active, render live pulsating countdown timer
        if res['status'] == 'ACTIVE':
            timer = PulsingTimerBadge(
                head_top, 
                expires_at_iso=res['expires_at'], 
                on_expire_callback=lambda: self.display_poll_results(poll_id)
            )
            timer.pack(side="right")
        else:
            exp_lbl = ctk.CTkLabel(head_top, text="🔒 VOTING CLOSED (EXPIRED)", font=FONT_BODY_BOLD, text_color=COLOR_DANGER)
            exp_lbl.pack(side="right")
            
        ctk.CTkLabel(
            header_card, 
            text=f"Meal: {res['meal_type']}  •  Date: {res['date']}  •  Total Votes Received: {res['total_votes']} votes", 
            font=FONT_BODY_BOLD, 
            text_color=COLOR_DEEP_OCEAN
        ).pack(anchor="w", padx=15, pady=(0, 15))
        
        # Winner highlight card
        if res['winner'] and res['total_votes'] > 0:
            winner_card = ctk.CTkFrame(self.right_pane, fg_color="#FEF3C7", border_width=1, border_color="#F59E0B", corner_radius=CORNER_RADIUS_CARD)
            winner_card.pack(fill="x", padx=20, pady=(0, 15))
            
            w_top = ctk.CTkFrame(winner_card, fg_color="transparent")
            w_top.pack(fill="x", padx=15, pady=12)
            
            ctk.CTkLabel(w_top, text="👑 CURRENT LEADING CHOICE (CHEF ACTION)", font=FONT_HEADING, text_color="#B45309").pack(side="left")
            ctk.CTkLabel(winner_card, text=f"Winner: {res['winner']}", font=FONT_TITLE, text_color="#78350F").pack(anchor="w", padx=15, pady=(0, 12))
            
        # Dish-by-dish voting tally with animated progress bars
        tally_card = ctk.CTkFrame(self.right_pane, fg_color=COLOR_BG_CARD_ALT, border_width=1, border_color=COLOR_BORDER_LIGHT, corner_radius=CORNER_RADIUS_CARD)
        tally_card.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(tally_card, text="📊 Live Voting Results Breakdown", font=FONT_SUBTITLE, text_color=COLOR_PRIMARY_DARK).pack(anchor="w", padx=15, pady=(15, 10))
        
        for d in res['dishes']:
            item = ctk.CTkFrame(tally_card, fg_color=COLOR_BG_CARD, border_width=1, border_color=COLOR_BORDER_LIGHT, corner_radius=10)
            item.pack(fill="x", padx=15, pady=6)
            
            info_row = ctk.CTkFrame(item, fg_color="transparent")
            info_row.pack(fill="x", padx=15, pady=(10, 4))
            
            badge_bg = COLOR_SUCCESS_LIGHT if d['category'] == 'Veg' else (COLOR_DANGER_LIGHT if d['category'] == 'Non-Veg' else COLOR_SPECIAL_LIGHT)
            badge_fg = COLOR_SUCCESS if d['category'] == 'Veg' else (COLOR_DANGER if d['category'] == 'Non-Veg' else COLOR_SPECIAL)
            badge = ctk.CTkFrame(info_row, fg_color=badge_bg, corner_radius=6)
            badge.pack(side="left")
            ctk.CTkLabel(badge, text=d['category'], font=FONT_CAPTION_BOLD, text_color=badge_fg).pack(padx=6, pady=1)
            
            ctk.CTkLabel(info_row, text=d['name'], font=FONT_BODY_BOLD, text_color=COLOR_TEXT_MAIN).pack(side="left", padx=10)
            ctk.CTkLabel(info_row, text=f"{d['vote_count']} votes ({d['percentage']}%)", font=FONT_BODY_BOLD, text_color=COLOR_TEXT_BLUE).pack(side="right")
            
            # Animated progress bar
            pb = AnimatedProgressBar(item, width=400, height=12, progress_color=COLOR_PRIMARY)
            pb.pack(fill="x", padx=15, pady=(0, 10))
            # Trigger smooth easing animation
            val = (d['percentage'] / 100.0) if d['percentage'] > 0 else 0.0
            pb.animate_to(val, duration_ms=650)
            
        # Action button if active: Close poll manually
        if res['status'] == 'ACTIVE':
            close_frame = ctk.CTkFrame(self.right_pane, fg_color="transparent")
            close_frame.pack(fill="x", padx=20, pady=15)
            
            close_btn = ctk.CTkButton(
                close_frame,
                text="🔒 Finalize Kitchen Order & Close Voting Now",
                font=FONT_BODY_BOLD,
                fg_color="#FEE2E2",
                hover_color="#FECACA",
                text_color=COLOR_DANGER,
                height=40,
                corner_radius=CORNER_RADIUS_BUTTON,
                command=lambda: self.confirm_close_poll(poll_id)
            )
            close_btn.pack(side="left")
            
    def confirm_close_poll(self, poll_id):
        if messagebox.askyesno("Confirm Close", "Are you ready to close voting now?\nNo further student votes will be accepted once closed."):
            close_poll_manually(poll_id, closed_by="Chef Suresh")
            self.display_poll_results(poll_id)
            self.load_polls_in_results()
