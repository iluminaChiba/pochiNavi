import json
import os
import sys
from playwright.sync_api import sync_playwright

def executer_le_pointage(page, mode):
    """
    打刻処理（入室/退室）を汎用的に実行する
    mode: 'IN' または 'OUT'
    """
    # モードに応じたIDとラベルの設定
    target_id = "#staffIN0" if mode == "IN" else "#staffOUT0"
    label = "entrée" if mode == "IN" else "sortie"

    print(f"Ouverture du menu déroulant pour {label}...")
    page.click('a.dropdown-toggle:has-text("卓美")')
    
    target_button = page.locator(target_id)
    
    if target_button.is_enabled():
        print(f"Bouton de {label} cliquable. Pointage en cours...")
        target_button.click()
        page.wait_for_load_state("load")
        print(f"Pointage de {label} terminé avec succès !")
    else:
        print(f"Le bouton de {label} est déjà désactivé.")

def connexion_personnel(mode):
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
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("Connexion au système...")
        page.goto("https://pochipass.com/kanri001.php")

        page.fill('input[name="username"]', conf['identifiant'])
        page.fill('input[name="password"]', conf['mot_de_passe'])
        page.click('button[type="submit"]')

        page.wait_for_load_state("networkidle")
        print("Connecté avec succès !")

        # 指定されたモードで打刻を実行
        executer_le_pointage(page, mode)

        print("\nToutes les opérations sont terminées.")
        # 自動で閉じる場合は以下をコメントアウトしてください
        # input("Appuyez sur Entrée pour fermer le navigateur...")
        browser.close()

if __name__ == "__main__":
    # 引数のチェック（デフォルトは IN としておく）
    mode_selectionne = "IN"
    if len(sys.argv) > 1:
        arg = sys.argv[1].upper()
        if arg in ["IN", "OUT"]:
            mode_selectionne = arg

    connexion_personnel(mode_selectionne)