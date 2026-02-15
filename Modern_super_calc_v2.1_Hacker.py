# -----------------------------------------------------------
#  Project: Super Multi-Calculator PRO 2026 (Hacker Perfect Edition)
#  Developed by: Ding243
#  AI Partner: Google Gemini
#  Status: V2.1 (Universal Base + Security Firewall)
#  Concept: "Secure, Smart, and Powerful"
# -----------------------------------------------------------

from datetime import datetime, timedelta
import customtkinter as ctk  
from tkinter import messagebox
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SuperCalc(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Super Multi-Calculator PRO 2026 (Hacker Perfect v2.1)")
        self.geometry("500x750")

        self.tab_control = ctk.CTkTabview(self, width=450, height=620)
        self.tab_control.pack(pady=20, padx=20)
        
        self.tab_gen = self.tab_control.add("🧮 ทั่วไป")
        self.tab_prog = self.tab_control.add("💻 นักพัฒนา")
        self.tab1 = self.tab_control.add("🏷️ ส่วนลด")
        self.tab2 = self.tab_control.add("💰 คอมมิชชั่น")
        self.tab3 = self.tab_control.add("📜 ประวัติ")

        self.setup_general_tab()
        self.setup_programmer_tab()
        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()

        self.btn_clear = ctk.CTkButton(self, text="🧹 ล้างข้อมูลหน้าจอ",
                                       fg_color="gray",
                                       border_width=2,
                                       command=self.clear_all)                         
        self.btn_clear.pack(side="bottom", pady=20)
        
        self.cleanup_old_logs(days=3)
        self.refresh_history()
        self.bind_keys() 
    
    def setup_general_tab(self):
        ctk.CTkLabel(self.tab_gen, text="เครื่องคิดเลขสามัญ", font=("Sarabun", 20, "bold")).pack(pady=10)
        
        self.ent_gen = ctk.CTkEntry(self.tab_gen, placeholder_text="พิมพ์โจทย์ (เช่น 10+2*5)", 
                                    width=350, height=50, justify="right", font=("Consolas", 24))
        self.ent_gen.pack(pady=10)

        self.btn_calc_gen = ctk.CTkButton(self.tab_gen, text="คำนวณ (=)", 
                                          width=150, height=40,
                                          fg_color="#10B981", hover_color="#059669",
                                          command=self.calc_general)
        self.btn_calc_gen.pack(pady=10)

        self.lbl_res_gen = ctk.CTkLabel(self.tab_gen, text="0", font=("Consolas", 40, "bold"), text_color="#10B981")
        self.lbl_res_gen.pack(pady=20)

        self.btn_go_hack = ctk.CTkButton(self.tab_gen, text="ไปโหมดแฮกเกอร์ ➡", 
                      fg_color="#333", border_color="#00FF00", border_width=1,
                      command=lambda: self.tab_control.set("💻 นักพัฒนา"))
        self.btn_go_hack.pack(pady=30, side="bottom")

    def setup_programmer_tab(self):
        ctk.CTkLabel(self.tab_prog, text="💻 Universal Base Converter", 
                     font=("Consolas", 20, "bold"), text_color="#00FF00").pack(pady=10)
        
        ctk.CTkLabel(self.tab_prog, text="1. ตัวเลข (Number):", font=("Sarabun", 14)).pack(pady=2)
        self.ent_prog_num = ctk.CTkEntry(self.tab_prog, placeholder_text="เช่น FF, 101, 128", 
                                     width=250, height=40, justify="center", font=("Consolas", 18))
        self.ent_prog_num.pack(pady=5)

        ctk.CTkLabel(self.tab_prog, text="2. ฐาน (Base):", font=("Sarabun", 14)).pack(pady=2)
        self.ent_prog_base = ctk.CTkEntry(self.tab_prog, placeholder_text="เช่น 10, 16, 2, 8", 
                                     width=250, height=40, justify="center", font=("Consolas", 18))
        self.ent_prog_base.pack(pady=5)
        self.ent_prog_base.insert(0, "10")

        self.btn_convert = ctk.CTkButton(self.tab_prog, text="แปลงค่าเดี๋ยวนี้ ⬇", 
                                       fg_color="#222", hover_color="#444",
                                       border_color="#00FF00", border_width=1,
                                       command=self.convert_base)
        self.btn_convert.pack(pady=15)

        res_frame = ctk.CTkFrame(self.tab_prog, fg_color="#1a1a1a")
        res_frame.pack(padx=20, pady=5, fill="x")

        self.lbl_dec = ctk.CTkLabel(res_frame, text="DEC (10): -", font=("Consolas", 16), anchor="w", text_color="#00FF00")
        self.lbl_dec.pack(fill="x", padx=15, pady=5)
        self.lbl_hex = ctk.CTkLabel(res_frame, text="HEX (16): -", font=("Consolas", 16), anchor="w", text_color="#00FF00")
        self.lbl_hex.pack(fill="x", padx=15, pady=5)
        self.lbl_oct = ctk.CTkLabel(res_frame, text="OCT (8) : -", font=("Consolas", 16), anchor="w", text_color="#00FF00")
        self.lbl_oct.pack(fill="x", padx=15, pady=5)
        self.lbl_bin = ctk.CTkLabel(res_frame, text="BIN (2) : -", font=("Consolas", 16), anchor="w", text_color="#00FF00")
        self.lbl_bin.pack(fill="x", padx=15, pady=5)

        self.btn_back_calc = ctk.CTkButton(self.tab_prog, text="⬅ กลับไปเครื่องคิดเลข", 
                      fg_color="#333", border_color="white", border_width=1,
                      command=lambda: self.tab_control.set("🧮 ทั่วไป"))
        self.btn_back_calc.pack(pady=20, side="bottom")

    def setup_tab1(self):
        ctk.CTkLabel(self.tab1, text="ราคาสินค้า:", font=("Sarabun", 16)).pack(pady=5)
        self.ent_p1 = ctk.CTkEntry(self.tab1, placeholder_text="0.00", width=200, justify="center")
        self.ent_p1.pack()
        ctk.CTkLabel(self.tab1, text="เปอร์เซ็นต์ (%):", font=("Sarabun", 16)).pack(pady=5)
        self.ent_pct1 = ctk.CTkEntry(self.tab1, placeholder_text="0", width=200, justify="center")
        self.ent_pct1.pack()
        
        btn_f = ctk.CTkFrame(self.tab1, fg_color="transparent")
        btn_f.pack(pady=15)
        self.btn_minus = ctk.CTkButton(btn_f, text="ลด (-)", width=80, fg_color="#E11D48", command=lambda: self.calc_discount("-"))
        self.btn_minus.pack(side="left", padx=5)
        self.btn_plus = ctk.CTkButton(btn_f, text="เพิ่ม (+)", width=80, fg_color="#10B981", command=lambda: self.calc_discount("+"))
        self.btn_plus.pack(side="left", padx=5)
        self.lbl_res1 = ctk.CTkLabel(self.tab1, text="...", font=("bold", 20))
        self.lbl_res1.pack(pady=10)

    def setup_tab2(self):
        ctk.CTkLabel(self.tab2, text="ยอดขาย:", font=("Sarabun", 16)).pack(pady=5)
        self.ent_s2 = ctk.CTkEntry(self.tab2, placeholder_text="0.00", width=200, justify="center")
        self.ent_s2.pack()
        ctk.CTkLabel(self.tab2, text="คอมมิชชั่น (%):", font=("Sarabun", 16)).pack(pady=5)
        self.ent_r2 = ctk.CTkEntry(self.tab2, placeholder_text="0", width=200, justify="center")
        self.ent_r2.pack()
        self.btn_com = ctk.CTkButton(self.tab2, text="คำนวณ", fg_color="#F59E0B", text_color="black", command=self.calc_commission)
        self.btn_com.pack(pady=15)
        self.lbl_res2 = ctk.CTkLabel(self.tab2, text="...", font=("bold", 20))
        self.lbl_res2.pack(pady=10)

    def setup_tab3(self):
        self.txt_history = ctk.CTkTextbox(self.tab3, width=400, height=300, font=("Courier", 12))
        self.txt_history.pack(pady=10)
        btn_f = ctk.CTkFrame(self.tab3, fg_color="transparent")
        btn_f.pack(pady=5)
        self.btn_refresh = ctk.CTkButton(btn_f, text="🔄 รีเฟรช", width=100, command=self.refresh_history)
        self.btn_refresh.pack(side="left", padx=5)
        self.btn_del_his = ctk.CTkButton(btn_f, text="🗑️ ลบ", width=100, fg_color="#7F1D1D", command=self.delete_history)
        self.btn_del_his.pack(side="left", padx=5)

    def calc_general(self):
        expr = self.ent_gen.get()
        if not expr: return
        
        allowed_chars = set("0123456789.+-*/%() abcdefABCDEFxX")
        
        if not all(char in allowed_chars or char.isspace() for char in expr):
            self.lbl_res_gen.configure(text="Security Alert! 🚫")
            messagebox.showwarning("Security", "พบตัวอักษรต้องห้าม! (อนุญาตเฉพาะเลข, สูตร, และ A-F)")
            return
        
        try:
            res = eval(expr) # nosec
            res_text = f"{int(res):,}" if res == int(res) else f"{res:,.2f}"
            self.lbl_res_gen.configure(text=res_text)
            self.save_log(f"General | {expr} = {res_text}")
        except: self.lbl_res_gen.configure(text="Error")

    def convert_base(self):
        num_str = self.ent_prog_num.get().strip()
        base_str = self.ent_prog_base.get().strip()
        if not num_str or not base_str: return
        try:
            base = int(base_str)
            val = int(num_str, base) # แปลงเลขตามฐานที่ระบุ
            
            self.lbl_dec.configure(text=f"DEC (10): {val}")
            self.lbl_hex.configure(text=f"HEX (16): {hex(val).upper().replace('0X', '')}")
            self.lbl_oct.configure(text=f"OCT (8) : {oct(val).replace('0O', '')}")
            self.lbl_bin.configure(text=f"BIN (2) : {bin(val).replace('0B', '')}")
            self.save_log(f"Base | Input:{num_str}(Base{base}) -> Dec:{val}")
        except: messagebox.showerror("Error", f"ค่า '{num_str}' ไม่ถูกต้องในฐาน {base_str}")

    def calc_discount(self, mode):
        try:
            p, pct = float(self.ent_p1.get()), float(self.ent_pct1.get() or 0)
            res = p - (p*pct/100) if mode == "-" else p + (p*pct/100)
            self.lbl_res1.configure(text=f"{res:,.2f}")
            self.save_log(f"Discount {mode} | {p} -> {res:,.2f}")
        except: pass

    def calc_commission(self):
        try:
            s, r = float(self.ent_s2.get()), float(self.ent_r2.get() or 0)
            self.lbl_res2.configure(text=f"{s*(r/100):,.2f}")
            self.save_log(f"Commission | {s} -> {s*(r/100):,.2f}")
        except: pass

    def save_log(self, text):
        with open("all_history.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {text}\n")
        self.refresh_history()

    def cleanup_old_logs(self, days=3):
        if not os.path.exists("all_history.txt"): return
        limit = datetime.now() - timedelta(days=days)
        valid = []
        with open("all_history.txt", "r", encoding="utf-8") as f:
            for line in f:
                try: 
                    if datetime.strptime(line.split(" | ")[0], "%Y-%m-%d %H:%M:%S") > limit: valid.append(line)
                except: continue
        with open("all_history.txt", "w", encoding="utf-8") as f: f.writelines(valid)

    def refresh_history(self):
        self.txt_history.configure(state="normal")
        self.txt_history.delete("1.0", "end")
        if os.path.exists("all_history.txt"):
            with open("all_history.txt", "r", encoding="utf-8") as f: self.txt_history.insert("1.0", f.read())
        self.txt_history.configure(state="disabled")

    def delete_history(self):
        if messagebox.askyesno("Confirm", "ลบประวัติ?"):
            if os.path.exists("all_history.txt"): os.remove("all_history.txt")
            self.refresh_history()

    def clear_all(self):
        for ent in [self.ent_gen, self.ent_prog_num, self.ent_prog_base, self.ent_p1, self.ent_pct1, self.ent_s2, self.ent_r2]:
            ent.delete(0, "end")
        self.ent_prog_base.insert(0, "10") # คืนค่าฐาน 10
        self.lbl_res_gen.configure(text="0")
        self.lbl_res1.configure(text="...")
        self.lbl_res2.configure(text="...")
        self.lbl_dec.configure(text="DEC (10): -")
        self.lbl_hex.configure(text="HEX (16): -")
        self.lbl_oct.configure(text="OCT (8) : -")
        self.lbl_bin.configure(text="BIN (2) : -")
        self.tab_clear_focus_logic()

    def tab_clear_focus_logic(self):
        current = self.tab_control.get()
        if current == "🧮 ทั่วไป": self.ent_gen.focus()
        elif current == "💻 นักพัฒนา": self.ent_prog_num.focus()
        elif current == "🏷️ ส่วนลด": self.ent_p1.focus()
        elif current == "💰 คอมมิชชั่น": self.ent_s2.focus()

    def bind_keys(self):
    
        self.ent_gen.bind('<Return>', lambda e: self.calc_general())

        self.ent_prog_num.bind('<Return>', lambda e: self.ent_prog_base.focus())
        self.ent_prog_base.bind('<Return>', lambda e: self.btn_convert.focus()) 
        
        self.ent_p1.bind('<Return>', lambda e: self.ent_pct1.focus())
        self.ent_pct1.bind('<Return>', lambda e: self.btn_minus.focus()) 
        
        self.ent_s2.bind('<Return>', lambda e: self.ent_r2.focus())
        self.ent_r2.bind('<Return>', lambda e: self.btn_com.focus())

        self.btn_calc_gen.bind('<Return>', lambda e: self.calc_general())
        self.btn_go_hack.bind('<Return>', lambda e: self.tab_control.set("💻 นักพัฒนา"))
        self.btn_convert.bind('<Return>', lambda e: self.convert_base())
        self.btn_back_calc.bind('<Return>', lambda e: self.tab_control.set("🧮 ทั่วไป"))
        self.btn_minus.bind('<Return>', lambda e: self.calc_discount("-"))
        self.btn_plus.bind('<Return>', lambda e: self.calc_discount("+"))
        self.btn_com.bind('<Return>', lambda e: self.calc_commission())
        self.btn_refresh.bind('<Return>', lambda e: self.refresh_history())
        self.btn_del_his.bind('<Return>', lambda e: self.delete_history())
        self.btn_clear.bind('<Return>', lambda e: self.clear_all())

        self.bind('<Control-Left>', lambda e: self.change_tab(-1))
        self.bind('<Control-Right>', lambda e: self.change_tab(1))

        self.ent_gen.bind('<Down>', lambda e: self.btn_calc_gen.focus())
        self.btn_calc_gen.bind('<Up>', lambda e: self.ent_gen.focus())
        self.btn_calc_gen.bind('<Down>', lambda e: self.btn_go_hack.focus())
        self.btn_go_hack.bind('<Up>', lambda e: self.btn_calc_gen.focus())
        self.btn_go_hack.bind('<Down>', lambda e: self.btn_clear.focus())

        self.ent_prog_num.bind('<Down>', lambda e: self.ent_prog_base.focus())
        self.ent_prog_base.bind('<Up>', lambda e: self.ent_prog_num.focus())
        self.ent_prog_base.bind('<Down>', lambda e: self.btn_convert.focus())
        self.btn_convert.bind('<Up>', lambda e: self.ent_prog_base.focus())
        self.btn_convert.bind('<Down>', lambda e: self.btn_back_calc.focus())
        self.btn_back_calc.bind('<Up>', lambda e: self.btn_convert.focus())
        self.btn_back_calc.bind('<Down>', lambda e: self.btn_clear.focus())

        self.ent_p1.bind('<Down>', lambda e: self.ent_pct1.focus())
        self.ent_pct1.bind('<Up>', lambda e: self.ent_p1.focus())
        self.ent_pct1.bind('<Down>', lambda e: self.btn_minus.focus())
        self.btn_minus.bind('<Right>', lambda e: self.btn_plus.focus())
        self.btn_minus.bind('<Up>', lambda e: self.ent_pct1.focus())
        self.btn_minus.bind('<Down>', lambda e: self.btn_clear.focus())
        self.btn_plus.bind('<Left>', lambda e: self.btn_minus.focus())
        self.btn_plus.bind('<Up>', lambda e: self.ent_pct1.focus())
        self.btn_plus.bind('<Down>', lambda e: self.btn_clear.focus())

        self.ent_s2.bind('<Down>', lambda e: self.ent_r2.focus())
        self.ent_r2.bind('<Up>', lambda e: self.ent_s2.focus())
        self.ent_r2.bind('<Down>', lambda e: self.btn_com.focus())
        self.btn_com.bind('<Up>', lambda e: self.ent_r2.focus())
        self.btn_com.bind('<Down>', lambda e: self.btn_clear.focus())

        self.btn_refresh.bind('<Right>', lambda e: self.btn_del_his.focus())
        self.btn_refresh.bind('<Down>', lambda e: self.btn_clear.focus())
        self.btn_del_his.bind('<Left>', lambda e: self.btn_refresh.focus())
        self.btn_del_his.bind('<Down>', lambda e: self.btn_clear.focus())

        self.btn_clear.bind('<Up>', lambda e: self.up_from_clear())

        all_btns = [self.btn_calc_gen, self.btn_go_hack, self.btn_convert, self.btn_back_calc,
                    self.btn_minus, self.btn_plus, self.btn_com, self.btn_refresh, 
                    self.btn_del_his, self.btn_clear]
        for btn in all_btns:
            btn.bind('<FocusIn>', lambda e, b=btn: b.configure(border_color="white", border_width=2))
            # คืนค่าสีเดิม (แต่ปุ่ม Hack ให้คืนเป็นสีเขียว)
            if btn == self.btn_go_hack:
                 btn.bind('<FocusOut>', lambda e, b=btn: b.configure(border_color="#00FF00", border_width=1))
            else:
                 btn.bind('<FocusOut>', lambda e, b=btn: b.configure(border_color=b._fg_color, border_width=0))

    def up_from_clear(self):
        current = self.tab_control.get()
        if current == "🧮 ทั่วไป": self.btn_go_hack.focus()
        elif current == "💻 นักพัฒนา": self.btn_back_calc.focus()
        elif current == "🏷️ ส่วนลด": self.btn_minus.focus()
        elif current == "💰 คอมมิชชั่น": self.btn_com.focus()
        elif current == "📜 ประวัติ": self.btn_refresh.focus()

    def change_tab(self, direction):
        tabs = ["🧮 ทั่วไป", "💻 นักพัฒนา", "🏷️ ส่วนลด", "💰 คอมมิชชั่น", "📜 ประวัติ"]
        try:
            new_idx = (tabs.index(self.tab_control.get()) + direction) % len(tabs)
            self.tab_control.set(tabs[new_idx])
            [self.ent_gen, self.ent_prog_num, self.ent_p1, self.ent_s2, self.btn_refresh][new_idx].focus()
        except: pass

if __name__ == "__main__":
    app = SuperCalc()
    app.mainloop()
