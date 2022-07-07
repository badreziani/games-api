from googleapiclient.discovery import build
from google.oauth2 import service_account


def get_sheet_data():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    SERVICE_ACCOUNT_FILE = './keys.json'

    credentials = None
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # # The ID of spreadsheet.
    SAMPLE_SPREADSHEET_ID = '19gv9W9qflPPFGjpnktK2D8jxPw8n5C5uFGz_Z32FNM8'

    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="games!A1:AD2089").execute()
    rows = result.get('values', [])[1:]

    return rows
