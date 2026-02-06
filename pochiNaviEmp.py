import json
import os
import sys
from playwright.sync_api import sync_playwright

def connexion_personnel():
    # [cite_start]実行環境に合わせたパス解決 [cite: 1]
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))

    config_path = os.path.join(script_dir, 'config.json')

    # [cite_start]設定ファイルの読み込み [cite: 1]
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            conf = json.load(f)
    except Exception as e:
        print(f"Erreur: {e}")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("Accès à la page de connexion...")
        page.goto("https://pochipass.com/kanri001.php")

        # HTML構造に基づいた入力操作
        page.fill('input[name="username"]', conf['identifiant'])
        page.fill('input[name="password"]', conf['mot_de_passe'])

        print("Tentative de connexion...")
        # フォームの送信
        page.click('button[type="submit"]')

        # ログイン後の遷移確認（例としてURLの変化を待つ）
        page.wait_for_load_state("networkidle")
        
        print("Connecté avec succès !")

        # ブラウザを閉じずに維持
        input("Appuyez sur Entrée pour fermer le navigateur...")
        browser.close()

if __name__ == "__main__":
    connexion_personnel()