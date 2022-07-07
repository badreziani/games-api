from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# # The ID of spreadsheet.
# SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
# fetcher@gamesapi-355613.iam.gserviceaccount.com
# creds = None
# service = build('sheets', 'v4', credentials=creds)

# # Call the Sheets API
# sheet = service.spreadsheets()
# result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
#                             range=SAMPLE_RANGE_NAME).execute()
# values = result.get('values', [])

# if not values:
#     print('No data found.')
#     return

# print('Name, Major:')
# for row in values:
#     # Print columns A and E, which correspond to indices 0 and 4.
#     print('%s, %s' % (row[0], row[4]))
   

