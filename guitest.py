import customtkinter as ctk
import json
import os
from tkinter import messagebox

CONFIG_FILE = 'config.json'


def load_config():
    """設定ファイルを読み込む"""
    if not os.path.exists(CONFIG_FILE):
        messagebox.showerror("エラー", f"設定ファイルが見つかりません: {CONFIG_FILE}")
        return {"key1": "", "key2": "", "key3": ""}

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        messagebox.showerror("エラー", f"設定ファイルの読み込みに失敗しました: {CONFIG_FILE}")
        return {"key1": "", "key2": "", "key3": ""}


def save_config(config):
    """設定ファイルを保存"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception as e:
        messagebox.showerror("エラー", f"設定ファイルの保存に失敗しました: {e}")


def on_save():
    """保存ボタン押下時の処理"""
    key1 = entry1.get().strip()
    key2 = entry2.get().strip()
    key3 = entry3.get().strip()

    # 入力バリデーション
    if not (key1.isdigit() and key2.isdigit() and key3.isdigit()):
        messagebox.showerror("入力エラー", "3つすべての項目に数値のみを入力してください。")
        return

    new_config = {"key1": key1, "key2": key2, "key3": key3}
    save_config(new_config)
    messagebox.showinfo("完了", "設定が保存されました。")
    app.destroy()  # 終了


# GUI初期設定
ctk.set_appearance_mode("light")  # "dark" も可
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("自動ログイン補助ツール")
app.geometry("400x300")

config = load_config()

# タイトル
ctk.CTkLabel(
    app,
    text="三つの数字を入力してください",
    font=("Meiryo UI", 16, "bold")
).pack(pady=15)

# 入力欄
frame = ctk.CTkFrame(app)
frame.pack(pady=10)

ctk.CTkLabel(frame, text="1:", width=50, anchor="e").grid(row=0, column=0, padx=5, pady=5)
entry1 = ctk.CTkEntry(frame, width=200)
entry1.insert(0, config.get("key1", ""))
entry1.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(frame, text="2:", width=50, anchor="e").grid(row=1, column=0, padx=5, pady=5)
entry2 = ctk.CTkEntry(frame, width=200)
entry2.insert(0, config.get("key2", ""))
entry2.grid(row=1, column=1, padx=5, pady=5)

ctk.CTkLabel(frame, text="3:", width=50, anchor="e").grid(row=2, column=0, padx=5, pady=5)
entry3 = ctk.CTkEntry(frame, width=200)
entry3.insert(0, config.get("key3", ""))
entry3.grid(row=2, column=1, padx=5, pady=5)

# ボタン
btn_frame = ctk.CTkFrame(app)
btn_frame.pack(pady=20)

ctk.CTkButton(btn_frame, text="保存", width=100, command=on_save).grid(row=0, column=0, padx=10)
ctk.CTkButton(btn_frame, text="キャンセル", width=100, command=app.destroy).grid(row=0, column=1, padx=10)

app.mainloop()
