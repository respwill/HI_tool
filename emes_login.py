#Job 8:7
#Though your beginning was small, yet your latter end would greatly increase.
import sqlite3

class access ():
# getting user information / need to change by each user
    def __init__(self,driver):
        self.con = sqlite3.connect("D:\Password DB\password.db")
        self.cursor = self.con.cursor()
        self.user = self.cursor.execute("SELECT user FROM USER_INFO WHERE system = 'eMES'").fetchone()[0]
        self.pswd = self.cursor.execute("SELECT pswd FROM USER_INFO WHERE system = 'eMES'").fetchone()[0]
        self.badge = self.cursor.execute("SELECT badge FROM USER_INFO WHERE system = 'eMES'").fetchone()[0]
        self.driver = driver

    def connecting(self):
        try:
            self.driver.get("http://aak1ws01/eMES/user/login.do?user="+self.user+"&password="+self.pswd+"&badge="+self.badge)
        except:
            invalidPswd = self.driver.find_element_by_css_selector("tbody > tr > td > center > font")
            if invalidPswd.text == "Invalid Username or Password !!!":
                print("경고: password.db 상 비밀번호 변경 필요합니다 / 변경없이 반복 실행시 계정이 잠길 수 있습니다.")
                input("프로그램 종료하고 갱신 해주세요.")
                sys.exit()
            elif invalidPswd.text == "Invalid Badge number.":
                print("경고: password.db 상 badge# 변경 필요합니다 / 변경없이 반복 실행시 계정이 잠길 수 있습니다.")
                input("프로그램 종료하고 갱신 해주세요.")
                sys.exit()
            else:
                print("예상못한 프로그램 오류")
                input("프로그램을 종료합니다.")
                sys.exit()

