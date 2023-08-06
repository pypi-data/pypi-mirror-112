
import gspread

ERR_MSG_SHEET = """
ERROR: Could not find sheet named '{0}'. Make sure it exists
"""

ERR_MSG_SPREADSHEET = """
ERROR: Could not find spreadsheet named '{0}'.
Make sure:
* it exists
* you have added your service account email as the document editor in the document sharing settings
"""

class Spreadsheet(object):
    def __init__(self, gspreadClient):
        self.client = gspreadClient
        self.document = None
    def open(self, spreadsheetKey):
        try:
            self.document = self.client.open_by_key(spreadsheetKey)
        except gspread.exceptions.SpreadsheetNotFound:
            print(ERR_MSG_SPREADSHEET.format(spreadsheetKey))
            raise
    def sheet(self, sheetName):
        try:
            return self.document.worksheet(sheetName)
        except:
            print(ERR_MSG_SHEET.format(sheetName))
            raise

