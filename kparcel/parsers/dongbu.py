# -*- coding: utf-8 -*-


from kparcel.models import Track, Parcel
from kparcel.parser import Parser, ParserRequest


class DongbuParser(Parser):
    def __init__(self, invoice_number):
        super(DongbuParser, self).__init__(invoice_number)
        parser_request = ParserRequest()
        parser_request.url = 'http://www.dongbups.com/newHtml/delivery/' \
                             'dvsearch_View.jsp?item_no=%s' % self.invoice_number
        self.parser_request = parser_request

    def parse(self, parser, response):
        tables = parser.find_all('table', {'class': 'dv_list'})

        basicTable = tables[0]
        trs = basicTable.find_all('tr')
        sender = getattr(trs[1].find_all('td')[0], 'string', '')
        receiver = getattr(trs[1].find_all('td')[1], 'string', '')

        parcel = Parcel()
        parcel.sender = sender
        parcel.receiver = receiver
        self.parcel = parcel

        trackTable = tables[1]
        trs = trackTable.find_all('tr')

        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) != 0:
                time = getattr(tds[0], 'string', '') + ' ' + getattr(tds[1], 'string', '')
                location = getattr(tds[2], 'string', '').split('/')[0]
                status = getattr(tds[3], 'string', '')
                phone = getattr(tds[2], 'string', '').split('/')[1]

                track = Track()
                track.time = time
                track.location = location
                track.status = status
                track.phone1 = ''.join(phone.split())
                self.add_track(track)

