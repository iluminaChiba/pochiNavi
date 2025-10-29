from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import traceback
import json
import os
# メッセージ定数定義 ----------------------------------------------------------------

MESSAGES = {
    'config_not_found': "設定ファイルが見つかりません",
    'config_invalid_format': "設定ファイルの形式が正しくありません",
    'config_key_mismatch': "configに記録された数字の数が、入力エレメントの数と一致しません。",
    'login_success': "ログインに成功しました。",
    'login_transition_failed': "ログイン後のページ遷移を確認できませんでした。",
    'config_error': "Configエラーが発生しました",
    'timeout_error': "タイムアウトが発生しました",
    'element_not_found': "必要な要素が見つかりません",
    'unexpected_error': "予期せぬエラーが発生しました",
    'browser_closed': "スクリプトを終了します。ブラウザは開いたまま残ります。"
}


def get_messages_array():
    """従来のインデックス形式でメッセージを取得"""
    return [
        MESSAGES['config_not_found'],
        MESSAGES['config_invalid_format'],
        MESSAGES['config_key_mismatch'],
        MESSAGES['login_success'],
        MESSAGES['login_transition_failed'],
        MESSAGES['config_error'],
        MESSAGES['timeout_error'],
        MESSAGES['element_not_found'],
        MESSAGES['unexpected_error'],
        MESSAGES['browser_closed']
    ]


txt = get_messages_array()

URL = "https://pochipass.com/member/"

# スクリプトと同じディレクトリのconfig.jsonを読み込む
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'config.json')

try:
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"{txt[0]}: {config_path}")
    exit(1)
except json.JSONDecodeError:
    print(f"{txt[1]}: {config_path}")
    exit(1)
my_keys = [str(config["key1"]), str(config["key2"]), str(config["key3"])]
el_ids = ["key1", "key2", "key3"]

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Run in headless mode
driver = None

try:
    if len(my_keys) != len(el_ids):
        raise ValueError(txt[2])

    options.add_experimental_option("detach", True)  # スクリプト終了後もブラウザを開いたままにする呪文
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(URL)

    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    for el_id, key in zip(el_ids, my_keys):
        el = wait.until(EC.element_to_be_clickable((By.ID, el_id)))
        el.clear()
        el.send_keys(key)
        wait.until(lambda d: el.get_attribute('value') == key)

    login_btn = wait.until(EC.element_to_be_clickable((By.ID, "login")))
    login_btn.click()

    # ログイン後のページ遷移を待機
    try:
        wait.until(EC.url_changes(URL))
        print(txt[3])
    except TimeoutException:
        print(txt[4])
except ValueError as ve:
    print(f"{txt[5]}:{ve}")
    traceback.print_exc()

except TimeoutException as te:
    print(f"{txt[6]}: {te}")
    traceback.print_exc()

except NoSuchElementException as nse:
    print(f"{txt[7]}: {nse}")
    traceback.print_exc()

except Exception as e:
    print(f"{txt[8]}: {e}")
    traceback.print_exc()

finally:
    if driver:
        driver.quit()
        print(f"[INFO] {txt[9]}")
