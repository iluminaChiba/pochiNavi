import json
import os
import sys
from playwright.sync_api import sync_playwright

def executer_le_pointage(page):
    """
    ドロップダウンを展開し、入室ボタンをクリックする
    """
    print("Ouverture du menu déroulant...")
    # '養老 卓美' を含むリンクをクリックしてメニューを展開
    page.click('a.dropdown-toggle:has-text("卓美")')
    
    # ボタンが操作可能になるのを待つ
    target_button = page.locator("#staffIN0")
    
    # ボタンが活性化（出勤前）しているか確認 
    if target_button.is_enabled():
        print("Bouton d'entrée cliquable. Pointage en cours...")
        target_button.click()
        # ページリロードを待機 
        page.wait_for_load_state("load")
        print("Pointage terminé avec succès !")
    else:
        print("Le bouton est déjà désactivé (Déjà pointé aujourd'hui ?).")

def connexion_personnel():
    # パス解決と設定読み込み 
    script_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.json')

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            conf = json.load(f)
    except Exception as e:
        print(f"Erreur de config: {e}")
        return

    with sync_playwright() as p:
        # ブラウザ起動 
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("Connexion au système...")
        page.goto("https://pochipass.com/kanri001.php")

        # ログイン情報の入力 
        page.fill('input[name="username"]', conf['identifiant'])
        page.fill('input[name="password"]', conf['mot_de_passe'])
        page.click('button[type="submit"]')

        # 遷移（kanri011.php）を待つ 
        page.wait_for_load_state("networkidle")
        print("Connecté avec succès !")

        # --- 自動打刻処理の呼び出し ---
        executer_le_pointage(page)

        print("\nToutes les opérations sont terminées.")
        input("Appuyez sur Entrée pour fermer le navigateur...")
        browser.close()

if __name__ == "__main__":
    connexion_personnel()