from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import yaml

# initialize the browser
br = webdriver.Chrome()
wait = WebDriverWait(br, 35)

# Load settings from yaml file
with open('./sys_settings.yaml') as f:
    sys_settings = yaml.load(f.read(), Loader=yaml.FullLoader)
    print("system settings loaded")

with open('./settings.yaml', 'r', encoding='utf-8') as f:
    settings = yaml.load(f.read(), Loader=yaml.FullLoader)
    print("user system loaded")
    print("--" * 20)
    for setting in settings:
        print(setting)
    print("--" * 20)


class Khan:
    def __init__(self):
        if self.login():
            print("login success")
            self.get_course_list()
        else:
            print("login failed")
            br.quit()

    @staticmethod
    def login():
        br.get(settings["base_url"] + 'login')
        time.sleep(3)
        try:
            wait.until(EC.element_to_be_clickable((By.ID, sys_settings['loginID'])))
            br.find_element(By.ID, sys_settings['loginID']).send_keys(settings["username"])
            password = br.find_element(By.ID, sys_settings['passwordID'])
            password.send_keys(settings["password"])
            # Login
            password.send_keys(Keys.RETURN)
            time.sleep(10)
            return True
        except Exception as e:
            print(e)
            return False


    def get_course_list(self):
        print("course_list")
        for url in settings["assignment"]:
            print(settings['base_url'] + url)
            br.get(settings['base_url'] + url)
            time.sleep(10)
            while True:
                # 等待表格加载完成
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_5kaapu")))
                btns = br.find_elements(By.CLASS_NAME,sys_settings['assignment_btn'])

                # 当前页面视频总数
                for i in btns:
                    # 点击视频
                    btn = br.find_element(By.CLASS_NAME, sys_settings['assignment_btn'])
                    btn.click()
                    time.sleep(10)

                    # 退出视频
                    # 等待10*60秒
                    exitTime = WebDriverWait(br, 15*60)

                    exitTime.until(EC.presence_of_element_located((By.CLASS_NAME, sys_settings["end_btn"])))
                    time.sleep(5)
                    print("--finish one video")
                    br.find_element(By.CLASS_NAME, sys_settings['exit_btn']).click()
                    time.sleep(5)

                print("finish one page")

                # 翻页
                next_btn = br.find_element(By.XPATH, sys_settings['next_btn'])
                # 如果没有下一页，则退出
                if next_btn.get_attribute('class') == sys_settings['next_btn']:
                    print("no more page")
                    break
                else:
                    # 点击下一页
                    next_btn.click()
                    time.sleep(10)

            print("finish one course")


if __name__ == '__main__':
    Khan()
    br.close()
