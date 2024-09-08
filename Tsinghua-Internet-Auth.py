import sys
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common import exceptions
import json, argparse, os, loguru
from AESCipher import AESCipher

def login(url, username, password):
    loguru.logger.debug(f'Start auth: \n- url: {url}')
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('window-size=1920x1080')
    options.add_argument('--start-maximized')
    options.add_argument('--ignore-certificate-errors')
    session = Chrome(options=options)
    loguru.logger.debug('Open browser successfully')
    try:
        session.implicitly_wait(3)
        session.get(url)
        session.find_element(By.ID, "username").send_keys(username)
        session.find_element(By.ID, "password").send_keys(password)
        if "auth4" in session.current_url and not "tauth4" in session.current_url:
            session.find_element(By.ID, "connect").click()
            session.find_element(By.ID, "disconnect")
        else:
            session.find_element(By.ID, "login-account").click()
            session.find_element(By.ID, "logout")
        loguru.logger.debug('Login successfully')
    except exceptions.NoSuchElementException:
        raise Exception('Login failed')
    

def parse_args():
    loguru.logger.add('auth.log', rotation='1 week', retention='7 days', level='DEBUG')
    if not os.path.isfile('config.json') or len(sys.argv) > 1:
        try:
            parser = argparse.ArgumentParser()
            parser.add_argument('--url', '-l', help='URL to connect to')
            parser.add_argument('--username', '-u', help='Username')
            parser.add_argument('--password', '-p', help='Password')
            args = parser.parse_args()
            loguru.logger.debug(f'Using new config: \n- url: {args.url}')        
            with open('config.json', 'w', encoding='utf-8') as f:
                cipher = AESCipher('Tsinghua-Internet-Auth'.encode('utf-8'))
                json.dump({'url': args.url, 'username': cipher.encrypt_from_str_to_base64(args.username), 'password': cipher.encrypt_from_str_to_base64(args.password)}, f, ensure_ascii=False, indent=4)
        except:
            if os.path.isfile('config.json'):
                os.remove('config.json')
            parser.print_help()
            return {}
    config = {}
    with open('config.json', 'r', encoding='utf-8') as f:
        cipher = AESCipher('Tsinghua-Internet-Auth'.encode('utf-8'))
        config = json.load(f)
        config = {k: cipher.decrypt_from_base64_to_str(v) for k, v in config.items() if k != 'url'} | {'url': config['url']}
    loguru.logger.debug(f'Loaded config: \n- url: {config["url"]}')
    return config


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    config = parse_args()
    if config == {}:
        os.system('pause')
        sys.exit(0)
    try:
        login(config['url'], config['username'], config['password'])
    except Exception as e:
        loguru.logger.error(f'Error: {e}')
        os.system('pause')


if __name__ == '__main__':
    main()
