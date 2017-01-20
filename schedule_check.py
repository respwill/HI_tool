#Job 8:7
#Though your beginning was small, yet your latter end would greatly increase.

import sys
sys.path.append("D:\Python")
import pandas as pd
from HI_tool import CES_read, emes_parsing
import os

class sch_check(emes_parsing.parser):
    # set data frame initially: excel information and column names
    #lot_column, device_column, po_column, datecode_column, tracecode_column, coo_column, el_fg_column, be_fg_column, ship_column
    def __init__(self, book, sheet, lot_column, device_column, po_column="optional", datecode_column="optional", tracecode_column="optional", coo_column="optional", ship_column="optional",
                 el_fg_column="optional", pre_split_fg_column="optional", be_fg_column="optional", marking_spec_column="optional"):
        # set excel information include column names.
        self.current_dir = os.getcwd()
        self.book = book
        self.sheet = sheet
        self.lot_column = lot_column
        self.device_column = device_column
        self.po_column = po_column
        self.datecode_column = datecode_column
        self.tracecode_column = tracecode_column
        self.coo_column = coo_column
        self.el_fg_column = el_fg_column
        self.pre_split_fg_column = pre_split_fg_column
        self.be_fg_column = be_fg_column
        self.ship_column = ship_column
        self.marking_spec_column = marking_spec_column

        # procedure for set columns list for DataFrame.
        # If input is blank, it will be ignored.
        collection = []
        collection = lot_column, device_column, po_column, datecode_column, tracecode_column, coo_column, ship_column, el_fg_column, pre_split_fg_column, be_fg_column, marking_spec_column
        self.sorted_collection = []
        for column in collection:
            if column == "optional":
                pass
            else:
                self.sorted_collection.append(column)

        # creating Dataframe using information that we got above.
        self.EMES_df = pd.DataFrame(columns=self.sorted_collection)
        self.result_df = pd.DataFrame(columns=self.sorted_collection)

        # read sheet from target excel file.
        self.CES_df = pd.read_excel(book, sheetname=sheet)

        # make target lot number list.
        self.target_lots = []

    # collecting target lot number and append to data frame and data base..
    def set_target(self, cust_code, pdl_column, quantity_column):
        # collecting target lot number from BE scheduling sheet which index is 'Row'
        self.CES_df = self.CES_df.loc["Row"]
        # set index as number from 0 to data frame length size.
        self.CES_df.index = range(len(self.CES_df))
        # ignoring blank, field column and get target lot numbers
        for n in range(0, len(self.CES_df[self.lot_column])):
            if pd.isnull(self.CES_df[self.lot_column].loc[n]):
                continue
            elif self.CES_df[self.lot_column].loc[n] == self.lot_column:
                continue
            else:
                self.target_lots.append(str(self.CES_df[self.lot_column].loc[n]))
                if pdl_column == "wafer":
                    CES_read.sch_db_input(cust_code, self.CES_df[self.lot_column].loc[n], "WP", self.CES_df[quantity_column].loc[n], self.CES_df[self.el_fg_column].loc[n])
                else:
                    CES_read.sch_db_input(cust_code, self.CES_df[self.lot_column].loc[n], self.CES_df[pdl_column].loc[n], self.CES_df[quantity_column].loc[n], self.CES_df[self.el_fg_column].loc[n])

    # Compare emes and target excel file.
    def comparing(self,type):
        for n in range(0, len(self.EMES_df)):
            # columns list could be used here
            # CES file's field names should be normalized..
            # make field names lower_case.
            # use different method depending on column name.
            for column_name in list(self.EMES_df):
                # to avoid confusion and provide chance to set CES file field name freely, use lower method.
                # it will normalize field names.
                check_column_name = column_name.lower()
                if check_column_name.find("fg") != -1:
                    self.result_df[column_name][n] = CES_read.fgCompare(emes_df=self.EMES_df[column_name][n], ces_df=self.CES_df[column_name][n])
                elif check_column_name.find("ship") != -1:
                    self.result_df[column_name][n] = CES_read.shipCompare(emes_df=self.EMES_df[column_name][n], ces_df=self.CES_df[column_name][n], devide_char='-')
                elif check_column_name.find("coo") != -1:
                    self.result_df[column_name][n] = CES_read.cooCompare(emes_df=self.EMES_df[column_name][n], ces_df=self.CES_df[column_name][n])
                elif check_column_name.find("po") != -1:
                    try:
                        self.result_df[column_name][n] = CES_read.compare(emes_df=self.EMES_df[column_name][n], ces_df=int(self.CES_df[column_name][n]))
                    except:
                        self.result_df[column_name][n] = CES_read.compare(emes_df=self.EMES_df[column_name][n], ces_df=self.CES_df[column_name][n])
                elif check_column_name.find("device") != -1:
                    pass
                elif check_column_name.find("lot") != -1:
                    pass
                else:
                    self.result_df[column_name][n] = CES_read.compare(emes_df=self.EMES_df[column_name][n], ces_df=(self.CES_df[column_name][n]))

        if not "inspection result" in os.listdir(self.current_dir):
            os.mkdir("inspection result")

        writer = pd.ExcelWriter("{}/inspection result/{} insp_result.xlsx".format(self.current_dir,type), engine="xlsxwriter")
        self.result_df.to_excel(writer, sheet_name=self.sheet)
        writer.close()
        print("\nChecking for {} has done".format(type))



