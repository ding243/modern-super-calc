from datetime import datetime, timedelta
import customtkinter as ctk  
from tkinter import messagebox
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SuperCalc(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Super Multi-Calculator PRO 2026")
        self.geometry("500x550")

        self.tab_control = ctk.CTkTabview(self, width=450, height=450)
        self.tab_control.pack(pady=20, padx=20)
        
        self.tab1 = self.tab_control.add("🏷️ ส่วนลด/ภาษี")
        self.tab2 = self.tab_control.add("💰 คอมมิชชั่น")
        self.tab3 = self.tab_control.add("📜 ประวัติ")

        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()

        self.btn_clear = ctk.CTkButton(self, text="🧹 ล้างข้อมูลหน้าจอ",
                                       fg_color="gray",
                                       border_width=2,
                                       command=self.clear_all)
                                         
        self.btn_clear.pack(side="bottom", pady=20)
        self.bind_keys()
        self.cleanup_old_logs(days=3)
        self.refresh_history()
    
    def setup_tab1(self):
        ctk.CTkLabel(self.tab1, text="ราคาสินค้าต้นทุน:", font=("Sarabun", 16)).pack(pady=10)
        self.ent_p1 = ctk.CTkEntry(self.tab1, placeholder_text="0.00", width=250, height=40, justify="center")
        self.ent_p1.pack()

        ctk.CTkLabel(self.tab1, text="เปอร์เซ็นต์ (%):", font=("Sarabun", 16)).pack(pady=10)
        self.ent_pct1 = ctk.CTkEntry(self.tab1, placeholder_text="0", width=250, height=40, justify="center")
        self.ent_pct1.pack()

        self.btn_frame = ctk.CTkFrame(self.tab1, fg_color="transparent")
        self.btn_frame.pack(pady=30)

        self.btn_minus = ctk.CTkButton(self.btn_frame, text="ลดราคา (-)", 
                                       fg_color="#E11D48",
                                       hover_color="#BE123C",
                                       border_width=2,
                                       border_color="#E11D48",
                                       command=lambda: self.calc_discount("-"))
        self.btn_minus.pack(side="left", padx=10)

        self.btn_plus = ctk.CTkButton(self.btn_frame, text="เพิ่มกำไร (+)",
                                      fg_color="#10B981",
                                      hover_color="#059669",
                                      border_width=2,
                                      border_color="#10B981",
                                      command=lambda: self.calc_discount("+"))
        self.btn_plus.pack(side="left", padx=10)

        self.lbl_res1 = ctk.CTkLabel(self.tab1, text="...", font=("Segoe UI", 22, "bold"))
        self.lbl_res1.pack(pady=20)

    def setup_tab2(self):
        ctk.CTkLabel(self.tab2, text="ยอดขายทั้งหมด:", font=("Segoe UI", 16)).pack(pady=10)
        self.ent_s2 = ctk.CTkEntry(self.tab2, placeholder_text="0.00", width=250, height=40, justify="center")
        self.ent_s2.pack()

        ctk.CTkLabel(self.tab2, text="ค่าคอมมิชชั่น (%):", font=("Segoe UI", 16)).pack(pady=10)
        self.ent_r2 = ctk.CTkEntry(self.tab2, placeholder_text="0", width=250, height=40, justify="center")
        self.ent_r2.pack()

        self.btn_com = ctk.CTkButton(self.tab2, text="คำนวณค่าคอมฯ",
                                     fg_color="#F59E0B",
                                     text_color="black",
                                     border_width=2,
                                     border_color="#F59E0B",
                                     command=self.calc_commission)
        self.btn_com.pack(pady=30)

        self.lbl_res2 = ctk.CTkLabel(self.tab2, text="...", font=("Roboto", 22, "bold"))
        self.lbl_res2.pack(pady=20)

    def setup_tab3(self):
        self.txt_history = ctk.CTkTextbox(self.tab3, width=500, height=350, font=("Courier", 12))
        self.txt_history.pack(pady=10)
    
        btn_f = ctk.CTkFrame(self.tab3, fg_color="transparent")
        btn_f.pack(pady=10)

        self.btn_refresh = ctk.CTkButton(btn_f, text="🔄 รีเฟรช", width=120, 
                                          command=self.refresh_history)
        self.btn_refresh.pack(side="left", padx=10)

        self.btn_del_his = ctk.CTkButton(btn_f, text="🗑️ ลบประวัติ", width=120, 
                                          fg_color="#7F1D1D", hover_color="#B91C1C",
                                          command=self.delete_history)
        self.btn_del_his.pack(side="left", padx=10)

    def calc_discount(self, mode):
        if not self.ent_p1.get(): return self.ent_pct1.focus()
        try:
            p = float(self.ent_p1.get())
            pct = float(self.ent_pct1.get() or 0)
            res = p - (p * pct / 100) if mode == "-" else p + (p * pct / 100)
            self.lbl_res1.configure(text=f"ผลลัพธ์: {res:,.2f} บาท")
            self.save_log(f"ส่วนลด [{mode}] | ราคา:{p:,.2f} | %:{pct} | ผล:{res:,.2f}")

        except: messagebox.showerror("ผิดพลาด", "กรอกตัวเลขเท่านั้นจ้า")

    def calc_commission(self):
        if not self.ent_s2.get(): return self.ent_r2.focus()
        try:
            s = float(self.ent_s2.get())
            r = float(self.ent_r2.get() or 0)
            com = s * (r / 100)
            self.lbl_res2.configure(text=f"ได้เงิน: {com:,.2f} บาท")
            self.save_log(f"คอมมิชชั่น | ยอดขาย:{s:,.2f} | %:{r} | รับ:{com:,.2f}")
        except: messagebox.showerror("ผิดพลาด", "กรอกตัวเลขเท่านั้นจ้า")

    def save_log(self, text):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("all_history.txt", "a", encoding="utf-8") as f:
            f.write(f"{now} | {text}\n")
        self.refresh_history()

    def cleanup_old_logs(self, days=3):
        if not os.path.exists("all_history.txt"): return
        limit_date = datetime.now() - timedelta(days=days)
        valid_logs = []
        
        with open("all_history.txt", "r", encoding="utf-8") as f:
            for line in f:
                try:
                    log_date_str = line.split(" | ")[0]
                    log_date = datetime.strptime(log_date_str, "%Y-%m-%d %H:%M:%S")
                    if log_date > limit_date:
                        valid_logs.append(line)
                except:
                    continue

        with open("all_history.txt", "w", encoding="utf-8") as f:
            f.writelines(valid_logs)

    def refresh_history(self):
        self.txt_history.configure(state="normal")
        self.txt_history.delete("1.0", "end")
        if os.path.exists("all_history.txt"):
            with open("all_history.txt", "r", encoding="utf-8") as f:
                self.txt_history.insert("1.0", f.read())
        self.txt_history.configure(state="disabled")

    def delete_history(self):
        if messagebox.askyesno("ยืนยัน", "ลบประวัติทั้งหมด?"):
            if os.path.exists("all_history.txt"):
                os.remove("all_history.txt")
            self.txt_history.configure(state="normal")
            self.txt_history.delete("1.0", "end")
            self.txt_history.configure(state="disabled")

    def clear_all(self):
        self.ent_p1.delete(0, "end"); self.ent_pct1.delete(0, "end")
        self.ent_s2.delete(0, "end"); self.ent_r2.delete(0, "end")
        self.ent_p1.focus()
        
        self.lbl_res1.configure(text="...",)
        self.lbl_res2.configure(text="...",)
    
    def bind_keys(self):
        for btn, color in [(self.btn_minus, "#E11D48"), (self.btn_plus, "#10B981"), 
                           (self.btn_com, "#F59E0B"), (self.btn_clear, "gray"),
                           (self.btn_refresh, "gray"), (self.btn_del_his, "#7F1D1D")]:
            btn.bind("<FocusIn>", lambda e, b=btn: b.configure(border_color="white"))
            btn.bind("<FocusOut>", lambda e, b=btn, c=color: b.configure(border_color=c))

        self.bind('<Control-Left>', lambda e: self.change_tab(-1))
        self.bind('<Control-Right>', lambda e: self.change_tab(1))

        self.ent_p1.bind('<Return>', lambda e: self.ent_pct1.focus())
        self.ent_pct1.bind('<Return>', lambda e: self.btn_minus.focus())
        self.btn_minus.bind('<Return>', lambda e: self.calc_discount("-"))
        self.btn_plus.bind('<Return>', lambda e: self.calc_discount("+"))
        
        self.ent_s2.bind('<Return>', lambda e: self.ent_r2.focus())
        self.ent_r2.bind('<Return>', lambda e: self.btn_com.focus())
        self.btn_com.bind('<Return>', lambda e: self.calc_commission())
        self.btn_clear.bind('<Return>', lambda e: self.clear_all())

        self.btn_minus.bind('<Right>', lambda e: self.btn_plus.focus())
        self.btn_plus.bind('<Left>', lambda e: self.btn_minus.focus())

        self.btn_refresh.bind('<Right>', lambda e: self.btn_del_his.focus())
        self.btn_del_his.bind('<Left>', lambda e: self.btn_refresh.focus())
        self.btn_refresh.bind('<Return>', lambda e: self.refresh_history())
        self.btn_del_his.bind('<Return>', lambda e: self.delete_history())

        self.btn_minus.bind('<Down>', lambda e: self.btn_clear.focus())
        self.btn_plus.bind('<Down>', lambda e: self.btn_clear.focus())
        self.btn_com.bind('<Down>', lambda e: self.btn_clear.focus())
        self.btn_del_his.bind('<Down>', lambda e: self.btn_clear.focus())
        self.btn_clear.bind('<Up>', lambda e: self.btn_minus.focus())

    def change_tab(self, direction):
        tabs = ["🏷️ ส่วนลด/ภาษี", "💰 คอมมิชชั่น", "📜 ประวัติ"]
        current = self.tab_control.get()
        idx = tabs.index(current)
        new_idx = (idx + direction) % len(tabs)
        self.tab_control.set(tabs[new_idx])

if __name__ == "__main__":
    app = SuperCalc()
    app.mainloop()