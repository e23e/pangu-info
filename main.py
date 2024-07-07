from helpers.nse_helper import NSE_Helper
from helpers.db_helper import DB_Helper




class Main:
    def __init__(self) -> None:
        self.nse_helper = NSE_Helper()
        self.db_helper = DB_Helper()

    def main(self):
        stocks_info = self.nse_helper.list_all_symbols()
        self.db_helper.insert_stocks_info(data=stocks_info)
        

if __name__=="__main__":
    obj = Main()
    obj.main()
