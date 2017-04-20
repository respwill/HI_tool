#Job 8:7
#Though your beginning was small, yet your latter end would greatly increase.

import sys
sys.path.append("D:\Python")
import pandas as pd
import numpy
import math
from HI_tool import CES_read, emes_parsing
import os

class sch_check(emes_parsing.parser, CES_read.CES_reader):
    # set data frame initially: excel information and column names
    #lot_column, device_column, po_column, datecode_column, tracecode_column, coo_column, el_fg_column, be_fg_column, ship_column
    def __init__(self, book, sheet, lot_column, dcc_column="no dcc", device_column="optional",  po_column="optional", datecode_column="optional",custInfo_column="optional",
                 tracecode_column="optional", coo_column="optional", ship_column="optional", current_fg_column="optional", pre_split_fg_column="optional",
                 tstock_fg_column="optional", marking_spec_column="optional", dropFlag_column="optional", probeFlag_column="optional"):
        # set excel information include column names.
        self.current_dir = os.getcwd()
        self.book = book
        self.sheet = sheet
        self.lot_column = lot_column
        self.dcc_column = dcc_column
        self.device_column = device_column
        self.po_column = po_column
        self.datecode_column = datecode_column
        self.custInfo_column = custInfo_column
        self.tracecode_column = tracecode_column
        self.coo_column = coo_column
        self.current_fg_column = current_fg_column
        self.pre_split_fg_column = pre_split_fg_column
        self.tstock_fg_column = tstock_fg_column
        self.ship_column = ship_column
        self.marking_spec_column = marking_spec_column
        self.drop_flag_column = dropFlag_column
        self.probe_flag_column = probeFlag_column

        # procedure for set columns list for DataFrame.
        # If input is blank, it will be ignored.
        collection = []
        collection = lot_column, dcc_column, device_column, po_column, datecode_column, custInfo_column, tracecode_column, coo_column, ship_column, current_fg_column, pre_split_fg_column, tstock_fg_column, marking_spec_column, dropFlag_column, probeFlag_column
        self.sorted_collection = []
        for column in collection:
            if column == "optional" or column == "no dcc":
                pass
            else:
                self.sorted_collection.append(column)

        # creating Dataframe using information that we got above / igonore column that has 'optional'
        self.EMES_df = pd.DataFrame(columns=self.sorted_collection)
        self.result_df = pd.DataFrame(columns=self.sorted_collection)

        # read sheet from target excel file.
        self.CES_df = pd.read_excel(book, sheetname=sheet)

        # make target lot number list.
        self.target_lots = []

    # collecting target lot number from CES file and append to data frame and data base..
    # ces_df's information is right one.
    def compare(self, emes_df, ces_df):
        if type(ces_df) == numpy.float64:
            print(ces_df)
            if emes_df == str(int(ces_df)):
                return "OK"
            elif emes_df == "" or emes_df == "/":
                if ces_df == "" or math.isnan(ces_df) == True:
                    return ""
                else:
                    return emes_df + " change it to " + str(int(ces_df))
            elif emes_df == "Pre-schedule didn't performed":
                return "Pre-schedule didn't performed"
            elif emes_df == "lot doesn't exist":
                return "lot doesn't exist"
            else:
                return emes_df + " change it to " + str(int(ces_df))
        else:
            if emes_df == str(ces_df):
                return "OK"
            elif emes_df == "" or emes_df == "/":
                if ces_df == "" or math.isnan(ces_df) == True :
                    return ""
                else:
                    return emes_df + " change it to " + str(int(ces_df))
            elif emes_df == "Pre-schedule didn't performed":
                return "Pre-schedule didn't performed"
            elif emes_df == "lot doesn't exist":
                return "lot doesn't exist"
            else:
                return emes_df + " change it to " + str(ces_df)

    def fgCompare(self, emes_df, ces_df):
        if len(str(ces_df)) == 10:
            if str(emes_df)[1:11] == str(ces_df):
                return "OK"
            elif emes_df == "Pre-schedule didn't performed":
                return "Pre-schedule didn't performed"
            elif emes_df == "lot doesn't exist":
                return "lot doesn't exist"
            else:
                return str(emes_df)[1:11] + " change it to " + str(ces_df)
        elif str(ces_df) == "No Bin2 split":
            return ""
        else:
            if str(emes_df)[1:11] == str(ces_df)[0:10]:
                return "OK"
            elif emes_df == "Pre-schedule didn't performed":
                return "Pre-schedule didn't performed"
            elif emes_df == "lot doesn't exist":
                return "lot doesn't exist"
            else:
                return str(emes_df)[1:11] + " change it to " + str(ces_df)[0:10]

    def markCompare(self, emes_df, ces_df):
        if emes_df == str(ces_df):
            return "OK"
        elif str(ces_df) == "No marking":
            if emes_df == "":
                return "OK"
            else:
                return "incorrect FG:"
        else:
            return "incorrect FG"

    def cooCompare(self, emes_df, ces_df):
        if ces_df == "PH":
            if emes_df == "D(PHILIPPINE)":
                return "OK"
            else:
                return "incorrect coo"
        elif ces_df == "TW":
            if emes_df == "G(TAIWAN )":
                return "OK"
            else:
                return "incorrect coo"
        else:
            return "Please revise cooCompare in CES_read.py"

    def shipCompare(self, emes_df, ces_df):
        # devider in emes is '-'
        if type(ces_df) == float:
            return ""
        else:
            if ces_df.find("/") != -1:
                checker = ces_df.find("/")
                trim_emes_df = str(emes_df).replace(' ', '')
                if str(ces_df)[:1] == "0":
                    if trim_emes_df == str(ces_df)[1:checker] + "-" + str(ces_df)[checker + 1:]:
                        return "OK"
                    elif emes_df == "wrong lot#":
                        return "wrong lot#"
                    else:
                        return trim_emes_df + " change it to " + str(ces_df)[1:checker] + "-" + str(ces_df)[
                                                                                                checker + 1:]
                else:
                    if trim_emes_df == str(ces_df)[:checker] + "-" + str(ces_df)[checker + 1:]:
                        return "OK"
                    elif emes_df == "wrong lot#":
                        return "wrong lot#"
                    else:
                        return trim_emes_df + " change it to " + str(ces_df)[:checker] + "-" + str(ces_df)[checker + 1:]
            elif ces_df.find("-") != -1:
                checker = ces_df.find("-")
                trim_emes_df = str(emes_df).replace(' ', '')
                if str(ces_df)[:1] == "0":
                    if trim_emes_df == str(ces_df)[1:checker] + "-" + str(ces_df)[checker + 1:]:
                        return "OK"
                    elif emes_df == "wrong lot#":
                        return "wrong lot#"
                    else:
                        return trim_emes_df + " change it to " + str(ces_df)[1:checker] + "-" + str(ces_df)[
                                                                                                checker + 1:]
                else:
                    if trim_emes_df == str(ces_df)[:checker] + "-" + str(ces_df)[checker + 1:]:
                        return "OK"
                    elif emes_df == "wrong lot#":
                        return "wrong lot#"
                    else:
                        return trim_emes_df + " change it to " + str(ces_df)[:checker] + "-" + str(ces_df)[checker + 1:]
            else:
                print("please use '/' or '-' to divide country code and local code in shipping code in CES file")

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
                    self.result_df[column_name][n] = self.fgCompare(emes_df=self.EMES_df[column_name][n], ces_df=self.CES_df[column_name][n])
                elif check_column_name.find("ship") != -1:
                    self.result_df[column_name][n] = self.shipCompare(emes_df=self.EMES_df[column_name][n], ces_df=self.CES_df[column_name][n])
                elif check_column_name.find("coo") != -1:
                    self.result_df[column_name][n] = self.cooCompare(emes_df=self.EMES_df[column_name][n], ces_df=self.CES_df[column_name][n])
                elif check_column_name.find("po") != -1:
                    try:
                        self.result_df[column_name][n] = self.compare(emes_df=self.EMES_df[column_name][n], ces_df=int(self.CES_df[column_name][n]))
                    except:
                        self.result_df[column_name][n] = self.compare(emes_df=self.EMES_df[column_name][n], ces_df=self.CES_df[column_name][n])
                elif check_column_name.find("device") != -1:
                    pass
                elif check_column_name.find("dcc") != -1:
                    pass
                elif check_column_name.find("lot") != -1:
                    pass
                else:
                    self.result_df[column_name][n] = self.compare(emes_df=self.EMES_df[column_name][n], ces_df=(self.CES_df[column_name][n]))

        if not "inspection result" in os.listdir(self.current_dir):
            os.mkdir("inspection result")

        writer = pd.ExcelWriter("{}/inspection result/{} insp_result.xlsx".format(self.current_dir,type), engine="xlsxwriter")
        self.result_df.to_excel(writer, sheet_name=self.sheet)
        writer.close()
        print("Checking for {} has done\n".format(type))



