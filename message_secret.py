import tkinter as tk
from tkinter import messagebox
import random
import string


# ============================================================
# CONFIGURATION
# ============================================================

CAESAR_KEY = 7
APP_TITLE = "🤫"

# Palette principale
BG = "#FFF7F2"
CARD = "#FFFFFF"
INPUT_BG = "#FFFDFC"

TEXT = "#3D3442"
SECONDARY = "#8A788F"

ACCENT = "#F06C9B"
ACCENT_HOVER = "#E85B8F"

BORDER = "#EADDE5"

# Partie secrète / sombre
SECRET_BG = "#302A33"
SECRET_HOVER = "#463D49"
SECRET_TEXT = "#FFFFFF"


# ============================================================
# DÉCHIFFREMENT CÉSAR
# ============================================================

def caesar_decrypt(text, shift):

    result = ""

    for char in text:

        if "A" <= char <= "Z":

            result += chr(
                (ord(char) - ord("A") - shift) % 26
                + ord("A")
            )

        elif "a" <= char <= "z":

            result += chr(
                (ord(char) - ord("a") - shift) % 26
                + ord("a")
            )

        else:

            # Accents, chiffres, ponctuation et emojis
            # restent inchangés.
            result += char

    return result


# ============================================================
# APPLICATION
# ============================================================

class SecretMessageApp:

    def __init__(self, root):

        self.root = root

        root.title(APP_TITLE)
        root.geometry("760x650")
        root.minsize(680, 600)

        root.configure(
            bg=BG
        )

        self.animation_running = False

        # Message actuellement affiché
        self.displayed_text = ""

        # Vrai message déchiffré
        self.final_message = ""

        # État caché / visible
        self.message_hidden = False

        self.create_ui()


    # ========================================================
    # INTERFACE
    # ========================================================

    def create_ui(self):

        # ----------------------------------------------------
        # EMOJI
        # ----------------------------------------------------

        emoji = tk.Label(
            self.root,
            text="🤫",
            bg=BG,
            font=("Segoe UI Emoji", 42)
        )

        emoji.pack(
            pady=(18, 10)
        )


        # ----------------------------------------------------
        # CARTE PRINCIPALE
        # ----------------------------------------------------

        self.card = tk.Frame(
            self.root,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        self.card.pack(
            padx=45,
            pady=(0, 22),
            fill="both",
            expand=True
        )


        # ====================================================
        # MESSAGE CODÉ
        # ====================================================

        input_label = tk.Label(
            self.card,
            text="Colle ton message codé ici",
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI", 11, "bold")
        )

        input_label.pack(
            anchor="w",
            padx=30,
            pady=(22, 8)
        )


        # ----------------------------------------------------
        # CONTENEUR DU CHAMP
        # ----------------------------------------------------

        self.input_container = tk.Frame(
            self.card,
            bg=INPUT_BG,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        self.input_container.pack(
            padx=30,
            fill="x"
        )


        # ----------------------------------------------------
        # SCROLLBAR DU CHAMP
        #
        # Créée mais PAS affichée au départ.
        # ----------------------------------------------------

        self.input_scrollbar = tk.Scrollbar(
            self.input_container,
            orient="vertical"
        )


        # ----------------------------------------------------
        # CHAMP ÉDITABLE
        # ----------------------------------------------------

        self.input_text = tk.Text(
            self.input_container,
            height=5,
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            borderwidth=0,
            font=("Consolas", 12),
            wrap="word",
            padx=15,
            pady=12
        )

        self.input_text.pack(
            side="left",
            fill="both",
            expand=True
        )


        # ----------------------------------------------------
        # GESTION AUTOMATIQUE DE LA SCROLLBAR
        # ----------------------------------------------------

        self.input_text.config(
            yscrollcommand=self.update_input_scrollbar
        )

        self.input_scrollbar.config(
            command=self.input_text.yview
        )


        # ====================================================
        # BOUTON DÉCOUVRIR
        # ====================================================

        self.decrypt_button = tk.Button(
            self.card,
            text="✨  Découvrir le message",
            command=self.start_decryption,
            bg=ACCENT,
            fg="white",
            activebackground=ACCENT_HOVER,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 11, "bold"),
            padx=30,
            pady=10
        )

        self.decrypt_button.pack(
            pady=(16, 15)
        )


        # ====================================================
        # SÉPARATEUR
        # ====================================================

        separator = tk.Frame(
            self.card,
            bg=BORDER,
            height=1
        )

        separator.pack(
            padx=30,
            fill="x",
            pady=(0, 15)
        )


        # ====================================================
        # BOUTON CACHER / REVOIR
        # ====================================================

        self.visibility_button = tk.Button(
            self.card,
            text="🙈  Cacher le message",
            command=self.toggle_message_visibility,
            bg=SECRET_BG,
            fg=SECRET_TEXT,
            activebackground=SECRET_HOVER,
            activeforeground=SECRET_TEXT,
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=22,
            pady=7
        )

        # Invisible au lancement


        # ====================================================
        # CONTENEUR DU RÉSULTAT
        # ====================================================

        self.result_container = tk.Frame(
            self.card,
            bg=INPUT_BG,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        self.result_container.pack(
            padx=30,
            pady=(5, 20),
            fill="both",
            expand=True
        )


        # ----------------------------------------------------
        # SCROLLBAR DU RÉSULTAT
        #
        # Créée mais invisible au départ.
        # ----------------------------------------------------

        self.result_scrollbar = tk.Scrollbar(
            self.result_container,
            orient="vertical"
        )


        # ----------------------------------------------------
        # RÉSULTAT
        # ----------------------------------------------------

        self.result_text = tk.Text(
            self.result_container,
            height=8,
            bg=INPUT_BG,
            fg=TEXT,
            relief="flat",
            borderwidth=0,
            font=("Segoe UI", 13),
            wrap="word",
            padx=18,
            pady=15,
            cursor="arrow"
        )

        self.result_text.pack(
            side="left",
            fill="both",
            expand=True
        )


        # ----------------------------------------------------
        # GESTION AUTOMATIQUE DE LA SCROLLBAR
        # ----------------------------------------------------

        self.result_text.config(
            yscrollcommand=self.update_result_scrollbar
        )

        self.result_scrollbar.config(
            command=self.result_text.yview
        )


        # Résultat en lecture seule
        self.result_text.config(
            state="disabled"
        )


    # ========================================================
    # SCROLLBAR AUTOMATIQUE DU CHAMP DU HAUT
    # ========================================================

    def update_input_scrollbar(self, first, last):

        first = float(first)
        last = float(last)


        # Met à jour la position du curseur
        self.input_scrollbar.set(
            first,
            last
        )


        # ----------------------------------------------------
        # Tout le texte est visible :
        # on cache complètement la scrollbar.
        # ----------------------------------------------------

        if first <= 0.0 and last >= 1.0:

            if self.input_scrollbar.winfo_ismapped():

                self.input_scrollbar.pack_forget()


        # ----------------------------------------------------
        # Le texte dépasse :
        # la scrollbar apparaît.
        # ----------------------------------------------------

        else:

            if not self.input_scrollbar.winfo_ismapped():

                self.input_scrollbar.pack(
                    side="right",
                    fill="y"
                )


    # ========================================================
    # SCROLLBAR AUTOMATIQUE DU RÉSULTAT
    # ========================================================

    def update_result_scrollbar(self, first, last):

        first = float(first)
        last = float(last)


        # Position du curseur
        self.result_scrollbar.set(
            first,
            last
        )


        # ----------------------------------------------------
        # Tout tient dans le cadre
        # ----------------------------------------------------

        if first <= 0.0 and last >= 1.0:

            if self.result_scrollbar.winfo_ismapped():

                self.result_scrollbar.pack_forget()


        # ----------------------------------------------------
        # Le contenu dépasse
        # ----------------------------------------------------

        else:

            if not self.result_scrollbar.winfo_ismapped():

                self.result_scrollbar.pack(
                    side="right",
                    fill="y"
                )


    # ========================================================
    # ÉCRIRE DANS LE RÉSULTAT
    # ========================================================

    def update_result(
        self,
        text,
        color=None,
        follow_end=True
    ):

        if color is None:
            color = TEXT


        # Autorise temporairement l'écriture
        self.result_text.config(
            state="normal"
        )


        self.result_text.delete(
            "1.0",
            "end"
        )


        self.result_text.insert(
            "1.0",
            text
        )


        self.result_text.config(
            fg=color
        )


        # Lecture seule
        self.result_text.config(
            state="disabled"
        )


        # Pendant l'animation,
        # suit automatiquement le texte.
        if follow_end:

            self.result_text.see(
                "end"
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
                "Petit oubli",
                "Il faut d'abord coller le message 👀"
            )

            return


        decrypted = caesar_decrypt(
            encrypted,
            CAESAR_KEY
        )


        self.final_message = decrypted

        self.message_hidden = False

        self.animation_running = True


        # Cache le bouton pendant le nouveau déchiffrement
        self.visibility_button.pack_forget()


        # Efface l'ancien résultat
        self.displayed_text = ""

        self.update_result(
            ""
        )


        # Remet le champ du haut au début
        self.input_text.yview_moveto(0)


        # Commence l'animation
        self.root.after(
            300,
            lambda: self.fake_key_scan(
                encrypted,
                decrypted,
                1
            )
        )


    # ========================================================
    # FAUX TEST DES CLÉS
    # ========================================================

    def fake_key_scan(
        self,
        encrypted,
        decrypted,
        attempt
    ):

        if attempt < CAESAR_KEY:

            fake_text = caesar_decrypt(
                encrypted,
                attempt
            )


            self.set_result(
                fake_text
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

            self.displayed_text = ""

            self.update_result(
                ""
            )


            self.root.after(
                350,
                lambda: self.reveal_message(
                    decrypted,
                    0
                )
            )


    # ========================================================
    # RÉVÉLATION PROGRESSIVE
    # ========================================================

    def reveal_message(
        self,
        message,
        index
    ):

        # ----------------------------------------------------
        # MESSAGE ENTIÈREMENT DÉVOILÉ
        # ----------------------------------------------------

        if index >= len(message):

            self.animation_running = False

            self.final_message = message

            self.message_hidden = False


            # Bouton cacher
            self.visibility_button.config(
                text="🙈  Cacher le message"
            )


            self.visibility_button.pack(
                pady=(0, 12),
                before=self.result_container
            )


            # Une fois le déchiffrement terminé,
            # on revient au début du message.
            self.result_text.yview_moveto(0)


            return


        char = message[index]


        # ----------------------------------------------------
        # ANIMATION DES LETTRES
        # ----------------------------------------------------

        if char.isalpha() and char.isascii():

            random_char = random.choice(
                string.ascii_letters
            )


            self.displayed_text += random_char


            self.update_result(
                self.displayed_text
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

            self.displayed_text += char


            self.update_result(
                self.displayed_text
            )


            self.root.after(
                30,
                lambda: self.reveal_message(
                    message,
                    index + 1
                )
            )


    # ========================================================
    # REMPLACEMENT DE LA LETTRE ALÉATOIRE
    # ========================================================

    def replace_last_char(
        self,
        real_char,
        message,
        index
    ):

        if self.displayed_text:

            self.displayed_text = (
                self.displayed_text[:-1]
                + real_char
            )


        self.update_result(
            self.displayed_text
        )


        self.root.after(
            20,
            lambda: self.reveal_message(
                message,
                index + 1
            )
        )


    # ========================================================
    # CACHER / REVOIR LE MESSAGE
    # ========================================================

    def toggle_message_visibility(self):

        if not self.final_message:
            return


        # ----------------------------------------------------
        # CACHER
        # ----------------------------------------------------

        if not self.message_hidden:

            self.message_hidden = True

            hidden_text = ""


            for char in self.final_message:

                if char == " ":

                    hidden_text += " "

                elif char == "\n":

                    hidden_text += "\n"

                else:

                    hidden_text += "•"


            self.update_result(
                hidden_text,
                SECONDARY,
                follow_end=False
            )


            self.visibility_button.config(
                text="👀  Revoir le message"
            )


            self.result_text.yview_moveto(0)


        # ----------------------------------------------------
        # REVOIR
        # ----------------------------------------------------

        else:

            self.message_hidden = False


            self.update_result(
                self.final_message,
                TEXT,
                follow_end=False
            )


            self.visibility_button.config(
                text="🙈  Cacher le message"
            )


            self.result_text.yview_moveto(0)


    # ========================================================
    # MODIFICATION DU TEXTE AFFICHÉ
    # ========================================================

    def set_result(
        self,
        text
    ):

        self.displayed_text = text


        self.update_result(
            text,
            TEXT
        )


# ============================================================
# LANCEMENT
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = SecretMessageApp(root)

    root.mainloop()
