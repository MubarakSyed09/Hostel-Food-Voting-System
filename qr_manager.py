"""
QR Code Manager: Generation, Styled Poster Creation, and OpenCV Live Camera Scanner
"""

import os
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageTk
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from theme import *

QR_STORAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qr_codes")
os.makedirs(QR_STORAGE_DIR, exist_ok=True)

class QRManager:
    
    @staticmethod
    def generate_qr_image(poll_id, title, meal_type, expires_at):
        """Generates a high-res QR code image with custom baby blue border poster"""
        # 1. Base QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2,
        )
        # Payload format recognized by scanner
        payload = f"HOSTEL_VOTE:{poll_id}"
        qr.add_data(payload)
        qr.make(fit=True)
        
        # Color: Sky Blue dark modules on white background
        qr_img = qr.make_image(fill_color="#0369A1", back_color="#FFFFFF").convert("RGBA")
        
        # 2. Build full poster (420 x 500)
        poster = Image.new("RGBA", (440, 520), "#FFFFFF")
        draw = ImageDraw.Draw(poster)
        
        # Outer soft baby blue border
        draw.rounded_rectangle([(8, 8), (432, 512)], radius=24, outline="#38BDF8", width=4)
        
        # Header banner (Baby Blue)
        draw.rounded_rectangle([(16, 16), (424, 95)], radius=16, fill="#E0F2FE")
        
        # Try loading system font, fallback to default
        try:
            font_title = ImageFont.truetype("arial.ttf", 20)
            font_meal = ImageFont.truetype("arialbd.ttf", 16)
            font_sub = ImageFont.truetype("arial.ttf", 13)
            font_code = ImageFont.truetype("courbd.ttf", 15)
        except:
            font_title = font_meal = font_sub = font_code = ImageFont.load_default()
            
        # Draw text
        draw.text((220, 36), "HOSTEL MESS DAILY VOTING", font=font_title, fill="#0369A1", anchor="mm")
        draw.text((220, 68), f"Meal: {meal_type.upper()}  •  {title[:26]}", font=font_meal, fill="#0F172A", anchor="mm")
        
        # Paste QR in center
        qr_w, qr_h = qr_img.size
        # Resize QR nicely to 260x260
        qr_resized = qr_img.resize((260, 260), Image.Resampling.LANCZOS)
        poster.paste(qr_resized, (90, 115), qr_resized)
        
        # Poll ID badge
        draw.rounded_rectangle([(70, 390), (370, 425)], radius=10, fill="#F0F8FF", outline="#BAE6FD", width=1)
        draw.text((220, 407), f"CODE: {poll_id}", font=font_code, fill="#0284C7", anchor="mm")
        
        # Expiry notice
        draw.text((220, 455), f"⏳ Voting closes at: {expires_at}", font=font_sub, fill="#EF4444", anchor="mm")
        draw.text((220, 480), "Scan with Student Portal to cast your vote!", font=font_sub, fill="#64748B", anchor="mm")
        
        # Save poster
        file_path = os.path.join(QR_STORAGE_DIR, f"{poll_id}.png")
        poster.convert("RGB").save(file_path, "PNG")
        return file_path

    @staticmethod
    def get_ctk_image(image_path, size=(240, 240)):
        if os.path.exists(image_path):
            img = Image.open(image_path)
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)
        return None

class CameraQRScannerDialog:
    """Live OpenCV camera QR scanner with animated scan laser overlay and manual image fallback"""
    
    def __init__(self, parent, on_detected_callback):
        self.parent = parent
        self.on_detected = on_detected_callback
        self.cap = None
        self.detector = cv2.QRCodeDetector()
        self.is_scanning = True
        self.laser_pos = 0
        self.laser_dir = 1
        
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Scan Hostel Food QR Code")
        self.dialog.geometry("540x580")
        self.dialog.configure(fg_color=COLOR_BG_CARD)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Header
        header = ctk.CTkFrame(self.dialog, fg_color=COLOR_LIGHT_ACCENT, corner_radius=0, height=60)
        header.pack(fill="x", side="top")
        
        title = ctk.CTkLabel(
            header, 
            text="📷 Scan Food Poll QR Code", 
            font=FONT_TITLE, 
            text_color=COLOR_PRIMARY_DARK
        )
        title.pack(pady=15)
        
        # Instructions
        self.status_lbl = ctk.CTkLabel(
            self.dialog,
            text="Hold the Cook's QR code in front of your camera",
            font=FONT_BODY,
            text_color=COLOR_TEXT_MUTED
        )
        self.status_lbl.pack(pady=(10, 5))
        
        # Video Canvas
        self.canvas_w = 460
        self.canvas_h = 340
        self.canvas = tk.Canvas(self.dialog, width=self.canvas_w, height=self.canvas_h, bg="#0F172A", highlightthickness=2, highlightbackground=COLOR_PRIMARY)
        self.canvas.pack(pady=5)
        
        # Fallback & control buttons
        btn_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        btn_frame.pack(fill="x", padx=40, pady=(15, 10))
        
        self.upload_btn = ctk.CTkButton(
            btn_frame,
            text="📁 Select QR Image File",
            font=FONT_BODY_BOLD,
            fg_color=COLOR_LIGHT_ACCENT,
            hover_color=COLOR_LIGHT_ACCENT_HOVER,
            text_color=COLOR_DEEP_OCEAN,
            corner_radius=CORNER_RADIUS_BUTTON,
            command=self.scan_from_file
        )
        self.upload_btn.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        self.cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            font=FONT_BODY,
            fg_color="#F1F5F9",
            hover_color="#E2E8F0",
            text_color=COLOR_TEXT_MAIN,
            corner_radius=CORNER_RADIUS_BUTTON,
            command=self.close
        )
        self.cancel_btn.pack(side="right", padx=(10, 0))
        
        self.dialog.protocol("WM_DELETE_WINDOW", self.close)
        
        # Start camera
        self.start_camera()
        
    def start_camera(self):
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                self.show_no_camera_fallback()
                return
            self.update_video()
        except Exception as e:
            self.show_no_camera_fallback()
            
    def show_no_camera_fallback(self):
        self.status_lbl.configure(
            text="⚠️ Camera unavailable. You can upload the QR code image or select from active polls below!",
            text_color=COLOR_WARNING
        )
        self.canvas.create_text(
            self.canvas_w // 2, 
            self.canvas_h // 2, 
            text="Camera feed not detected.\nPlease click 'Select QR Image File' below.",
            fill="#94A3B8",
            font=("Segoe UI", 12),
            justify="center"
        )
        
    def update_video(self):
        if not self.is_scanning or not self.cap or not self.cap.isOpened():
            return
            
        ret, frame = self.cap.read()
        if ret:
            # Flip horizontally for natural mirror feel
            frame = cv2.flip(frame, 1)
            
            # Detect QR code
            data, bbox, _ = self.detector.detectAndDecode(frame)
            
            if bbox is not None and len(bbox) > 0:
                # Draw baby blue / emerald bounding box around detected QR
                pts = bbox[0].astype(int)
                for i in range(len(pts)):
                    pt1 = tuple(pts[i])
                    pt2 = tuple(pts[(i + 1) % len(pts)])
                    cv2.line(frame, pt1, pt2, (56, 189, 248), 3)
                    
            # Resize frame to fit canvas
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(frame_rgb)
            img_resized = img_pil.resize((self.canvas_w, self.canvas_h), Image.Resampling.BILINEAR)
            
            self.tk_photo = ImageTk.PhotoImage(image=img_resized)
            self.canvas.create_image(0, 0, image=self.tk_photo, anchor="nw")
            
            # Draw animated laser line
            self.laser_pos += 6 * self.laser_dir
            if self.laser_pos > self.canvas_h - 10:
                self.laser_dir = -1
            elif self.laser_pos < 10:
                self.laser_dir = 1
                
            self.canvas.create_line(
                30, self.laser_pos, self.canvas_w - 30, self.laser_pos, 
                fill="#38BDF8", width=2
            )
            
            # If QR detected
            if data and data.strip():
                self.process_qr_data(data)
                return
                
        self.dialog.after(30, self.update_video)
        
    def process_qr_data(self, data):
        poll_id = data.replace("HOSTEL_VOTE:", "").strip()
        self.status_lbl.configure(text=f"✅ QR Code Scanned: {poll_id}", text_color=COLOR_SUCCESS)
        self.close()
        if self.on_detected:
            self.on_detected(poll_id)
            
    def scan_from_file(self):
        file_path = filedialog.askopenfilename(
            title="Select QR Code Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            try:
                img = cv2.imread(file_path)
                data, _, _ = self.detector.detectAndDecode(img)
                if data and data.strip():
                    self.process_qr_data(data)
                else:
                    # Fallback check filename if it has poll ID
                    base = os.path.basename(file_path)
                    if "POLL-" in base:
                        poll_id = base.replace(".png", "").replace(".jpg", "")
                        self.process_qr_data(poll_id)
                    else:
                        messagebox.showwarning("Scan Result", "No readable QR code found in this image.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read image: {e}")
                
    def close(self):
        self.is_scanning = False
        if self.cap:
            try:
                self.cap.release()
            except:
                pass
        try:
            self.dialog.destroy()
        except:
            pass
