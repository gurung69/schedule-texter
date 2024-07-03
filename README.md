# Schedule Texter

## Description
Python script that fetches scheduled events for the day from Google Calender and sends summary of all the events via SMS text using Twilio API.

## Prerequisites
- Python 3.6 or higher
- Google calender credentails (stored as credentials.json)
- Twilio credentials (Account SID, Auth Token, Twilio Phone Number)

## Running locally

1. **Clone the repository:**
```sh
git clone git@github.com:gurung69/schedule-texter.git
cd schedule-texter
```
2. **Install required Packages**
```
pip install -r requirements.txt
```
3. **Setup Google Calender Credentials**
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project or select existing one
- Enable Google Calender API
- Configure OAuth consent Screen
- Authorize credentials for desktop applicaiton and download the json as "credentails.json"
- Place the credentails file in the root directory of the project

4. **Setup Twilio**
- Sign up for a [Twilio account](https://twilio.com/)
- Get Account SID, Auth Token and Twilio phone number
5. **Create .env file**
```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_NUMBER=your_twilio_number
PHONE_NUMBER=your_phone_number
```
6. **Run the script**
```sh
python schedule-texter.py
```

## Automating with Crontab
Setup cron job to run this script every morning at 7 a.m
1. Open crontab file
```sh
crontab -e
```
2. Add the following line to schedule the script
```sh
0 7 * * * /usr/bin/python3 /path/to/your/script/schedule-texter.py
```