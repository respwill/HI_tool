#Job 8:7
#Though your beginning was small, yet your latter end would greatly increase.
import sqlite3
import datetime

# ces_df's information is right one.
def compare(emes_df,ces_df):
    if emes_df == str(ces_df):
        return "OK"
    elif emes_df == "" or emes_df == "/":
        return "No lot"
    else:
        return emes_df + " change it to " + str(ces_df)

def elCompare(emes_df,ces_df):
    if len(str(ces_df)) == 10:
        if str(emes_df)[1:11] == str(ces_df):
            return "OK"
        elif emes_df == "wrong lot#":
            return "wrong lot#"
        else:
            return str(emes_df)[1:11] + " change it to " + str(ces_df)
    else:
        if str(emes_df)[1:11] == str(ces_df)[0:10]:
            return "OK"
        elif emes_df == "wrong lot#":
            return "wrong lot#"
        else:
            return str(emes_df)[1:11] + " change it to " + str(ces_df)[0:10]

def markCompare(emes_df,ces_df):
    if emes_df == str(ces_df):
        return "OK"
    elif str(ces_df) == "No marking":
        if emes_df == "":
            return "OK"
        else:
            return "incorrect FG:"
    else:
        return "incorrect FG"

def cooCompare(emes_df,ces_df):
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


def shipCompare(emes_df,ces_df,devide_char):
    checker = emes_df.find(devide_char)
    if str(ces_df)[:1] == "0":
        if str(emes_df)[:checker]+devide_char+str(emes_df)[checker+1:checker+2] == str(ces_df)[1:]:
            return "OK"
        elif emes_df == "wrong lot#":
            return "wrong lot#"
        else:
            return str(emes_df)[:checker]+devide_char+str(emes_df)[checker+1:checker+2] + " change it to " + str(ces_df)[1:]
    else:
        if str(emes_df)[:checker]+devide_char+str(emes_df)[checker+1:checker+2] == str(ces_df):
            return "OK"
        elif emes_df == "wrong lot#":
            return "wrong lot#"
        else:
            return str(emes_df)[:checker]+devide_char+str(emes_df)[checker+1:checker+2] + " change it to " + str(ces_df)


def sch_db_input (cust_code,lotnuber,pdl,qty,fg):
    sch_con = sqlite3.connect("D:\Schedule DB\Schedule_history.db")
    sch_cusor = sch_con.cursor()
    create_q = "CREATE TABLE IF NOT EXISTS history (DATE, CUST_CODE, LOT_NUMBER_DCC, PDL, QTY, FG_NUMBER)"
    insert_q = "INSERT OR IGNORE INTO history (DATE, CUST_CODE, LOT_NUMBER_DCC, PDL, QTY, FG_NUMBER) VALUES (?,?,?,?,?,?)"
    date = datetime.date.today()
    sch_cusor.execute(create_q)
    sch_cusor.execute(insert_q,(date,cust_code,lotnuber,pdl,qty,fg))
    sch_con.commit()


