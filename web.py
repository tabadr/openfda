# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2016 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors:
#     Teresa Abad Rueda
#


import http.server
import http.client
import json


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    OPENFDA_API_URL = 'api.fda.gov'
    OPENFDA_API_EVENT = '/drug/event.json'

    def get_event(self):

        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?limit=10')
        r1 = conn.getresponse()
        data1 = r1.read()
        data = data1.decode('utf8')
        events = json.loads(data)
        return events

    def get_drugs_from_events(self):

        events = self.get_event()
        medicamentos = []
        results = events['results']
        for event in results:
            medicamentos += [event['patient']['drug'][0]['medicinalproduct']]
        return medicamentos


    def get_events_search(self):
        incognita=self.path.split('=')[1]
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct:"'+incognita+'"&limit=10')
        r1 = conn.getresponse()
        data1 = r1.read()
        data = data1.decode('utf8')
        events= json.loads(data)
        return events

    def get_empresas(self):

        events= self.get_events_search()
        empresas = []
        results = events['results']
        for event in results:
            empresas += [event['companynumb']]
        return empresas


    def get_companynumb(self):
        events=self.get_event()
        companynumb=[]
        results= events['results']
        for company in results:
            companynumb+=[company['companynumb']]
        return companynumb


    def get_main_page(self):

        html = """
        <html>
            <head>
            </head>
            <body>
                <form method="get" action="receivedrug">
                    <input type = "submit" value="Drug List: Send to OpenFDA">
                    </input>
                </form>
                <form method="get" action="search">
                    <input type = "text" name="drug"></input>
                    <input type = "submit" value="Drug Search: Send to OpenFDA">
                    </input>
                </form>
                <form method="get" action="receivecompany">
                    <input type = "submit" value="Companynumb List: Send to OpenFDA"></input>
                </form>
                <form method="get" action="search">
                    <input type = "text" name="company"></input>
                    <input type = "submit" value="Search drug from companynumb: Send to OpenFDA"></input>
                </form>
            </body>
        </html>
        """
        return html

    def get_page_drugs(self, medicamentos):

        s = ''
        for med in medicamentos:
            s += '<li>' +med+ '</li>'

        html = '''
        <html>
        <head> </head>
        <body>
            <h1>Medicinal Products</h1>
            <ul>
                %s
            </ul>
        </body>
        </html>
        ''' %(s)

        return html

    def get_page_companies(self, medicamentos):

        s = ''
        for med in medicamentos:
            s += '<li>' +med+ '</li>'

        html = '''
        <html>
        <head> </head>
        <body>
            <h1>Companies</h1>
            <ul>
                %s
            </ul>
        </body>
        </html>
        ''' %(s)

        return html



    def do_GET(self):

        main_page = False
        is_event = False
        is_search = False
        is_company= False
        if self.path == '/':
            main_page = True
        elif self.path =='/receivedrug':
            is_event = True
        elif self.path == '/receivecompany':
            is_company= True
        elif self.path.find('search'):
            is_search = True



        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()





        if main_page:
            html = self.get_main_page()
            self.wfile.write(bytes(html, "utf8"))
        elif is_event:
            medicamentos = self.get_drugs_from_events()
            html2 = self.get_page_drugs(medicamentos)
            event = self.get_event()
            self.wfile.write(bytes(html2, "utf8"))
        elif is_search:
            empresas = self.get_empresas()
            html3 = self.get_page_companies(empresas)
            self.wfile.write(bytes(html3, "utf8"))
        elif is_company:
            companynumb= self.get_companynumb()
            html4= self.get_page_companies(companynumb)
            self.wfile.write(bytes(html4, "utf8"))
        return
