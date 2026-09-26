"""
Login / Role Selector View
Beautiful baby blue theme with animated role selection cards.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import simpledialog, messagebox
from theme import *

class LoginView(ctk.CTkFrame):
    
    def __init__(self, parent, on_role_selected):
        super().__init__(parent, fg_color=COLOR_BG_MAIN)
        self.parent = parent
        self.on_role_selected = on_role_selected
        
        self.setup_ui()
        
    def setup_ui(self):
        # Center container
        center_box = ctk.CTkFrame(
            self,
            fg_color="transparent",
            width=850
        )
        center_box.place(relx=0.5, rely=0.5, anchor="center")
        
        # Header Badge
        badge = ctk.CTkFrame(
            center_box,
            fg_color=COLOR_LIGHT_ACCENT,
            corner_radius=CORNER_RADIUS_PILL,
            border_width=1,
            border_color=COLOR_BORDER
        )
        badge.pack(pady=(0, 10))
        
        badge_lbl = ctk.CTkLabel(
            badge,
            text="✨ NEXT-GEN HOSTEL DINING MANAGEMENT ✨",
            font=FONT_CAPTION_BOLD,
            text_color=COLOR_DEEP_OCEAN
        )
        badge_lbl.pack(padx=16, pady=4)
        
        # Main Title
        title = ctk.CTkLabel(
            center_box,
            text="Hostel Mess Smart Voting System",
            font=FONT_HERO,
            text_color=COLOR_PRIMARY_DARK
        )
        title.pack(pady=(0, 6))
        
        subtitle = ctk.CTkLabel(
            center_box,
            text="Real-time menu decision making with QR-based polling & automated expiry",
            font=FONT_BODY,
            text_color=COLOR_TEXT_MUTED
        )
        subtitle.pack(pady=(0, 35))
        
        # Role Cards Container (3 Cards side by side)
        cards_row = ctk.CTkFrame(center_box, fg_color="transparent")
        cards_row.pack(fill="x", padx=10)
        
        # 1. COOK CARD
        self.create_role_card(
            parent=cards_row,
            icon="👨‍🍳",
            role_name="Hostel Cook",
            badge_text="KITCHEN ACCESS",
            badge_color=COLOR_SPECIAL_LIGHT,
            badge_text_color=COLOR_SPECIAL,
            description="Add limited daily dishes,\nset poll expiry time,\nand generate QR for students.",
            button_text="Enter Cook Portal →",
            button_color=COLOR_PRIMARY,
            command=lambda: self.on_role_selected("cook")
        )
        
        # 2. STUDENT CARD (Highlighted / Featured)
        self.create_role_card(
            parent=cards_row,
            icon="🎓",
            role_name="Hostel Student",
            badge_text="POLLING ACCESS",
            badge_color=COLOR_SUCCESS_LIGHT,
            badge_text_color=COLOR_SUCCESS,
            description="Scan QR code with camera,\nview available dishes,\nand cast your food vote.",
            button_text="Scan & Vote Now →",
            button_color=COLOR_PRIMARY_DARK,
            button_text_color="#FFFFFF",
            command=lambda: self.on_role_selected("student"),
            is_featured=True
        )
        
        # 3. ADMIN CARD
        self.create_role_card(
            parent=cards_row,
            icon="🛡️",
            role_name="Mess Admin",
            badge_text="FULL SYSTEM ACCESS",
            badge_color=COLOR_WARNING_LIGHT,
            badge_text_color=COLOR_WARNING,
            description="View all generated QRs,\ndaily dishes log, who polled\nvs who didn't poll, & analytics.",
            button_text="Admin Login (PIN) →",
            button_color=COLOR_LIGHT_ACCENT,
            button_hover=COLOR_LIGHT_ACCENT_HOVER,
            button_text_color=COLOR_DEEP_OCEAN,
            command=self.prompt_admin_login
        )
        
        # Footer
        footer = ctk.CTkLabel(
            center_box,
            text="Hostel Administration & Food Services • All rights reserved",
            font=FONT_CAPTION,
            text_color=COLOR_TEXT_LIGHT
        )
        footer.pack(pady=(35, 0))
        
    def create_role_card(self, parent, icon, role_name, badge_text, badge_color, badge_text_color, description, button_text, button_color, command, button_hover=None, button_text_color=COLOR_TEXT_MAIN, is_featured=False):
        border_color = COLOR_PRIMARY if is_featured else COLOR_BORDER
        border_w = 2 if is_featured else 1
        
        card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_BG_CARD,
            border_width=border_w,
            border_color=border_color,
            corner_radius=CORNER_RADIUS_CARD,
            width=260,
            height=340
        )
        card.pack(side="left", padx=12, fill="both", expand=True)
        card.pack_propagate(False)
        
        # Hover effect on card
        def on_enter(e):
            card.configure(border_color=COLOR_PRIMARY_HOVER, border_width=2)
        def on_leave(e):
            card.configure(border_color=border_color, border_width=border_w)
            
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        # Icon
        icon_lbl = ctk.CTkLabel(card, text=icon, font=("Segoe UI", 42))
        icon_lbl.pack(pady=(20, 4))
        
        # Badge
        badge = ctk.CTkFrame(card, fg_color=badge_color, corner_radius=CORNER_RADIUS_PILL)
        badge.pack(pady=(0, 8))
        badge_l = ctk.CTkLabel(badge, text=badge_text, font=FONT_CAPTION_BOLD, text_color=badge_text_color)
        badge_l.pack(padx=10, pady=2)
        
        # Role Name
        title_lbl = ctk.CTkLabel(card, text=role_name, font=FONT_SUBTITLE, text_color=COLOR_PRIMARY_DARK)
        title_lbl.pack(pady=(2, 6))
        
        # Description
        desc_lbl = ctk.CTkLabel(card, text=description, font=FONT_BODY, text_color=COLOR_TEXT_MUTED, justify="center")
        desc_lbl.pack(pady=(0, 20), padx=10)
        
        # Button
        btn = ctk.CTkButton(
            card,
            text=button_text,
            font=FONT_BODY_BOLD,
            fg_color=button_color,
            hover_color=button_hover or COLOR_PRIMARY_HOVER,
            text_color=button_text_color,
            corner_radius=CORNER_RADIUS_BUTTON,
            height=38,
            command=command
        )
        btn.pack(side="bottom", fill="x", padx=20, pady=20)
        
    def prompt_admin_login(self):
        # Security gate for admin
        dialog = ctk.CTkInputDialog(
            text="Enter Admin PIN to access master dashboard:\n(Default PIN: admin123)",
            title="Admin Verification"
        )
        pin = dialog.get_input()
        if pin == "admin123":
            self.on_role_selected("admin")
        elif pin is not None:
            messagebox.showerror("Access Denied", "Incorrect Admin PIN! Only authorized administration has access.")
