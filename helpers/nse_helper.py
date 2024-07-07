import requests
import csv
from utils.logger import get_logger
from io import StringIO

REQUEST_HEADERS  = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
}



class NSE_Helper:
    def __init__(self) -> None:
        self.logger = get_logger()
        self.nse_home_url = "http://nseindia.com"
        self.nsearchives_url = "https://nsearchives.nseindia.com"
        self.session = requests.session()
        self._update_session()
    
    def _update_session(self):
        self.session.get(self.nse_home_url, headers=REQUEST_HEADERS)
    
    def _convert_csv_data_to_dict(self, content: str) -> list[dict]:
        csv_reader = csv.DictReader(StringIO(content))
        results = []
        for row in csv_reader:
            normalized_value = self._data_normalizer(data=row)
            results.append(normalized_value)
        return results

    def _data_normalizer(self, data: dict) -> dict:
        new_format_data = {
            "symbol" : data.get("SYMBOL"),
            "company_name" : data.get("NAME OF COMPANY"),
            "exchange" : "nse",
            "isin_number" : data.get(" ISIN NUMBER"),
            "date_of_listing" : data.get(" DATE OF LISTING"),
            "face_value" : data.get(" FACE VALUE"),
            "type" : data.get(" SERIES")
        }
        return new_format_data
    
    def list_all_symbols(self) -> list:
        # https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv
        url = f"{self.nsearchives_url}/content/equities/EQUITY_L.csv"
        res = self.session.get(url=url, headers=REQUEST_HEADERS)
        if res.status_code != 200:
            self.logger.error(f"Status code is non 200!, url: {url}, status code: {res.status_code}, content: {res.text}")
            exit(1)
        return self._convert_csv_data_to_dict(content=res.text)
        
