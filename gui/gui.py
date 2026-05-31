import os
import customtkinter as ctk
from tkinter import filedialog
from core import core


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DiSiT - Digital Signature Tool")
        self.geometry("900x500")
        self.minsize(800, 450)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # ---------- STATE ----------
        self.file_path = None
        self.private_key_path = None
        self.public_key_path = None
        self.signature_path = None
        self.lang = "ru"

        # ---------- SOFT COLOR PALETTE ----------
        self.colors = {
            "bg": "#1e1e1e",
            "panel": "#252525",
            "off": "#3a3a3a",
            "bad": "#a05a5a",   # soft red (not aggressive)
            "ok": "#4a9b73",    # soft green
        }

        # ---------- TEXTS ----------
        self.texts = {
            "ru": {
                "file": "Файл не выбран",
                "choose_file": "Выбрать файл",
                "choose_sig": "Выбрать файл подписи",
                "choose_priv": "Выбрать private key",
                "choose_pub": "Выбрать public key",
                "gen_keys": "Сгенерировать ключи",
                "sign": "Подписать файл",
                "verify": "Проверить подпись",
            },
            "en": {
                "file": "No file selected",
                "choose_file": "Select file",
                "choose_sig": "Select signature file",
                "choose_priv": "Select private key",
                "choose_pub": "Select public key",
                "gen_keys": "Generate keys",
                "sign": "Sign file",
                "verify": "Verify signature",
            }
        }

        # ================= GRID LAYOUT =================
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------- SIDEBAR ----------
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color=self.colors["panel"])
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_rowconfigure(0, weight=1)

        # ===== TOP TEXT =====
        self.sidebar_title = ctk.CTkLabel(
            self.sidebar,
            text="DiSiT",
            font=("Arial", 34, "bold"),
            text_color="#dddddd"
        )
        self.sidebar_title.grid(row=0, column=0, pady=(15, 5), padx=10, sticky="n")

        # Контейнер кнопок внизу
        self.buttons_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.buttons_frame.grid(row=1, column=0, sticky="sew", padx=0, pady=(0, 10))

        # ---------- MAIN ----------
        self.main = ctk.CTkFrame(self, fg_color=self.colors["bg"])
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)

        # ---------- TOPBAR ----------
        self.topbar = ctk.CTkFrame(self.main, height=40, fg_color=self.colors["panel"])
        self.topbar.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.lang_menu = ctk.CTkOptionMenu(
            self.topbar,
            values=["RU", "EN"],
            command=self.change_lang,
            width=100
        )
        self.lang_menu.set("RU")
        self.lang_menu.pack(side="right", padx=10)

        self.file_label = ctk.CTkLabel(
            self.topbar,
            text=self.texts[self.lang]["file"],
            text_color="#aaaaaa"
        )
        self.file_label.pack(side="left", padx=10)

        # ---------- LOG ----------
        self.log = ctk.CTkTextbox(self.main, fg_color=self.colors["panel"])
        self.log.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.log.configure(state="disabled")

        # ================= BUTTONS =================
        self.btn_file = self.create_btn("choose_file", self.choose_file)
        self.btn_sig = self.create_btn("choose_sig", self.choose_signature_file)
        self.btn_priv = self.create_btn("choose_priv", self.choose_private_key)
        self.btn_pub = self.create_btn("choose_pub", self.choose_public_key)
        self.btn_gen = self.create_btn("gen_keys", self.generate_keys)
        self.btn_sign = self.create_btn("sign", self.sign_file)
        self.btn_verify = self.create_btn("verify", self.verify_file)

        for b in [
            self.btn_file,
            self.btn_sig,
            self.btn_priv,
            self.btn_pub,
            self.btn_gen,
            self.btn_sign,
            self.btn_verify
        ]:
            b.pack(in_=self.buttons_frame, pady=10, padx=12, fill="x")

        # ---------- INIT STATES ----------
        self.update_button_state(self.btn_file, False)
        self.update_button_state(self.btn_sig, False)
        self.update_button_state(self.btn_priv, False)
        self.update_button_state(self.btn_pub, False)

    # ================= BUTTON STYLE =================
    def create_btn(self, key, cmd):
        return ctk.CTkButton(
            self.buttons_frame,
            text=self.texts[self.lang][key],
            command=cmd,
            width=180,
            height=36,
            corner_radius=10,
            border_width=2,
            border_color=self.colors["off"],
            fg_color="#1f1f1f",
            hover_color="#2a2a2a"
        )

    def update_button_state(self, button, ok: bool):
        if ok:
            button.configure(
                border_color=self.colors["ok"],
                fg_color="#1f2a26"
            )
        else:
            button.configure(
                border_color=self.colors["bad"],
                fg_color="#2a1f1f"
            )

    # ================= LANGUAGE =================
    def change_lang(self, value):
        self.lang = "ru" if value == "RU" else "en"
        t = self.texts[self.lang]

        self.file_label.configure(text=t["file"])

        self.btn_file.configure(text=t["choose_file"])
        self.btn_sig.configure(text=t["choose_sig"])
        self.btn_priv.configure(text=t["choose_priv"])
        self.btn_pub.configure(text=t["choose_pub"])
        self.btn_gen.configure(text=t["gen_keys"])
        self.btn_sign.configure(text=t["sign"])
        self.btn_verify.configure(text=t["verify"])

        self.log_msg(f"[LANG] {self.lang}")

    # ================= LOG =================
    def log_msg(self, msg):
        self.log.configure(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    # ================= FILES =================
    def choose_file(self):
        file = filedialog.askopenfilename()
        if file:
            self.file_path = file
            self.file_label.configure(text=file)
            self.log_msg(f"[FILE] {file}")
            self.update_button_state(self.btn_file, True)

    def choose_signature_file(self):
        file = filedialog.askopenfilename(
            title="Select signature file",
            filetypes=[("Signature files", "*.sig"), ("All files", "*.*")]
        )
        if file:
            self.signature_path = file
            self.log_msg(f"[SIG] {file}")
            self.update_button_state(self.btn_sig, True)

    def choose_private_key(self):
        file = filedialog.askopenfilename()
        if file:
            self.private_key_path = file
            self.log_msg(f"[KEY] private: {file}")
            self.update_button_state(self.btn_priv, True)

    def choose_public_key(self):
        file = filedialog.askopenfilename()
        if file:
            self.public_key_path = file
            self.log_msg(f"[KEY] public: {file}")
            self.update_button_state(self.btn_pub, True)

    # ================= KEYS =================
    def generate_keys(self):
        priv, pub = core.generate_keypair()

        priv_path = filedialog.asksaveasfilename(
            defaultextension=".key",
            initialfile="private.key",
            title="Save private key"
        )

        pub_path = filedialog.asksaveasfilename(
            defaultextension=".key",
            initialfile="public.key",
            title="Save public key"
        )

        if priv_path and pub_path:
            core.save_private_key(priv_path, priv)
            core.save_public_key(pub_path, pub)

            # Автоматически подставляем сгенерированные ключи
            self.private_key_path = priv_path
            self.public_key_path = pub_path

            self.update_button_state(self.btn_priv, True)
            self.update_button_state(self.btn_pub, True)

            self.log_msg(f"[KEYS] generated")
            self.log_msg(f"[KEY] private auto-selected: {priv_path}")
            self.log_msg(f"[KEY] public auto-selected: {pub_path}")

    # ================= SIGN =================
    def sign_file(self):
        if not self.file_path or not self.private_key_path:
            self.log_msg("[ERROR] missing file or private key")
            return

        data = core.read_file(self.file_path)
        private_key = core.load_private_key(self.private_key_path)

        default_sig_name = os.path.basename(self.file_path) + ".sig"
        sig_path = filedialog.asksaveasfilename(
            defaultextension=".sig",
            initialfile=default_sig_name,
            title="Save signature file",
            filetypes=[("Signature files", "*.sig"), ("All files", "*.*")]
        )

        if not sig_path:
            self.log_msg("[SIGN] canceled")
            return

        signature = core.sign(data, private_key)
        core.save_signature(sig_path, signature)

        # Автоматически подставляем подпись для валидации
        self.signature_path = sig_path
        self.update_button_state(self.btn_sig, True)

        self.log_msg(f"[SIGN] {sig_path}")
        self.log_msg(f"[SIG] auto-selected for verify: {sig_path}")

    # ================= VERIFY =================
    def verify_file(self):
        if not self.file_path or not self.public_key_path or not self.signature_path:
            self.log_msg("[ERROR] missing file/public key/signature file")
            return

        try:
            data = core.read_file(self.file_path)
            public_key = core.load_public_key(self.public_key_path)
            signature = core.load_signature(self.signature_path)

            result = core.verify(data, public_key, signature)

            if result:
                self.log_msg("[VERIFY] Digital Signature is correct!")
                self.update_button_state(self.btn_verify, True)
            else:
                self.log_msg("[VERIFY] FAILED! Digital Signature is not correct")
                self.update_button_state(self.btn_verify, False)

        except Exception as e:
            self.log_msg(f"[ERROR] {str(e)}")


def gui():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    gui()