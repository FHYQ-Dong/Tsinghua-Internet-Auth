import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common import exceptions
import json, argparse, os, loguru

def main(url, username, password):
    loguru.logger.debug(f'Start auth: \n- url: {url}')
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('window-size=1920x1080')
    options.add_argument('--start-maximized')
    options.add_argument('--ignore-certificate-errors')
    session = webdriver.Edge(options=options)
    loguru.logger.debug('Open browser successfully')
    # 等待页面加载
    try:
        session.implicitly_wait(3)
        session.get(url)
        session.find_element(By.ID, "username").send_keys(username)
        session.find_element(By.ID, "password").send_keys(password)
        session.find_element(By.ID, "login-account").click()
        session.find_element(By.ID, "logout")
        loguru.logger.debug('Login successfully')
    except exceptions.NoSuchElementException:
        loguru.logger.error('Login failed')
        raise Exception('Login failed')
    

if __name__ == '__main__':
    loguru.logger.add('auth.log', rotation='1 week', retention='7 days', level='DEBUG')
    if not os.path.isfile('config.json') or len(sys.argv) > 1:
        try:
            loguru.logger.debug('Using new config')
            parser = argparse.ArgumentParser()
            parser.add_argument('--url', '-l', help='URL to connect to')
            parser.add_argument('username', '-u', help='Username')
            parser.add_argument('password', '-p', help='Password')
            args = parser.parse_args()
            loguru.logger.debug(f'New config: \n- url: {args.url}')        
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(vars(args), f, indent=4, ensure_ascii=False)
        except:
            parser.print_help()
    config = {}
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    loguru.logger.debug(f'Loaded config: \n- url: {config["url"]}')
    try:
        main(config['url'], config['username'], config['password'])
    except Exception as e:
        print(e)
        os.system('pause')
