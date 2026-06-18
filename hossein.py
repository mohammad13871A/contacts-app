from tkinter import filedialog,messagebox
import customtkinter
import os 
import sqlite3
import shutil
from PIL import Image

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

if not os.path.exists("image"):
    os.makedirs("image")
coon=sqlite3.connect("hossein.db")
cursor=coon.cursor()
cursor.execute("""CREATE TABLE if not exists user(
    id integer primary key autoincrement,
    name text,
    phone text unique,
    image_path text
    )""")
coon.commit()

app=customtkinter.CTk()
app.title("فهرست مخاطبین")
app.geometry("950x650")
app.resizable(False,False)

sidebar=customtkinter.CTkFrame(app,width=200,corner_radius=0,fg_color="#1a1a2e")
sidebar.pack(fill="y",side="left")
sidebar.pack_propagate(False)
customtkinter.CTkLabel(sidebar,text="\nمخاطبین",font=("Tahoma", 18, "bold")).pack(pady=(40,30))

customtkinter.CTkFrame(sidebar, height=1, fg_color="#333355").pack(fill="x", padx=20, pady=5)

def sidebar_btn(text,icon,cmd):
    customtkinter.CTkButton(sidebar,text=f"{icon} {text}",font=("tahoma",13),anchor="w",width=160,height=0,fg_color="transparent", hover_color="#2a2a4a", text_color="#c0c0d0", command=cmd).pack(pady=5, padx=20)
content = customtkinter.CTkFrame(app, corner_radius=0, fg_color="#12121f")
content.pack(side="right", fill="both", expand=True)

name_entry = phone_entry = photo_text = None
photo_path = ""

def clear():
    for w in content.winfo_children():
        w.destroy()
        
def make_header(title, subtitle=""):
    hdr = customtkinter.CTkFrame(content, fg_color="#1e1e35", corner_radius=0, height=80)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)
    customtkinter.CTkLabel(hdr, text=title, font=("Tahoma", 22, "bold"), text_color="#ffffff").pack(anchor="w", padx=30, pady=(18, 0))
    if subtitle:
        customtkinter.CTkLabel(hdr, text=subtitle, font=("Tahoma", 11), text_color="#8888aa").pack(anchor="w", padx=30)
def home():
    clear()
    make_header("🏠 خانه ","به مدیریت مخاطب خوش آمدی")
    center = customtkinter.CTkFrame(content, fg_color="transparent")
    center.pack(expand=True)
    
    cursor.execute("SELECT count (*) from user")
    count=cursor.fetchone()[0]
    stat=customtkinter.CTkFrame(center,width=280,height=110,corner_radius=15,fg_color="#1e1e35")
    stat.pack(pady=20)
    stat.pack_propagate(False)
    customtkinter.CTkLabel(stat,text="👥  کل مخاطبین",font=("tahoma",13)).pack(pady=(15, 4))


    customtkinter.CTkLabel(stat, text=str(count), font=("Tahoma", 36, "bold"), text_color="#4da6ff").pack()
    
    btn_frame = customtkinter.CTkFrame(center, fg_color="transparent")
    btn_frame.pack(pady=10)
    customtkinter.CTkButton(btn_frame, text="➕  افزودن مخاطب", font=("Tahoma", 14, "bold"),
                            width=200, height=48, corner_radius=12,command=add_user,
                            fg_color="#2563eb", hover_color="#1d4ed8",).pack(pady=8)
    customtkinter.CTkButton(btn_frame, text="📋  مشاهده مخاطبین", font=("Tahoma", 14, "bold"),
                            width=200, height=48, corner_radius=12,
                            fg_color="#059669", hover_color="#047857",command=show_user).pack(pady=8)
def image_chose():
    global photo_path
    try:
        p=filedialog.askopenfilename(filetypes=[("تصویر", "*.png *.jpg *.webp"), ("همه فایل‌ها", "*.*")])
        photo_path=p
        photo_text.configure(text="✔"+os.path.basename(p),text_color="#4ade80")
    except:
        pass
def save():
    global photo_path
    name=name_entry.get()
    phone=phone_entry.get()
    if not name:
        messagebox.showerror("خطا","لطفا نام را وارد کنید")
        return
    if not phone.isdigit():
        messagebox.showerror("خطا","لطفا عدد وارد کنید")
        return
    if len(phone)!=11:
        messagebox.showerror("خطا","شماره باید یازده رقمی باشد")
        return
    saved_path=""
    if photo_path:
        ext=os.path.splitext(photo_path)[1]
        dest=os.path.join("image",f"{phone}{ext}")
        shutil.copy2(photo_path,dest)
        saved_path=dest
    try:
        cursor.execute("INSERT into user(name,phone,image_path)values(?,?,?)",(name,phone,saved_path))
        coon.commit()
        messagebox.showinfo("تبریک","اطلاعات در مخاطبین ذخیره شد")
        home()
        
    except sqlite3.IntegrityError:
        messagebox.showerror("خطا","این شماره وارد شده است")
def add_user():
    global photo_path,photo_text,name_entry,phone_entry
    clear()
    make_header("➕  افزودن مخاطب", "اطلاعات مخاطب جدید را وارد کنید")
    photo_path=""
    card=customtkinter.CTkFrame(content,width=450,height=600,corner_radius=15,fg_color="#1e1e35")
    card.pack(pady=30)
    card.pack_propagate(False)
    def field(parent, label):
        customtkinter.CTkLabel(parent, text=label, font=("Tahoma", 12, "bold"), text_color="#a0a0c0").pack(anchor="e", padx=50, pady=(18, 4))
        e = customtkinter.CTkEntry(parent, width=280, height=40, corner_radius=10,
                                   font=("Tahoma", 13), justify="right",
                                   border_color="#333355", fg_color="#12121f")
        e.pack()
        return e
    name_entry= field(card,"نام و نام خانوادگی")
    phone_entry=field(card,"شماره")
    
    customtkinter.CTkButton(card,text="📷 انتخاب عکس",text_color="#BCBCBC",fg_color="green",hover_color="#29914B",width=200,height=10,corner_radius=15,command=image_chose).pack(pady=(20,5))
    photo_text = customtkinter.CTkLabel(card, text="تصویری انتخاب نشده", font=("Tahoma", 11), text_color="#6b7280")
    photo_text.pack()

    btn_row = customtkinter.CTkFrame(card, fg_color="transparent")
    btn_row.pack(pady=22)
    customtkinter.CTkButton(btn_row, text="💾  ذخیره", font=("Tahoma", 13, "bold"),
                            width=130, height=40, corner_radius=10,
                            fg_color="#2563eb", hover_color="#1d4ed8", command=save).pack(side="left", padx=10)
    customtkinter.CTkButton(btn_row, text="↩  بازگشت", font=("Tahoma", 13),
                            width=130, height=40, corner_radius=10,
                            fg_color="#374151", hover_color="#4b5563", command=home).pack(side="left", padx=10)
def delete(phone):
    if messagebox.askyesno("توجه",f"آیا می خوایید شماره ({phone}) را پاک کنی"):
        cursor.execute("delete from user where phone=?",(phone,))
        coon.commit()
        show_user()
def show_user():
    clear()
    make_header("مخاطبین","مخاطبین ثبت شده")
    scrool=customtkinter.CTkScrollableFrame(content,fg_color="transparent", corner_radius=0)
    scrool.pack(fill="both",expand=True,pady=20,padx=15)
    cursor.execute("select name,phone,image_path from user")
    users=cursor.fetchall()
    
    if not users:
        empty=customtkinter.CTkFrame(scrool,fg_color="transparent")
        customtkinter.CTkLabel(empty,text="👤",font=("tahoma",48)).pack()
        customtkinter.CTkLabel(empty,text="مخاطبین وارد نشده",font=("tahoma",15)).pack(pady=2)
        empty.pack(pady=80)
        return
    for name,phone,image_path in users:
        card=customtkinter.CTkFrame(scrool,height=90,corner_radius=14,fg_color="#444444")
        card.pack(fill="x",pady=16,padx=20)
        card.pack_propagate(False)

        if image_path and os.path.exists(image_path):
            img=Image.open(image_path)
            ctk_img=customtkinter.CTkImage(light_image=img,dark_image=img,size=(58,58))
            customtkinter.CTkLabel(card,image=ctk_img,text="").pack(side="right",padx=18, pady=16)
        else:
            av=customtkinter.CTkFrame(card,width=50,height=30,corner_radius=14,fg_color="#23D9D9")
            av.pack(side="right",fill="y",padx=18,pady=16)
            av.pack_propagate(False)
            customtkinter.CTkLabel(av,text=name[0].upper(),font=("tahoma",18,"bold"),fg_color="#23D9D9",text_color="#111111").pack(expand=True)
        
        into=customtkinter.CTkFrame(card,fg_color="transparent")
        into.pack(side="right",fill="y",pady=18)
        customtkinter.CTkLabel(into,text=name,font=("Tahoma", 15, "bold"),text_color="#B1A5A5").pack(anchor="e")
        customtkinter.CTkLabel(into,text=phone,font=("Tahoma", 15, "bold"),text_color="#B1A5A5").pack(anchor="e",pady=4)
        
        customtkinter.CTkButton(card, text="🗑", width=38, height=38, corner_radius=10,
            font=("Tahoma", 16), fg_color="#7f1d1d", hover_color="#991b1b",
            command=lambda ph=phone: delete(ph)).pack(side="left", padx=18)
sidebar_btn("خانه", "🏠", home)
sidebar_btn("افزودن مخاطب", "➕", add_user)
sidebar_btn("مخاطبین", "📋", show_user)

def on_close():
    coon.close()
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_close)

home()
app.mainloop()