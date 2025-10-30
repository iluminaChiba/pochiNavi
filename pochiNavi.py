from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import logging
import logging.handlers  # RotatingFileHandlerに必要
import json
import sys
import os
# Logファイル記録用定数--------------------------------------------------------------
MAX_BYTES = 100 * 1024  # 100KB（コメントを実際の値に修正）
BACKUP_COUNT = 5  # 古いログを保存する数
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
    'browser_closed': "スクリプトを終了します。ブラウザは開いたまま残ります。",
    'driver_not_initialized': "ChromeDriverが初期化されていません。"
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
        MESSAGES['browser_closed'],
        MESSAGES['driver_not_initialized']
    ]


txt = get_messages_array()
URL = "https://pochipass.com/member/"

# ------------------ 実行ディレクトリの決定（PyInstaller対応） ------------------
if getattr(sys, 'frozen', False):
    # exe化された場合（PyInstaller実行時）
    script_dir = os.path.dirname(sys.executable)
else:
    # コンソールからの実行時
    script_dir = os.path.dirname(os.path.abspath(__file__))

logfile_path = os.path.join(script_dir, 'pochiNavi.log')
config_path = os.path.join(script_dir, 'config.json')
# ロギング設定 ----------------------------------------------------------------

logger = logging.getLogger('pochiNavi')
logger.setLevel(logging.INFO)

# ログファイルハンドラの設定
file_handler = logging.handlers.RotatingFileHandler(
    logfile_path,
    maxBytes=MAX_BYTES,
    backupCount=BACKUP_COUNT,
    encoding='utf-8'
)
file_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(file_formatter)

if not logger.handlers:
    logger.addHandler(file_handler)
    if not getattr(sys, 'frozen', False):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(file_formatter)
        logger.addHandler(console_handler)

# helper関数 ----------------------------------------------------------------


def log_info(msg):
    logger.info(msg)


def log_error(msg):
    logger.error(msg)


def log_exception(msg):
    logger.exception(msg)  # スタックトレースも記録する


def get_cached_chromedriver():

    try:
        log_info("ChromeDriverの確認を開始...")

        # WebDriverManagerのデフォルトキャッシュ機能を使用
        driver_path = ChromeDriverManager().install()

        log_info(f"ChromeDriverパス: {driver_path}")
        return driver_path

    except Exception as e:
        log_error(f"ChromeDriverの取得に失敗: {e}")
        raise


log_info("--- 起動 ---")

try:
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    log_error(f"{txt[0]}: {config_path}")
    sys.exit(1)
except json.JSONDecodeError:
    log_error(f"{txt[1]}: {config_path}")
    sys.exit(1)

# キー情報を一箇所で定義
KEY_FIELDS = ["key1", "key2", "key3"]

try:
    # 設定からキー情報を辞書形式で取得
    login_keys = {field: str(config[field]) for field in KEY_FIELDS}
except KeyError as ke:
    log_error(f"{txt[5]}: {ke}")
    sys.exit(1)

# キャッシュを利用してChromeDriverを取得
chromedriver_path = get_cached_chromedriver()
service = Service(chromedriver_path)
options = webdriver.ChromeOptions()
driver = None

try:
    options.add_experimental_option("detach", True)  # スクリプト終了後もブラウザを開いたままにする呪文
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(URL)

    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    for field_id in KEY_FIELDS:
        el = wait.until(EC.element_to_be_clickable((By.ID, field_id)))
        key_value = login_keys[field_id]
        el.clear()
        el.send_keys(key_value)
        wait.until(lambda d: el.get_attribute('value') == key_value)

    login_btn = wait.until(EC.element_to_be_clickable((By.ID, "login")))
    login_btn.click()

    # ログイン後のページ遷移を待機
    try:
        wait.until(EC.presence_of_all_elements_located((By.ID, "send")))
        log_info(txt[3])
    except TimeoutException:
        log_error(txt[4])
except ValueError as ve:
    log_error(f"{txt[5]}: {ve}")
    log_exception("ValueError trace:")

except TimeoutException as te:
    log_error(f"{txt[6]}: {te}")
    log_exception("TimeoutException trace:")

except NoSuchElementException as nse:
    log_error(f"{txt[7]}: {nse}")
    log_exception("NoSuchElementException trace:")

except Exception as e:
    log_error(f"{txt[8]}: {e}")
    log_exception("Unexpected error trace:")

finally:
    if driver is not None:
        log_info(f"---{txt[9]}---")
    else:
        log_info(f"---{txt[10]}---")
