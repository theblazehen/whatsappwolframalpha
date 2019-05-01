# WhatsApp Web Wolfram Alpha Bot

## Installation
- `pip3 install -r requirements.txt`

- Run whatsapp web in selenium: 
  - ``docker run -d -p 4444:4444 -p 5900:5900 --name firefox -v /dev/shm:/dev/shm selenium/standalone-firefox-debug:3.14.0-curium``
  
- `python3 bot.py`

- `vncviewer 127.0.0.1`, pw is secret. Scan the code on the phone

## Usage
Direct message it with a query, or if it's added to a group then start the query with a "WA", or "wa", case doesn't matter.
