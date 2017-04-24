#Job 8:7
#Though your beginning was small, yet your latter end would greatly increase.
import sqlite3
import datetime
import pandas as pd

class CES_reader():
    def sch_db_input (self, cust_code,lotnuber,pdl,qty,fg):
        sch_con = sqlite3.connect("D:\Schedule DB\Schedule_history.db")
        sch_cusor = sch_con.cursor()
        create_q = "CREATE TABLE IF NOT EXISTS history (DATE, CUST_CODE, LOT_NUMBER_DCC, PDL, QTY, FG_NUMBER)"
        insert_q = "INSERT OR IGNORE INTO history (DATE, CUST_CODE, LOT_NUMBER_DCC, PDL, QTY, FG_NUMBER) VALUES (?,?,?,?,?,?)"
        date = datetime.date.today()
        sch_cusor.execute(create_q)
        sch_cusor.execute(insert_q,(date,cust_code,lotnuber,pdl,qty,fg))
        sch_con.commit()

    # collecting target lot number from CES file and append to data frame and data base..
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
            elif str(self.CES_df[self.lot_column].loc[n]).find("복사") != -1:
                continue
            else:
                if self.dcc_column in self.CES_df:
                    self.CES_df[self.dcc_column] = self.CES_df[self.dcc_column].fillna('')
                else:
                    pass
                # in case of no dcc column in CES
                if self.dcc_column == "no dcc" or str(self.CES_df[self.dcc_column].loc[n]) == '':
                    self.target_lots.append(str(self.CES_df[self.lot_column].loc[n]))
                    if pdl_column == "wafer":
                        self.sch_db_input(cust_code, self.CES_df[self.lot_column].loc[n], "WP", self.CES_df[quantity_column].loc[n], self.CES_df[self.current_fg_column].loc[n])
                    else:
                        self.sch_db_input(cust_code, self.CES_df[self.lot_column].loc[n], self.CES_df[pdl_column].loc[n], self.CES_df[quantity_column].loc[n], self.CES_df[self.current_fg_column].loc[n])

                else:
                    self.target_lots.append(str(self.CES_df[self.lot_column].loc[n]) + " / " + str(self.CES_df[self.dcc_column].loc[n]))
                    if pdl_column == "wafer":
                        self.sch_db_input(cust_code, (str(self.CES_df[self.lot_column].loc[n]) + " / " + str(self.CES_df[self.dcc_column].loc[n])), "WP", self.CES_df[quantity_column].loc[n], self.CES_df[self.current_fg_column].loc[n])
                    else:
                        self.sch_db_input(cust_code, (str(self.CES_df[self.lot_column].loc[n]) + " / " + str(self.CES_df[self.dcc_column].loc[n])), self.CES_df[pdl_column].loc[n], self.CES_df[quantity_column].loc[n], self.CES_df[self.current_fg_column].loc[n])
