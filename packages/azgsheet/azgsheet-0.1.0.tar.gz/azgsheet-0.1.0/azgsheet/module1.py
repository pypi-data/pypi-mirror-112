import logging
import os
import os.path
import pickle
import sys
from typing import Union, Any, List, Optional, cast
import time

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import errors
from googleapiclient.discovery import build

GSHEET_READONLY_SCOPE = 'https://www.googleapis.com/auth/spreadsheets.readonly'
GSHEET_READWRITE_SCOPE = 'https://www.googleapis.com/auth/spreadsheets'

DRIVE_READONLY_SCOPE = 'https://www.googleapis.com/auth/drive.metadata.readonly'
DRIVE_READWRITE_SCOPE = 'https://www.googleapis.com/auth/drive'

WAIT_TIME = 2 # in seconds

def __verify_token__(credentials_file: str, scope: str) -> Any:
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, scope)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def init_gsheet_service(credentials_file: str = "", scope: List[str] = [GSHEET_READONLY_SCOPE]) -> Any:
    """ Initializes the Google Sheet service to be used later by other other apis

    :param credentials_file: see https://developers.google.com/sheets/api/quickstart/python
    :param scope: List of scopes to request, like DRIVE_READONLY_SCOPE or DRIVE_READWRITE_SCOPE
    :returns: A Resource object with methods for interacting with the service
    :rtype: bool
    """
    creds = __verify_token__(credentials_file,scope)
    service = build('sheets', 'v4', credentials=creds)
    return service


def init_drive_service(credentials_file: str = "", scope: List[str] = [DRIVE_READONLY_SCOPE]) -> Any:
    """ Initializes the Google Drive service to be used later by other other apis

    :param credentials_file: see https://developers.google.com/sheets/api/quickstart/python
    :param scope: List of scopes to request, like GSHEET_READONLY_SCOPE or GSHEET_READWRITE_SCOPE
    :returns: A Resource object with methods for interacting with the service
    :rtype: bool
    """
    creds = __verify_token__(credentials_file,scope)
    service = build('drive', 'v3', credentials=creds)
    return service


def get_sheet_values(service: Any, spreadsheet_id: str, sheet_range: str) -> List[List[str]]:
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=sheet_range).execute()
    values = result.get('values', [])
    return values


def create_spreadsheet(service: Any, sheet_title: str) -> str:
    spreadsheet = {
        'properties': {
            'title': sheet_title
        }
    }
    spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                                fields='spreadsheetId').execute()
    return spreadsheet.get('spreadsheetId')


def delete_spreadsheet_content(service: Any, spreadsheet_id: str, ranges: List[str]) -> Union[None,str]:
    command = {
         "ranges": ranges
    }
    request = service.spreadsheets().values().batchClear(spreadsheetId=spreadsheet_id,body=command)
    response = request.execute()
    if response:
        return response['clearedRanges'][0]
    else:
        return None


def delete_spreadsheet(service: Any, spreadsheet_id: str) -> Union[None,str]:
    try:
        service.files().delete(fileId=spreadsheet_id).execute()
        return spreadsheet_id
    except errors.HttpError as err:
        logging.error('Unable to delete file %s with error %s' % (spreadsheet_id, err), file=sys.stderr)
        return None


# RAW vs USER_ENTERED: see https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption
def append_row(service: Any, spreadsheet_id: str, range_name: str, values: List[str], value_input_option="USER_ENTERED") -> Any:
    values = values
    body = {
        'values': values
    }
    time.sleep(WAIT_TIME)
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    print('{0} cells appended.'.format(result \
                                       .get('updates') \
                                       .get('updatedCells')))
    # [END sheets_append_values]
    return result


def get_sheets(service: Any, spreadsheet_id: str) -> List[Any]:
    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = sheet_metadata.get('sheets', '')
    return sheets
    # title = sheets[0].get("properties", {}).get("title", "Sheet1")
    # sheet_id = sheets[0].get("properties", {}).get("sheetId", 0)


def print_sheet_values(service, sheet_id, sheet_range):
    values = get_sheet_values(service, sheet_id, sheet_range)
    if not values:
        print('No data found.')
    else:
        print(len(values))
        for row in values:
            if len(row) > 1:
                print(row)
