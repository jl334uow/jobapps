import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
import base64

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def list_emails_start_of_month(service):
  # Calculate current month
  first_date = datetime.date.today().replace(day=1).strftime('%Y/%m/%d')
  # Currently only supporting SEEK emails
  seek_query = f'from:noreply@s.seek.com.au subject:Your application was successfully submitted after:{first_date}'
  # Retreive full message payload
  result = service.users().messages().list(userId = 'me', q = seek_query).execute()
  payload = result.get('messages', [])

  return payload

def filter_body(payload):
  if payload.get('mimeType') == 'text/html':
    return payload.get('body', {}).get('data')

  if 'parts' in payload:
    for sub_part in payload['parts']:
      html_data = filter_body(sub_part)
      if html_data:
        return html_data
  return None

def decode_html(b64_html):
  decoded_bytes = base64.urlsafe_b64decode(b64_html.encode('ASCII'))
  return decoded_bytes.decode('utf-8')

def main():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:

    # Retreive list of emails, get content for each email, and decode into HTML
    service = build("gmail", "v1", credentials=creds)

    payload = list_emails_start_of_month(service)

    if not payload:
        print("No messages found.")
        return

    html_documents = []

    for email in payload:
      email_id = email['id']

      full_email = service.users().messages().get(userId='me', id = email_id, format = 'full').execute()

      b64_html = filter_body(full_email.get('payload', {}))

      if b64_html:
        html_content = decode_html(b64_html)

        html_documents.append({
          'id': email_id,
          'html': html_content
        })

        print(f'Retrieved HTML for email id: {email_id}')

      else:
        print(f'Email {email_id} did not contain a text/html part')


  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()