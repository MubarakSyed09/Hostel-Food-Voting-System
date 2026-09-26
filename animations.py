"""
Animation and Transition Engine for Hostel Food Voting Application
Provides smooth frame slide transitions, animated result bars, pulsing timer badges,
and celebration confetti particle simulations.
"""

import math
import random
import tkinter as tk
import customtkinter as ctk
from theme import *

def ease_out_quad(t):
    """Quadratic easing out: decelerating to zero velocity"""
    return 1 - (1 - t) * (1 - t)

def ease_in_out_cubic(t):
    """Cubic easing in/out: acceleration until halfway, then deceleration"""
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - math.pow(-2 * t + 2, 3) / 2

class FrameTransitionManager:
    """Manages smooth sliding page transitions between views"""
    
    @staticmethod
    def slide_in(widget, direction="right", duration_ms=250, steps=15, callback=None):
        widget.lift()
        start_x = 1.0 if direction == "right" else -1.0
        target_x = 0.0
        
        current_step = 0
        interval = max(10, duration_ms // steps)
        
        def animate_step():
            nonlocal current_step
            current_step += 1
            progress = current_step / steps
            eased = ease_out_quad(progress)
            
            new_x = start_x + (target_x - start_x) * eased
            widget.place(relx=new_x, rely=0.0, relwidth=1.0, relheight=1.0)
            
            if current_step < steps:
                widget.after(interval, animate_step)
            else:
                widget.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
                if callback:
                    callback()
                    
        animate_step()

class AnimatedProgressBar:
    """A progress bar that smoothly animates from 0% to the target value with percentage counter"""
    
    def __init__(self, parent, width=300, height=12, fg_color=COLOR_BORDER_LIGHT, progress_color=COLOR_PRIMARY):
        self.container = ctk.CTkFrame(parent, fg_color="transparent")
        
        self.bar = ctk.CTkProgressBar(
            self.container, 
            width=width, 
            height=height, 
            fg_color=fg_color, 
            progress_color=progress_color,
            corner_radius=height // 2
        )
        self.bar.set(0.0)
        self.bar.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.label = ctk.CTkLabel(
            self.container, 
            text="0%", 
            font=FONT_CAPTION_BOLD, 
            text_color=COLOR_TEXT_BLUE,
            width=45
        )
        self.label.pack(side="right")
        
    def pack(self, **kwargs):
        self.container.pack(**kwargs)
        
    def animate_to(self, target_value, duration_ms=600, steps=25):
        """target_value between 0.0 and 1.0"""
        current_step = 0
        interval = max(15, duration_ms // steps)
        
        def step():
            nonlocal current_step
            current_step += 1
            t = current_step / steps
            eased = ease_out_quad(t)
            current_val = target_value * eased
            
            self.bar.set(current_val)
            pct = int(current_val * 100)
            self.label.configure(text=f"{pct}%")
            
            if current_step < steps:
                self.container.after(interval, step)
            else:
                self.bar.set(target_value)
                self.label.configure(text=f"{int(target_value * 100)}%")
                
        step()

class ConfettiCelebrationCanvas:
    """Full overlay celebratory confetti animation triggered upon successful voting"""
    
    COLORS = ["#38BDF8", "#0284C7", "#7DD3FC", "#34D399", "#FBBF24", "#F472B6", "#A78BFA", "#FFFFFF"]
    
    def __init__(self, parent, duration_ms=2500):
        self.parent = parent
        self.canvas = tk.Canvas(parent, highlightthickness=0, bg=COLOR_BG_CARD)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.canvas.lift()
        
        # Center card container
        self.center_card = ctk.CTkFrame(
            self.canvas,
            fg_color=COLOR_BG_CARD,
            border_width=2,
            border_color=COLOR_BORDER,
            corner_radius=20,
            width=420,
            height=320
        )
        self.center_card.place(relx=0.5, rely=0.5, anchor="center")
        self.center_card.pack_propagate(False)
        
        # Success Icon & Message inside center card
        self.icon_lbl = ctk.CTkLabel(
            self.center_card,
            text="✨ 🗳️ ✨",
            font=("Segoe UI", 36)
        )
        self.icon_lbl.pack(pady=(25, 5))
        
        self.title_lbl = ctk.CTkLabel(
            self.center_card,
            text="Vote Successfully Cast!",
            font=FONT_TITLE,
            text_color=COLOR_PRIMARY_DARK
        )
        self.title_lbl.pack(pady=4)
        
        self.msg_lbl = ctk.CTkLabel(
            self.center_card,
            text="Your food preference has been registered.\nThe mess kitchen appreciates your voice!",
            font=FONT_BODY,
            text_color=COLOR_TEXT_MUTED,
            justify="center"
        )
        self.msg_lbl.pack(pady=8)
        
        self.close_btn = ctk.CTkButton(
            self.center_card,
            text="Awesome, Done!",
            font=FONT_BODY_BOLD,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT_MAIN,
            corner_radius=CORNER_RADIUS_BUTTON,
            height=40,
            command=self.close
        )
        self.close_btn.pack(pady=(15, 10))
        
        # Particles
        self.particles = []
        width = parent.winfo_width() or 800
        height = parent.winfo_height() or 600
        
        for _ in range(75):
            self.particles.append({
                'x': random.uniform(50, width - 50),
                'y': random.uniform(-100, 50),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(3, 7),
                'size': random.uniform(5, 11),
                'color': random.choice(self.COLORS),
                'shape': random.choice(['rect', 'oval']),
                'rot': random.uniform(0, 360),
                'rot_speed': random.uniform(-8, 8)
            })
            
        self.is_running = True
        self.animate()
        self.parent.after(duration_ms, self.fade_out)
        
    def animate(self):
        if not self.is_running:
            return
            
        self.canvas.delete("confetti")
        h = self.parent.winfo_height() or 600
        w = self.parent.winfo_width() or 800
        
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['rot'] += p['rot_speed']
            
            # Wrap around top if falls off
            if p['y'] > h:
                p['y'] = random.uniform(-40, -10)
                p['x'] = random.uniform(20, w - 20)
                
            x, y, s = p['x'], p['y'], p['size']
            if p['shape'] == 'rect':
                self.canvas.create_rectangle(x, y, x + s, y + s * 1.5, fill=p['color'], outline="", tags="confetti")
            else:
                self.canvas.create_oval(x, y, x + s, y + s, fill=p['color'], outline="", tags="confetti")
                
        self.center_card.lift()
        self.parent.after(25, self.animate)
        
    def fade_out(self):
        # Auto close or keep until user clicks
        pass
        
    def close(self):
        self.is_running = False
        try:
            self.canvas.destroy()
        except:
            pass

class PulsingTimerBadge:
    """Animated live countdown pill with pulsating indicator dot"""
    
    def __init__(self, parent, expires_at_iso, on_expire_callback=None):
        self.parent = parent
        self.expires_at_iso = expires_at_iso
        self.on_expire = on_expire_callback
        self.is_active = True
        self.pulse_phase = 0
        
        self.frame = ctk.CTkFrame(
            parent, 
            fg_color=COLOR_LIGHT_ACCENT, 
            border_width=1, 
            border_color=COLOR_BORDER,
            corner_radius=CORNER_RADIUS_PILL
        )
        
        # Pulse indicator circle
        self.dot_canvas = tk.Canvas(self.frame, width=16, height=16, bg=COLOR_LIGHT_ACCENT, highlightthickness=0)
        self.dot_canvas.pack(side="left", padx=(10, 4), pady=4)
        
        self.timer_label = ctk.CTkLabel(
            self.frame, 
            text="⏳ Calculating...", 
            font=FONT_HEADING, 
            text_color=COLOR_DEEP_OCEAN
        )
        self.timer_label.pack(side="left", padx=(2, 12), pady=4)
        
        self.update_pulse()
        self.update_countdown()
        
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
        
    def update_pulse(self):
        if not self.is_active:
            return
        self.pulse_phase = (self.pulse_phase + 1) % 2
        color = COLOR_PRIMARY if self.pulse_phase == 0 else COLOR_PRIMARY_DARK
        self.dot_canvas.delete("dot")
        self.dot_canvas.create_oval(3, 3, 13, 13, fill=color, outline="")
        self.frame.after(600, self.update_pulse)
        
    def update_countdown(self):
        if not self.is_active:
            return
        try:
            from datetime import datetime
            expire_dt = datetime.strptime(self.expires_at_iso, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            diff = expire_dt - now
            
            if diff.total_seconds() <= 0:
                self.timer_label.configure(text="🔒 Poll Closed", text_color=COLOR_DANGER)
                self.dot_canvas.delete("dot")
                self.dot_canvas.create_oval(3, 3, 13, 13, fill=COLOR_DANGER, outline="")
                self.is_active = False
                if self.on_expire:
                    self.on_expire()
                return
                
            total_sec = int(diff.total_seconds())
            hours = total_sec // 3600
            mins = (total_sec % 3600) // 60
            secs = total_sec % 60
            
            if hours > 0:
                time_str = f"Closes in: {hours:02d}h {mins:02d}m {secs:02d}s"
            else:
                time_str = f"Closes in: {mins:02d}m {secs:02d}s"
                
            # If under 15 minutes, turn warning amber
            if total_sec < 900:
                self.frame.configure(fg_color=COLOR_WARNING_LIGHT, border_color=COLOR_WARNING)
                self.timer_label.configure(text=f"⚠️ {time_str}", text_color=COLOR_WARNING)
            else:
                self.timer_label.configure(text=time_str)
                
        except Exception as e:
            self.timer_label.configure(text="Closes soon")
            
        self.frame.after(1000, self.update_countdown)
        
    def destroy(self):
        self.is_active = False
        try:
            self.frame.destroy()
        except:
            pass
