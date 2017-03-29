# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2017 Bitergia
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
# Author:
#     Teresa Abad Rueda
#


import http.server
import http.client
import json


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    OPENFDA_API_URL = 'api.fda.gov'
    OPENFDA_API_EVENT = '/drug/event.json'

    def get_event(self):

        limite=self.path.split('=')[1]
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?limit='+limite)
        r1 = conn.getresponse()
        data1 = r1.read()
        data = data1.decode('utf8')
        events = json.loads(data)
        return events


    def get_drugs_from_events(self):

        events = self.get_event()
        drugs = []
        results = events['results']
        for event in results:
            drugs += [event['patient']['drug'][0]['medicinalproduct']]
        return drugs


    def get_events_search_medicinal_product(self):

        path=self.path.split('=')[1]
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct:"'+path+'"&limit=10')
        r1 = conn.getresponse()
        data1 = r1.read()
        data = data1.decode('utf8')
        events= json.loads(data)
        return events


    def get_events_search_companynumb(self):

        path=self.path.split('=')[1]
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?search=companynumb:'+path+'&limit=10')
        r1 = conn.getresponse()
        data1 = r1.read()
        data = data1.decode('utf8')
        events= json.loads(data)
        return events


    def get_companies(self):

        events= self.get_events_search_medicinal_product()
        companies = []
        results = events['results']
        for event in results:
            companies += [event['companynumb']]
        return companies


    def get_drugs(self):

        events=self.get_events_search_companynumb()
        drugs=[]
        results= events['results']
        for event in results:
            drugs +=[event['patient']['drug'][0]['medicinalproduct']]
        return drugs



    def get_companynumb(self):

        events=self.get_event()
        companynumb=[]
        results= events['results']
        for company in results:
            companynumb+=[company['companynumb']]
        return companynumb

    def get_patient_sex(self):

        events=self.get_event()
        patientsex=[]
        results=events['results']
        for sex in results:
            patientsex+=[sex['patient']['patientsex']]
        return patientsex


    def get_main_page(self):

        html = """
        <html>
            <head>
            </head>
            <body>
                <h1>OpenFDA Client</h1>
                <form method="get" action="listDrugs">
                    <input type = "submit" value="Drug List: Send to OpenFDA"></input>
                    Limit:
                    <input type = "text" name="limit"></input>
                </form>
                <form method="get" action="searchDrug">
                    <input type = "text" name="drug"></input>
                    <input type = "submit" value="Drug Search: Send to OpenFDA">
                    </input>
                </form>
                <form method="get" action="listCompanies">
                    <input type = "submit" value="Companynumb List: Send to OpenFDA"></input>
                    Limit:
                    <input type = "text" name="limit"></input>
                </form>
                <form method="get" action="searchCompany">
                    <input type = "text" name="company"></input>
                    <input type = "submit" value="Search drug from companynumb: Send to OpenFDA"></input>
                </form>
                <form method="get" action="listGender">
                    <input type = "submit" value="Patient sex: Send to OpenFDA"></input>
                    Limit:
                    <input type = "text" name="limit"></input>
            </body>
        </html>
        """
        return html


    def get_page_drugs(self, drugs):

        s = ''
        for drug in drugs:
            s += '<li>' +drug+ '</li>'

        html = '''
        <html>
        <head> </head>
        <body>
            <h1>Medicinal Products</h1>
            <ol>
                %s
            </ol>
        </body>
        </html>
        ''' %(s)

        return html


    def get_page_companies(self, companies):

        s = ''
        for company in companies:
            s += '<li>' +company+ '</li>'

        html = '''
        <html>
        <head> </head>
        <body>
            <h1>Companies</h1>
            <ol>
                %s
            </ol>
        </body>
        </html>
        ''' %(s)

        return html

    def get_page_patient_sex(sefl,patients):

        s = ''
        for sex in patients:
            s += '<li>' +sex+ '</li>'

        html = '''
        <html>
        <head> </head>
        <body>
            <h1>Patients Sex</h1>
            <ol>
                %s
            </ol>
        </body>
        </html>
        ''' %(s)

        return html

    def get_page_error_404(self):
        html='''
        <html>
        <head></head>
        <body>
            Error 404 Found
            The action sent doesn't exist
        </body>
        </html>
        '''
        return html



    def do_GET(self):

        main_page = False
        is_list_drugs = False
        is_search_drug = False
        is_list_companies= False
        is_search_companies=False
        is_list_patient_sex=False
        is_not_url=False
        is_found=True
        if self.path == '/':
            main_page = True
        elif '/listDrugs' in self.path:
            is_list_drugs = True
        elif '/listCompanies' in self.path:
            is_list_companies= True
        elif 'searchDrug' in self.path:
            is_search_drug = True
        elif 'searchCompany' in self.path:
            is_search_companies= True
        elif 'listGender' in self.path:
            is_list_patient_sex=True
        else:
            is_not_url=True
            is_found=False

        if is_found:
            self.send_response(200)
        else:
            self.send_response(404)



        self.send_header('Content-type','text/html')
        self.end_headers()





        if main_page:
            html = self.get_main_page()
            self.wfile.write(bytes(html, "utf8"))
        elif is_list_drugs:
            drugs = self.get_drugs_from_events()
            html = self.get_page_drugs(drugs)
            event = self.get_event()
            self.wfile.write(bytes(html, "utf8"))
        elif is_search_drug:
            companies = self.get_companies()
            html = self.get_page_companies(companies)
            self.wfile.write(bytes(html, "utf8"))
        elif is_list_companies:
            companynumb= self.get_companynumb()
            html= self.get_page_companies(companynumb)
            self.wfile.write(bytes(html, "utf8"))
        elif is_search_companies:
            drugs= self.get_drugs()
            html = self.get_page_drugs(drugs)
            self.wfile.write(bytes(html, "utf8"))
        elif is_list_patient_sex:
            patientsex= self.get_patient_sex()
            html= self.get_page_patient_sex(patientsex)
            self.wfile.write(bytes(html, "utf8"))
        elif is_not_url:
            html= self.get_page_error_404()
            self.wfile.write(bytes(html, "utf8"))


        return
