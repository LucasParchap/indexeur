import tkinter as tk
from tkinter import messagebox
import random
import string

# ============================================================
# CONFIGURATION
# ============================================================

CAESAR_KEY = 7

APP_TITLE = "CIPHER // TERMINAL"

BG = "#0d1117"
CARD = "#161b22"
INPUT_BG = "#21262d"
TEXT = "#f0f6fc"
SECONDARY = "#8b949e"
ACCENT = "#58a6ff"
GREEN = "#3fb950"
BORDER = "#30363d"


# ============================================================
# CHIFFREMENT CÉSAR
# ============================================================

def caesar_decrypt(text, shift):
    result = ""

    for char in text:

        if "A" <= char <= "Z":
            result += chr(
                (ord(char) - ord("A") - shift) % 26 + ord("A")
            )

        elif "a" <= char <= "z":
            result += chr(
                (ord(char) - ord("a") - shift) % 26 + ord("a")
            )

        else:
            # Accents, chiffres, espaces et ponctuation
            # restent inchangés
            result += char

    return result


# ============================================================
# APPLICATION
# ============================================================

class CipherTerminal:

    def __init__(self, root):

        self.root = root

        root.title(APP_TITLE)
        root.geometry("720x620")
        root.minsize(650, 580)
        root.configure(bg=BG)

        self.animation_running = False

        self.create_ui()


    # ========================================================
    # INTERFACE
    # ========================================================

    def create_ui(self):

        # TITRE

        title = tk.Label(
            self.root,
            text="CIPHER // TERMINAL",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 25, "bold")
        )

        title.pack(
            pady=(30, 4)
        )


        subtitle = tk.Label(
            self.root,
            text="Secure Message Decoder",
            bg=BG,
            fg=SECONDARY,
            font=("Consolas", 10)
        )

        subtitle.pack(
            pady=(0, 25)
        )


        # ====================================================
        # CARTE
        # ====================================================

        self.card = tk.Frame(
            self.root,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        self.card.pack(
            padx=40,
            pady=10,
            fill="both",
            expand=True
        )


        # ====================================================
        # MESSAGE CODÉ
        # ====================================================

        input_label = tk.Label(
            self.card,
            text="MESSAGE ENCRYPTED",
            bg=CARD,
            fg=SECONDARY,
            font=("Consolas", 10, "bold")
        )

        input_label.pack(
            anchor="w",
            padx=25,
            pady=(25, 8)
        )


        self.input_text = tk.Text(
            self.card,
            height=7,
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            font=("Consolas", 12),
            wrap="word",
            padx=15,
            pady=15
        )

        self.input_text.pack(
            padx=25,
            fill="x"
        )


        # ====================================================
        # BOUTON DECODE
        # ====================================================

        decrypt_button = tk.Button(
            self.card,
            text="DECODE MESSAGE",
            command=self.start_decryption,
            bg=ACCENT,
            fg="white",
            activebackground=ACCENT,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 11, "bold"),
            padx=30,
            pady=11
        )

        decrypt_button.pack(
            pady=20
        )


        # ====================================================
        # STATUT
        # ====================================================

        self.status = tk.Label(
            self.card,
            text="SYSTEM READY // WAITING FOR INPUT",
            bg=CARD,
            fg=SECONDARY,
            font=("Consolas", 9)
        )

        self.status.pack(
            pady=(0, 15)
        )


        # ====================================================
        # RÉSULTAT
        # ====================================================

        result_label = tk.Label(
            self.card,
            text="DECODED MESSAGE",
            bg=CARD,
            fg=SECONDARY,
            font=("Consolas", 10, "bold")
        )

        result_label.pack(
            anchor="w",
            padx=25,
            pady=(5, 8)
        )


        self.result_text = tk.Text(
            self.card,
            height=7,
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            font=("Segoe UI", 13),
            wrap="word",
            padx=15,
            pady=15
        )

        self.result_text.pack(
            padx=25,
            fill="both",
            expand=True
        )


    # ========================================================
    # LANCEMENT DU DÉCHIFFREMENT
    # ========================================================

    def start_decryption(self):

        if self.animation_running:
            return

        encrypted = self.input_text.get(
            "1.0",
            "end-1c"
        )

        if not encrypted.strip():

            messagebox.showwarning(
                "NO DATA",
                "Aucun message détecté."
            )

            return


        decrypted = caesar_decrypt(
            encrypted,
            CAESAR_KEY
        )


        self.animation_running = True


        self.result_text.delete(
            "1.0",
            "end"
        )


        self.status.config(
            text="ANALYZING ENCRYPTED DATA...",
            fg=SECONDARY
        )


        self.root.after(
            600,
            lambda: self.fake_key_scan(
                encrypted,
                decrypted,
                1
            )
        )


    # ========================================================
    # TEST DES CLÉS
    # ========================================================

    def fake_key_scan(
        self,
        encrypted,
        decrypted,
        attempt
    ):

        if attempt < CAESAR_KEY:

            self.status.config(
                text=f"TESTING DECRYPTION KEY [{attempt}]..."
            )


            fake_text = caesar_decrypt(
                encrypted,
                attempt
            )


            preview = fake_text[:80]


            self.set_result(
                preview
            )


            self.root.after(
                220,
                lambda: self.fake_key_scan(
                    encrypted,
                    decrypted,
                    attempt + 1
                )
            )


        else:

            self.status.config(
                text=f"KEY [{CAESAR_KEY}] ACCEPTED // DECRYPTING...",
                fg=GREEN
            )


            self.result_text.delete(
                "1.0",
                "end"
            )


            self.root.after(
                500,
                lambda: self.reveal_message(
                    decrypted,
                    0
                )
            )


    # ========================================================
    # ANIMATION DU MESSAGE
    # ========================================================

    def reveal_message(
        self,
        message,
        index
    ):

        if index >= len(message):

            self.status.config(
                text="DECRYPTION COMPLETE // MESSAGE VERIFIED",
                fg=GREEN
            )

            self.animation_running = False

            return


        char = message[index]


        if char.isalpha() and char.isascii():

            random_char = random.choice(
                string.ascii_letters
            )


            self.result_text.insert(
                "end",
                random_char
            )


            self.result_text.see(
                "end"
            )


            self.root.after(
                25,
                lambda: self.replace_last_char(
                    char,
                    message,
                    index
                )
            )


        else:

            self.result_text.insert(
                "end",
                char
            )


            self.root.after(
                30,
                lambda: self.reveal_message(
                    message,
                    index + 1
                )
            )


    # ========================================================
    # REMPLACEMENT CARACTÈRE
    # ========================================================

    def replace_last_char(
        self,
        real_char,
        message,
        index
    ):

        self.result_text.delete(
            "end-2c",
            "end-1c"
        )


        self.result_text.insert(
            "end",
            real_char
        )


        self.result_text.see(
            "end"
        )


        self.root.after(
            20,
            lambda: self.reveal_message(
                message,
                index + 1
            )
        )


    # ========================================================
    # UTILITAIRE
    # ========================================================

    def set_result(
        self,
        text
    ):

        self.result_text.delete(
            "1.0",
            "end"
        )

        self.result_text.insert(
            "1.0",
            text
        )


# ============================================================
# LANCEMENT
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = CipherTerminal(root)

    root.mainloop()
