"""
Telegram Sender - GUI tool for sending messages and media to Telegram
Author: Nexus
License: All Rights Reserved

Features:
- Send text messages to Telegram
- Send photos, videos, and documents
- Clean GUI with two windows
- Threaded sending (no UI freeze)
"""
import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import requests

# ─────────────────────────────────────────────────────────────
# CONFIG — put your credentials here (or set env variables)
# ─────────────────────────────────────────────────────────────
BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "YOUR_BOT_TOKEN")
CHAT_ID   = os.getenv("TG_CHAT_ID",   "YOUR_CHAT_ID")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


# ─────────────────────────────────────────────────────────────
#  TELEGRAM API
# ─────────────────────────────────────────────────────────────
def send_message(text: str):
    """Send a text message to the configured chat."""
    url = f"{BASE_URL}/sendMessage"
    r = requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=30)
    return r.ok, r.json()


def send_media(file_path: str, caption: str = ""):
    """Send a photo, video, or document depending on the file extension."""
    ext = file_path.lower().rsplit(".", 1)[-1] if "." in file_path else ""

    if ext in ("jpg", "jpeg", "png", "gif", "webp"):
        endpoint, field = "sendPhoto", "photo"
    elif ext in ("mp4", "mov", "avi", "mkv"):
        endpoint, field = "sendVideo", "video"
    else:
        endpoint, field = "sendDocument", "document"

    url = f"{BASE_URL}/{endpoint}"
    with open(file_path, "rb") as f:
        r = requests.post(
            url,
            files={field: f},
            data={"chat_id": CHAT_ID, "caption": caption},
            timeout=120,
        )
    return r.ok, r.json()


# ─────────────────────────────────────────────────────────────
# MESSAGE GUI
# ─────────────────────────────────────────────────────────────
class MessageGUI:
    def __init__(self, root):
        self.root = root
        root.title("Telegram – Send Message")
        root.geometry("500x400")

        ttk.Label(root, text="Message:").pack(anchor="w", padx=10, pady=(10, 0))

        self.text = tk.Text(root, wrap="word", height=12)
        self.text.pack(fill="both", expand=True, padx=10, pady=5)

        self.status = ttk.Label(root, text="Ready", foreground="gray")
        self.status.pack(anchor="w", padx=10)

        ttk.Button(root, text="Send", command=self.on_send).pack(pady=10)

    def on_send(self):
        msg = self.text.get("1.0", "end").strip()
        if not msg:
            messagebox.showwarning("Empty", "Please type a message.")
            return
        self.status.config(text="Sending...", foreground="blue")
        threading.Thread(target=self._worker, args=(msg,), daemon=True).start()

    def _worker(self, msg):
        try:
            ok, resp = send_message(msg)
            if ok:
                self.status.config(text="✅ Sent!", foreground="green")
                self.text.delete("1.0", "end")
            else:
                self.status.config(text=f"❌ {resp.get('description')}", foreground="red")
        except Exception as e:
            self.status.config(text=f"❌ {e}", foreground="red")


# ─────────────────────────────────────────────────────────────
#  MEDIA GUI
# ─────────────────────────────────────────────────────────────
class MediaGUI:
    def __init__(self, root):
        self.root = root
        root.title("Telegram – Send Media")
        root.geometry("520x280")

        self.file_path = tk.StringVar()

        # File picker row
        row = ttk.Frame(root)
        row.pack(fill="x", padx=10, pady=(15, 5))
        ttk.Entry(row, textvariable=self.file_path).pack(side="left", fill="x", expand=True)
        ttk.Button(row, text="Browse…", command=self.browse).pack(side="left", padx=5)

        # Caption
        ttk.Label(root, text="Caption (optional):").pack(anchor="w", padx=10, pady=(10, 0))
        self.caption = tk.Text(root, height=5, wrap="word")
        self.caption.pack(fill="both", expand=True, padx=10)

        self.status = ttk.Label(root, text="Ready", foreground="gray")
        self.status.pack(anchor="w", padx=10)

        ttk.Button(root, text="Send", command=self.on_send).pack(pady=10)

    def browse(self):
        path = filedialog.askopenfilename(
            title="Choose file",
            filetypes=[
                ("All supported",
                 "*.jpg *.jpeg *.png *.gif *.webp *.mp4 *.mov *.avi *.mkv *.pdf *.zip *.txt"),
                ("Images", "*.jpg *.jpeg *.png *.gif *.webp"),
                ("Videos", "*.mp4 *.mov *.avi *.mkv"),
                ("All files", "*.*"),
            ],
        )
        if path:
            self.file_path.set(path)

    def on_send(self):
        path = self.file_path.get().strip()
        if not path:
            messagebox.showwarning("No file", "Please choose a file first.")
            return
        caption = self.caption.get("1.0", "end").strip()
        self.status.config(text="Sending...", foreground="blue")
        threading.Thread(target=self._worker, args=(path, caption), daemon=True).start()

    def _worker(self, path, caption):
        try:
            ok, resp = send_media(path, caption)
            if ok:
                self.status.config(text="✅ Sent!", foreground="green")
                self.caption.delete("1.0", "end")
            else:
                self.status.config(text=f"❌ {resp.get('description')}", foreground="red")
        except Exception as e:
            self.status.config(text=f"❌ {e}", foreground="red")


# ─────────────────────────────────────────────────────────────
# LAUNCHER — opens both windows
# ─────────────────────────────────────────────────────────────
def main():
    root = tk.Tk()
    root.withdraw()  # hide the empty root window

    msg_win = tk.Toplevel(root)
    MediaGUI_win = tk.Toplevel(root)

    MessageGUI(msg_win)
    MediaGUI(MediaGUI_win)

    # Close everything when the message window is closed
    msg_win.protocol("WM_DELETE_WINDOW", root.destroy)

    root.mainloop()


if __name__ == "__main__":
    main()