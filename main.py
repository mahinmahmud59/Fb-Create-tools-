import json, os, secrets, string, random, base64, hashlib, hmac, struct, time
from datetime import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.clipboard import Clipboard
from kivy.utils import get_color_from_hex

KV = r"""
<MainUI>:
    orientation: "vertical"
    padding: "7dp"
    spacing: "6dp"
    canvas.before:
        Color:
            rgba: (0.035,0.035,0.04,1)
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        size_hint_y: None
        height: "48dp"
        spacing: "7dp"
        Button:
            text: "🔑\\nUID"
            background_normal: ""
            background_color: (0.08,0.43,0.92,1)
            on_release: root.show_module("UID")
        Button:
            text: "▣\\nCOOKIES"
            background_normal: ""
            background_color: (0.08,0.78,0.38,1)
            on_release: root.show_module("COOKIES")
    BoxLayout:
        size_hint_y: None
        height: "48dp"
        spacing: "7dp"
        Button:
            text: "⬟\\n2FA"
            background_normal: ""
            background_color: (0.58,0.12,0.68,1)
            on_release: root.show_module("2FA")
        Button:
            text: "🔑\\n2FA OTP"
            background_normal: ""
            background_color: (0.0,0.68,0.78,1)
            on_release: root.show_module("2FA OTP")
    BoxLayout:
        id: panel
        orientation: "vertical"
        padding: "12dp"
        spacing: "8dp"
        canvas.before:
            Color:
                rgba: (1,1,1,1)
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [12,]
        Label:
            id: panel_title
            text: "Fb Create tools"
            color: (0.05,0.05,0.05,1)
            bold: True
            font_size: "21sp"
            size_hint_y: None
            height: "38dp"
        ScrollView:
            do_scroll_x: False
            GridLayout:
                id: content
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: "7dp"
    GridLayout:
        cols: 3
        size_hint_y: None
        height: "48dp"
        spacing: "6dp"
        Button:
            text: "⚡ AUTO CREATE"
            background_normal: ""
            background_color: (1,0.82,0.0,1)
            on_release: root.show_module("AUTO CREATE")
        Button:
            text: "☎ NUMBER SET"
            background_normal: ""
            background_color: (0.92,0.05,0.34,1)
            on_release: root.show_module("NUMBER SET")
        Button:
            text: "🔒 PW SET"
            background_normal: ""
            background_color: (0.58,0.12,0.68,1)
            on_release: root.show_module("PW SET")
    GridLayout:
        cols: 2
        size_hint_y: None
        height: "48dp"
        spacing: "6dp"
        Button:
            text: "▣ DESKTOP"
            background_normal: ""
            background_color: (0.58,0.12,0.68,1)
            on_release: root.show_module("DESKTOP")
        Button:
            text: "▯ AGENT SET"
            background_normal: ""
            background_color: (0.0,0.68,0.78,1)
            on_release: root.show_module("AGENT SET")
    GridLayout:
        cols: 2
        size_hint_y: None
        height: "48dp"
        spacing: "6dp"
        Button:
            text: "⟳ RELOAD"
            background_normal: ""
            background_color: (1,0.53,0.0,1)
            on_release: root.reload_app()
        Button:
            text: "▤ ALL CLEAR"
            background_normal: ""
            background_color: (0.95,0.12,0.12,1)
            on_release: root.clear_form()
"""

NAMES = ["James Smith", "John Miller", "Michael Brown", "David Wilson",
         "Daniel Taylor", "Matthew Anderson", "Christopher Thomas",
         "Andrew Jackson", "Joseph White", "Ryan Harris"]

def totp(secret):
    s = secret.replace(" ", "").upper()
    pad = "=" * ((8 - len(s) % 8) % 8)
    key = base64.b32decode(s + pad)
    counter = int(time.time()) // 30
    msg = struct.pack(">Q", counter)
    digest = hmac.new(key, msg, hashlib.sha1).digest()
    off = digest[-1] & 15
    code = (struct.unpack(">I", digest[off:off+4])[0] & 0x7fffffff) % 1000000
    return f"{code:06d}"

class MainUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {"uid":"", "name":"", "dob":"", "password":"", "phone":"",
                     "manual_code":"", "twofa_secret":"", "agent":""}
        self.show_module("AUTO CREATE")

    def add_label(self, text, size=16, color=(0.1,0.1,0.1,1)):
        from kivy.uix.label import Label
        w = Label(text=text, color=color, size_hint_y=None, height="28dp",
                  halign="left", valign="middle")
        w.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        self.ids.content.add_widget(w)

    def add_input(self, hint, key, password=False):
        w = TextInput(hint_text=hint, multiline=False, password=password,
                      size_hint_y=None, height="42dp", padding=("9dp","9dp"))
        w.text = self.data.get(key, "")
        w.bind(text=lambda inst, val: self.data.__setitem__(key, val))
        self.ids.content.add_widget(w)
        return w

    def add_button(self, text, callback, color=(0.08,0.43,0.92,1)):
        b = Button(text=text, size_hint_y=None, height="42dp",
                   background_normal="", background_color=color)
        b.bind(on_release=lambda *_: callback())
        self.ids.content.add_widget(b)

    def show_module(self, name):
        self.ids.panel_title.text = name
        self.ids.content.clear_widgets()
        if name in ("AUTO CREATE", "AUTO PROFILE"):
            self.add_label("১) Demo profile generator — শুধু টেস্ট ডেটা")
            self.add_button("Generate fictional name + DOB", self.generate_profile)
            self.add_input("Name", "name")
            self.add_input("DOB (2000–2003)", "dob")
            self.add_label("বাস্তব ব্যক্তির পরিচয় বা অন্য সাইটে অ্যাকাউন্ট তৈরির জন্য নয়।")
        elif name == "UID":
            self.add_label("নিজের অ্যাপ/টেস্ট প্রোফাইলের UID")
            self.add_input("UID লিখুন", "uid")
            self.add_button("COPY UID", lambda: self.copy(self.data["uid"]))
        elif name == "COOKIES":
            self.add_label("COOKIES / DATA BACKUP")
            self.add_label("Facebook বা অন্যের session cookie সংগ্রহ/কপি করা হবে না।")
            self.add_label("নিজের এই অ্যাপের ডেটা encrypted backup হিসেবে Export/Import করুন।")
            self.add_button("EXPORT APP BACKUP", self.export_backup)
            self.add_button("IMPORT BACKUP", self.import_backup)
        elif name == "2FA":
            self.add_label("নিজের অ্যাকাউন্টের 2FA secret এখানে দিন")
            self.add_input("Base32 secret", "twofa_secret")
            self.add_button("SAVE 2FA SECRET", self.save_local)
            self.add_label("Secret কাউকে দেবেন না।")
        elif name == "2FA OTP":
            self.add_label("নিজের সংরক্ষিত 2FA secret থেকে OTP")
            self.add_button("GENERATE 2FA OTP", self.generate_otp)
        elif name == "NUMBER SET":
            self.add_label("নিজের ব্যবহারের নম্বর লিখুন")
            self.add_input("Phone number", "phone")
            self.add_label("SMS/WhatsApp verification code নিজে বৈধভাবে পেলে লিখুন।")
            self.add_input("Manually received code", "manual_code")
            self.add_button("CONFIRM MANUAL CODE", self.confirm_manual)
        elif name == "PW SET":
            self.add_label("নিজের টেস্ট প্রোফাইলের পাসওয়ার্ড")
            self.add_input("Password", "password", True)
            self.add_button("SAVE PASSWORD LOCALLY", self.save_local)
        elif name == "DESKTOP":
            self.add_label("DESKTOP MODE")
            self.add_label("এটি মোবাইল UI-র ডেস্কটপ-স্টাইল তথ্য প্যানেল।")
            self.add_button("SHOW SAVED PROFILE", self.show_summary)
        elif name == "AGENT SET":
            self.add_label("AGENT SET — নিজের নোট/লেবেল")
            self.add_input("Agent label", "agent")
            self.add_button("SAVE AGENT LABEL", self.save_local)
        elif name == "SECURE VAULT":
            self.add_label("লোকাল ভল্ট — ডেটা এই অ্যাপের ফাইলে রাখা হয়।")
            self.add_button("SAVE LOCAL DATA", self.save_local)
        elif name == "OTP CONFIRM":
            self.add_label("নিজে পাওয়া OTP হাতে লিখে নিশ্চিত করুন")
            self.add_input("Verification code", "manual_code")
            self.add_button("CONFIRM", self.confirm_manual)
        elif name == "RELOAD":
            self.reload_app()
        else:
            self.add_label("Module: " + name)
            self.add_button("Back to AUTO CREATE", lambda: self.show_module("AUTO CREATE"))

    def generate_profile(self):
        self.data["name"] = random.choice(NAMES)
        year = random.choice([2000, 2001, 2002, 2003])
        month = random.randint(1,12)
        day = random.randint(1,28)
        self.data["dob"] = f"{year}-{month:02d}-{day:02d}"
        self.show_module("AUTO CREATE")

    def copy(self, value):
        if value:
            Clipboard.copy(value)
            self.popup("Copied", "তথ্য কপি হয়েছে।")
        else:
            self.popup("Empty", "আগে তথ্য লিখুন।")

    def generate_otp(self):
        try:
            code = totp(self.data["twofa_secret"])
            self.popup("Your 2FA OTP", code + "\\n৩০ সেকেন্ড পর কোড বদলাবে।")
            Clipboard.copy(code)
        except Exception:
            self.popup("Error", "সঠিক Base32 2FA secret দিন।")

    def confirm_manual(self):
        if self.data.get("manual_code","").strip():
            self.popup("Saved", "আপনার দেওয়া কোডটি লোকালি নোট করা হয়েছে; কোনো সার্ভারে যাচাই করা হয়নি।")
        else:
            self.popup("Missing", "কোড লিখুন।")

    def save_local(self):
        try:
            path = os.path.join(App.get_running_app().user_data_dir, "vault.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.data, f)
            self.popup("Saved", "ডেটা এই ডিভাইসে সেভ হয়েছে।")
        except Exception as e:
            self.popup("Error", str(e))

    def export_backup(self):
        self.save_local()
        self.popup("Backup", "ভল্টের লোকাল ফাইল Android app data-তে থাকে। পরের সংস্করণে encrypted export/import যোগ করা হবে।")

    def import_backup(self):
        self.popup("Import", "এই starter সংস্করণে ফাইল picker এখনো যুক্ত হয়নি।")

    def show_summary(self):
        self.popup("Profile", f"Name: {self.data['name']}\\nDOB: {self.data['dob']}\\nUID: {self.data['uid']}")

    def clear_form(self):
        self.data = {k:"" for k in self.data}
        self.show_module("AUTO CREATE")

    def reload_app(self):
        self.show_module("AUTO CREATE")

    def popup(self, title, message):
        Popup(title=title, content=Label(text=message), size_hint=(.82,.35)).open()

class FbCreateToolsApp(App):
    def build(self):
        Builder.load_string(KV)
        return MainUI()

if __name__ == "__main__":
    FbCreateToolsApp().run()