#Job 8:7
#Though your beginning was small, yet your latter end would greatly increase.

import sys
sys.path.append("D:\Python")
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium import webdriver
from HI_tool import emes_login

class parser():
    # function for initializing.
    def parser(self, lot_list, emes_df, result_df):
        # set driver
        self.driver = webdriver.PhantomJS()
        # self.driver = webdriver.Chrome()

        # create 'access' instance to log in to EMES.
        login = emes_login.access(self.driver)
        login.connecting()

        self.lot_list = lot_list
        self.emes_df = emes_df
        self.result_df = result_df

    def quit_driver(self):
        self.driver.quit()

    # script for pin tracking / crawling fg number and marking spec number.
    def fg_info_gathering(self,driver, pin):
        driver.get("http://aak1ws01/eMES/testpdb/pinView.do?PinNo=" + pin)
        pinInfos = driver.find_elements_by_css_selector("p > a > span > font")
        point = pinInfos[0].text.find("/")
        mark_number = pinInfos[0].text[1:point - 1]
        fg = pinInfos[1].text
        return fg, mark_number

    # Making target url using target lot number and tracking
    def tracking_lot(self,target_lot):
        self.strip_target_lot = target_lot.replace(" ","")
        # if lot number has '/', before '/' is lot number and after '/' is dcc number.
        self.first_dividing = self.strip_target_lot.find("/")
        self.second_dividing = self.strip_target_lot.find("/",self.first_dividing + 1)
        self.equal = self.strip_target_lot.find('=')

        #if '=' exist the first '/' is not divider for lot number.
        if self.equal == -1:
            if self.first_dividing == -1:
                self.target_lotNumber = self.strip_target_lot
                self.target_DccNumber = ""
            else:
                self.target_lotNumber = self.strip_target_lot[:self.first_dividing]
                self.target_DccNumber = self.strip_target_lot[self.first_dividing + 1:]
        else:
            if self.second_dividing == -1:
                self.target_lotNumber = self.strip_target_lot
                self.target_DccNumber = ""
            # if sencond dividing exists..
            else:
                self.target_lotNumber = self.strip_target_lot[:self.second_dividing]
                self.target_DccNumber = self.strip_target_lot[self.second_dividing + 1:]

        self.tracking_url = "http://aak1ws01/eMES/sch/historyTestInfo.do?factoryID=1&Lot=" + str(self.target_lotNumber) + "&Dcc=" + str(self.target_DccNumber) + "&dest=TEST"
        self.driver.get(self.tracking_url)



    # tracking each lot number and crawling information from it.
    def collecting(self,target_lot):
        self.tracking_lot(target_lot)
        try:
            alert = self.driver.switch_to.alert
            print(alert.text)
            alert.accept()
        except:
            pass
        #if lot is incorrect or lot number has changed, alert shows up. needs to handle it.

        error_message = self.driver.find_element_by_css_selector('body').text
        error_text = "Error 500: java.lang.ClassCastException: com.amkor.emes.struts.forms.sch.WipHistoryTrackingTestInfoForm incompatible with com.amkor.emes.struts.forms.sch.WipHistoryTrackingForm"
        if error_message == error_text:
            self.ship_code = self.drop_flag = self.test_PO = self.custInfo = self.dateCode = self.coo = self.traceCode = self.scheduleType = self.testFloor = "wrong lot#"
            print(str(self.target_lotNumber) + " / " + str(self.target_DccNumber), "doesn't exist")
            return 0
        else:
            pass

        if self.target_DccNumber != "":
            print("Checking: ", self.target_lotNumber+" / "+self.target_DccNumber)
        else:
            print("Checking: ", self.target_lotNumber)

        # get Assy and Test target device name
        self.device = self.driver.find_elements_by_css_selector("table > tbody > tr > td > pre > font")
        self.assy_device = self.device[0].text
        self.test_device = self.device[1].text

        # get extra information
        self.point = self.driver.find_elements_by_css_selector("table > tbody > tr > td > font")
        self.ship_code = (self.point[23].text)[0:4]
        self.drop_flag = (self.point[23].text)[6:]
        self.test_PO = self.point[38].text
        self.custInfo = self.point[40].text
        self.dateCode = self.point[42].text
        self.coo = self.point[44].text[0:13]
        self.traceCode = self.point[46].text
        self.scheduleType = self.point[82].text
        self.testFloor = self.point[92].text

        # Clicking 'sub pin info' button on lot trakcing page.
        # It will show 2nd window. move to the 2nd window and get pin number.
        pin_list = self.driver.find_element_by_partial_link_text("Sub Pin Info")
        pin_list.click()

        self.driver.switch_to.window(self.driver.window_handles[1])
        self.current_pin = self.driver.find_elements_by_css_selector("tbody > tr > td")[6].text
        # self.previous_pin = self.driver.find_elements_by_css_selector("tbody > tr > td")[8]
        self.pre_split_pin = self.driver.find_elements_by_css_selector("tbody > tr > td")[10].text
        self.t_stock_pin = self.driver.find_elements_by_css_selector("tbody > tr > td")[12].text

        # self.previous_fg =""
        # self.previous_fg_marking =""

        # if pin information is blank, set fg, and marking information as blank
        if self.current_pin == "":
            self.current_fg = ""
            self.current_fg_marking = ""
        else:
            self.current_fg, self.current_fg_marking = self.fg_info_gathering(self.driver, self.current_pin)

        if self.pre_split_pin == "":
            self.pre_split_fg = ""
            self.pre_split_fg_marking = ""
        else:
            self.pre_split_fg, self.pre_split_fg_marking =self.fg_info_gathering(self.driver, self.pre_split_pin)

        if self.t_stock_pin == "":
            self.t_stock_fg = ""
            self.t_stock_fg_marking = ""
        else:
            self.t_stock_fg, self.t_stock_fg_marking =  self.fg_info_gathering(self.driver, self.t_stock_pin)

        # close 2nd window and go back to 1st window.
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    # get list of items that user want to inpect as parameter and return emes information to emes_df and result_df.
    def get_info(self,inspect_item_list):
        for target_lot in self.lot_list:
            self.collecting(target_lot)
            info_dic = {'assy_device':self.assy_device, 'test_device':self.test_device, 'ship_code':self.ship_code,'drop_flag':self.drop_flag,
                        'test_po':self.test_PO, 'cust_info':self.custInfo, 'date_code':self.dateCode, 'coo':self.coo, 'trace_code':self.traceCode,
                        'schedule_type':self.scheduleType, 'test_floor':self.testFloor,
                        'current_fg':self.current_fg, 'pre_split_fg':self.pre_split_fg, 't_stock_fg':self.t_stock_fg, 'current_fg_marking':self.current_fg_marking}
            collected_info = []
            collected_info.append(target_lot)
            for info in inspect_item_list:
                 collected_info.append(info_dic[info])
            self.emes_df.loc[len(self.emes_df)] = collected_info
            # some columns doesn't need to be inspected but needs to show emes information.
            self.result_df.loc[len(self.result_df)] = collected_info