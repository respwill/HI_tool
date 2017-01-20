import sys
sys.path.append("D:\Python")

from selenium import webdriver
import pandas as pd
from HI_tool import CES_read, emes_parsing, emes_login
import os

class sch_check(emes_parsing.parser):
    # set data frame initially: excel information and column names
    #lot_column, device_column, po_column, datecode_column, tracecode_column, coo_column, el_fg_column, be_fg_column, ship_column
    def __init__(self, book, sheet, pdl_column, lot_column, device_column, po_column, datecode_column, tracecode_column, coo_column,
                 el_fg_column, be_fg_column, ship_column):
        # set excel information include column names.
        self.book = book
        self.sheet = sheet
        self.lot_column = lot_column
        self.device_column = device_column
        self.po_column = po_column
        self.datecode_column = datecode_column
        self.tracecode_column = tracecode_column
        self.el_fg_column = el_fg_column
        self.be_fg_column = be_fg_column
        self.ship_column = ship_column
        self.coo_column = coo_column
        self.pdl_column = pdl_column

        self.current_dir = os.getcwd()

        # creating Dataframe.
        self.EMES_df = pd.DataFrame(
            columns=[lot_column, device_column, po_column, datecode_column, tracecode_column, coo_column, el_fg_column,
                     be_fg_column,
                     ship_column])
        self.result_df = pd.DataFrame(
            columns=[lot_column, device_column, po_column, datecode_column, tracecode_column, coo_column, el_fg_column,
                     be_fg_column,
                     ship_column])

        # read lot# list from target excel file.
        self.CES_df = pd.read_excel(book, sheetname=sheet)

        # make target lot number list.
        self.target_lots = []

        # set driver
        driver = webdriver.PhantomJS()

        # create 'access' instance to log in to EMES.
        login = emes_login.access(driver)
        login.connecting()

    # collecting target lot number and append to data fram and data base..
    def set_target(self):
        # collecting target lot number from BE scheduling column and ignore blank or column name.
        self.CES_df = self.CES_df.loc["Row"]
        self.CES_df.index = range(len(self.CES_df))
        for n in range(0, len(self.CES_df[self.lot_column])):
            if pd.isnull(self.CES_df[self.lot_column].loc[n]):
                break
            elif self.CES_df[self.lot_column].loc[n] == self.lot_column:
                break
            else:
                self.target_lots.append(str(self.CES_df[self.lot_column].loc[n]))
                CES_read.sch_db_input(74, self.CES_df[self.lot_column].loc[n], self.CES_df[self.pdl_column].loc[n],self.CES_df["EOH(D)"].loc[n],
                                      self.CES_df[self.el_fg_column].loc[n])

    # Compare emes and target excel file.
    def comparing(self,type):
        for n in range(0, len(self.EMES_df)):
            self.result_df[self.po_column][n] = CES_read.compare(emes_df=self.EMES_df[self.po_column][n],
                                                                 ces_df=int(self.CES_df[self.po_column][n]))
            self.result_df[self.tracecode_column][n] = CES_read.compare(emes_df=self.EMES_df[self.tracecode_column][n],
                                                                        ces_df=self.CES_df[self.tracecode_column][n])

            self.result_df[self.el_fg_column][n] = CES_read.elCompare(emes_df=self.EMES_df[self.el_fg_column][n],
                                                                   ces_df=self.CES_df[self.el_fg_column][n])

            self.result_df[self.be_fg_column][n] = CES_read.elCompare(emes_df=self.EMES_df[self.be_fg_column][n],
                                                                   ces_df=self.CES_df[self.be_fg_column][n])

            self.result_df[self.ship_column][n] = CES_read.shipCompare(emes_df=self.EMES_df[self.ship_column][n],
                                                                       ces_df=self.CES_df[self.ship_column][n],devide_char='-')
        if not "inspection result" in os.listdir(self.current_dir):
            os.mkdir("inspection result")

        writer = pd.ExcelWriter("{}/inspection result/{} insp_result.xlsx".format(self.current_dir,type), engine="xlsxwriter")
        self.result_df.to_excel(writer, sheet_name=self.sheet)
        writer.close()
        print("\nChecking for Tunrkey lots has done")

    def only_checking(self):
        for n in range(0, len(self.EMES_df)):
            self.result_df[self.po_column][n] = CES_read.compare(emes_df=self.EMES_df[self.po_column][n],
                                                                 ces_df=self.CES_df[self.po_column][n])
            self.result_df[self.tracecode_column][n] = CES_read.compare(emes_df=self.EMES_df[self.tracecode_column][n],
                                                                        ces_df=self.CES_df[self.tracecode_column][n])
            self.result_df[self.coo_column][n] = CES_read.cooCompare(emes_df=self.EMES_df[self.coo_column][n],
                                                                      ces_df=self.CES_df[self.coo_column][n])
            self.result_df[self.datecode_column][n] = CES_read.compare(emes_df=self.EMES_df[self.datecode_column][n],
                                                                       ces_df=self.CES_df[self.datecode_column][n])
            self.result_df[self.el_fg_column][n] = CES_read.elCompare(emes_df=self.EMES_df[self.el_fg_column][n],
                                                                   ces_df=self.CES_df[self.el_fg_column][n])
            self.result_df[self.be_fg_column][n] = CES_read.elCompare(emes_df=self.EMES_df[self.be_fg_column][n],
                                                                   ces_df=self.CES_df[self.be_fg_column][n])
            self.result_df[self.ship_column][n] = CES_read.shipCompare(emes_df=self.EMES_df[self.ship_column][n],
                                                                       ces_df=self.CES_df[self.ship_column][n],devide_char='-')
        if "inspection result" not in os.listdir(self.current_dir):
            os.mkdir("inspection result")

        writer = pd.ExcelWriter("{}/inspection result/Only_Lot insp_result.xlsx".format(self.current_dir), engine="xlsxwriter")
        self.result_df.to_excel(writer, sheet_name=self.sheet)
        writer.close()
        print("\nChecking for Only lots has done")

