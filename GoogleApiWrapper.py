# encoding: utf-8

import sys
import httplib2
import pytz
import argparse
from datetime import datetime, timedelta
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.tools import run

class GoogleApiWrapper:
    _http = None
    _timezone = pytz.timezone('Asia/Tokyo')
    _parser = None

    def __init__(self, conf):
        self._InitCredentials(conf)
        self._InitParser()

    def _InitParser(self):
        self._parser = argparse.ArgumentParser(description='google apis.')
        subparsers = self._parser.add_subparsers(help='sub command help')

        parser_calendar = subparsers.add_parser('calendar', help='calendar api')
        calendar_subparsers = parser_calendar.add_subparsers(help='calendar sub command help')
        
        parser_calendar_list = calendar_subparsers.add_parser('list', help='show events list')
        parser_calendar_list.add_argument('--calendar_list', action='store_true')

        parser_calendar_list = calendar_subparsers.add_parser('insert', help='insert new event')
        parser_calendar_list.add_argument('--calendar_insert', action='store_true')
        parser_calendar_list.add_argument('-s', '--summary', help='summary context', required=True)
        parser_calendar_list.add_argument('-b', '--start', '--begin', help='start date', type=str, required=True)
        parser_calendar_list.add_argument('-e', '--end', help='end date', type=str, required=True)
        parser_calendar_list.add_argument('-t', '--date_time', help='which is format start and end, yyyy-MM-ddTHH:mm:ss (true) or yyyy-MM-dd (false)', action='store_true', default=False)

    def _InitCredentials(self, conf):
        storage = Storage('calendar.dat')
        credentials = storage.get()
        if not credentials or credentials.invalid:
            flow = OAuth2WebServerFlow(conf)
            credentials = run(flow, storage)

        self._http = httplib2.Http()
        credentials.authorize(self._http)

        service = build('oauth2', 'v2', http=self._http)

    def ArgParse(self, args):
        ag = self._parser.parse_args(args.split())
        if 'calendar_list' in ag:
            list = self.GetCalendarList()
            print u'\n'.join(list)
        elif 'calendar_insert' in ag:
            data_type = 'dateTime' if ag.date_time else 'date'
            event = {
                'start': {data_type: ag.start + ("+09:00" if ag.date_time else "")},
                'end': {data_type: ag.end + ("+09:00" if ag.date_time else "")},
                'summary': ag.summary
            }

            try:
                self.SetCalendarEvent(event)
            except:
                raise
            print u'insert event completed!\n'
    
    def GetCalendarList(self):
        now = datetime.now(tz=self._timezone)
        timeMin = datetime(year=now.year, month=now.month, day=now.day, tzinfo=self._timezone)
        timeMin = timeMin.isoformat()
    
        res = [];
        service = build('calendar', 'v3', http=self._http)
        calendars = service.calendarList().list().execute()
        for calendar in calendars['items']:
            events = service.events().list(
                calendarId=calendar['id'],
                singleEvents=True,
                timeMin=timeMin,
                timeZone=self._timezone.zone
            ).execute()
            for event in events['items']:
                start = ""

                if 'date' in event['start']:
                    start = event['start']['date'] + ' ' * 17
                elif 'dateTime' in event['start']:
                    start = event['start']['dateTime'][:-6]

                res.append('%s [%s]' % (start, event['summary']))
    
        res.sort()
        return res

    def SetCalendarEvent(self, arg):
        service = build('calendar', 'v3', http=self._http)
        calendars = service.calendarList().list().execute()
        target_calendar_id = calendars['items'][0]['id']
        service.events().insert(calendarId=target_calendar_id, body=arg).execute()
