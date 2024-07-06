import datetime
import os.path

from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from twilio.rest import Client

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def get_scheduled_events(service):
  # Get the current date in UTC
  utc_today = datetime.datetime.now(datetime.timezone.utc).date()

  # Get UTC of today midnight
  today_midnight = utc_today + datetime.timedelta(days=1)
  today_midnight = datetime.datetime.combine(today_midnight, datetime.time(0, 0), datetime.timezone.utc)
  # Get UTC of yesterday midnight
  yesterday_midnight = datetime.datetime.combine(utc_today, datetime.time(0, 0), datetime.timezone.utc)

  yesterday_midnight = yesterday_midnight.isoformat()
  today_midnight = today_midnight.isoformat()

  events_result = (
    service.events()
    .list(
        calendarId="primary",
        timeMin=yesterday_midnight,
        timeMax=today_midnight,
        singleEvents=True,
        orderBy="startTime",
    )
    .execute()
  )
  events = events_result.get("items", [])
  return events


def send_text(events):
  account_sid = os.environ["TWILIO_ACCOUT_SID"]
  auth_token = os.environ['TWILIO_AUTH_TOKEN']
  client = Client(account_sid, auth_token)

  message = "GoodMorning! Your scheduled events tonight:\n"
  
  if not events:
    message += "No Scheduled events today"

  for event in events:

    start = datetime.datetime.fromisoformat(event["start"].get("dateTime", event["start"].get("date")))
    end = datetime.datetime.fromisoformat(event["end"].get("dateTime", event["end"].get("date")))
    message += f" {start.hour}:{start.minute:02d}-{end.hour}:{end.minute:02d}: "
    message += event["summary"] + '\n'

  message = client.messages.create(
    from_=os.environ['TWILIO_NUMBER'],
    to=os.environ['PHONE_NUMBER'],
    body=message
  )




def main():
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
    service = build("calendar", "v3", credentials=creds)
    events = get_scheduled_events(service)
    send_text(events)

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()