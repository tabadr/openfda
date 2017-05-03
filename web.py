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

class OpenFDAClient():

    OPENFDA_API_URL = 'api.fda.gov'
    OPENFDA_API_EVENT = '/drug/event.json'


    def get_event(self,path):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?limit='+path)
        r1 = conn.getresponse()
        data1 = r1.read()
        data = data1.decode('utf8')
        events = json.loads(data)
        return events


    def get_events_search_medicinal_product(self,path):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct:"'+path+'"&limit=10')
        r1 = conn.getresponse()
        data1 = r1.read()
        data = data1.decode('utf8')
        events= json.loads(data)
        return events

    def get_events_search_companynumb(self,path):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?search=companynumb:'+path+'&limit=10')
        r1 = conn.getresponse()
        data1 = r1.read()
        data = data1.decode('utf8')
        events= json.loads(data)
        return events



class OpenFDAParser():


    def get_companies(self,path):
        client= OpenFDAClient()
        events= client.get_events_search_medicinal_product(path)
        companies = []
        results = events['results']
        for event in results:
            companies += [event['companynumb']]
        return companies


    def get_drugs_from_events(self,path):
        client= OpenFDAClient()
        events = client.get_event(path)
        drugs = []
        results = events['results']
        for event in results:
            drugs += [event['patient']['drug'][0]['medicinalproduct']]
        return drugs

    def get_drug_effects(self,path):
        client= OpenFDAClient()
        events= client.get_event(path)
        effects = []
        results = events['results']
        for effect in results:
            effects += [effect['patient']['reaction'][0]['reactionmeddrapt']]
        return effects


    def get_drugs(self,path):
        client= OpenFDAClient()
        events=client.get_events_search_companynumb(path)
        drugs=[]
        results= events['results']
        for event in results:
            drugs +=[event['patient']['drug'][0]['medicinalproduct']]
        return drugs



    def get_companynumb(self,path):
        client= OpenFDAClient()
        events=client.get_event(path)
        companynumb=[]
        results= events['results']
        for company in results:
            companynumb+=[company['companynumb']]
        return companynumb


    def get_patient_sex(self,path):
        client= OpenFDAClient()
        events=client.get_event(path)
        patientsex=[]
        results=events['results']
        for sex in results:
            patientsex+=[sex['patient']['patientsex']]
        return patientsex



class OpenFDAHTML():

    def get_main_page(self):

        html = """
        <html>
            <head>
                <title>Open FDA App</title>
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

    def get_second_main_page(self):

        html = """
        <html>
            <head></head>
            <body>
                <h1>OpenFDA Client 2</h1>
                <form method="get" action="effects">
                    <input type = "submit" value="Drug effects list: Send to OpenFDA"></input>
                    Limit:
                    <input type = "text" name="limit"></input>
                </form>
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

    def get_page_patient_sex(self,patients):

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
            <h1>Error 404 Found</h1>
            The action sent doesn't exist
        </body>
        </html>
        '''
        return html

    def get_page_effects(self,effects):
        s = ''
        for effect in effects:
            s += '<li>' +effect+ '</li>'

        html = '''
        <html>
        <head> </head>
        <body>
            <h1>Drug effects</h1>
            <ol>
                %s
            </ol>
        </body>
        </html>
        ''' %(s)

        return html



class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        client= OpenFDAClient()
        parser= OpenFDAParser()
        HTML= OpenFDAHTML()

        main_page = False
        is_second_main_page=False
        is_list_effects=False
        is_list_drugs = False
        is_search_drug = False
        is_list_companies= False
        is_search_companies=False
        is_list_patient_sex=False
        is_not_url=False
        is_found=True
        is_secret=False
        is_redirect=False
        if self.path == '/':
            main_page = True
        elif 'secondMainPage' in self.path:
            is_second_main_page=True
        elif 'listDrugs' in self.path:
            is_list_drugs = True
        elif 'listCompanies' in self.path:
            is_list_companies= True
        elif 'searchDrug' in self.path:
            is_search_drug = True
        elif 'searchCompany' in self.path:
            is_search_companies= True
        elif 'listGender' in self.path:
            is_list_patient_sex=True
        elif 'secret' in self.path:
            is_secret=True
        elif 'redirect'in self.path:
            is_redirect=True
        elif 'effects' in self.path:
            is_list_effects=True
        else:
            is_not_url=True
            is_found=False


        if is_secret:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Login required"')
        elif is_redirect:
            self.send_response(302)
            self.send_header('Location','/')
        elif is_found:
            self.send_response(200)
            self.send_header('Content-type','text/html')
        else:
            self.send_response(404)
            self.send_header('Content-type','text/html')

        self.end_headers()







        if main_page:
            html = HTML.get_main_page()
            self.wfile.write(bytes(html, "utf8"))
        elif is_second_main_page:
            html=HTML.get_second_main_page()
            self.wfile.write(bytes(html,"utf8"))
        elif is_list_drugs:
            path=self.path.split('=')[1]
            drugs = parser.get_drugs_from_events(path)
            html = HTML.get_page_drugs(drugs)
            self.wfile.write(bytes(html, "utf8"))
        elif is_search_drug:
            path=self.path.split('=')[1]
            companies = parser.get_companies(path)
            html = HTML.get_page_companies(companies)
            self.wfile.write(bytes(html, "utf8"))
        elif is_list_companies:
            path=self.path.split('=')[1]
            companynumb= parser.get_companynumb(path)
            html= HTML.get_page_companies(companynumb)
            self.wfile.write(bytes(html, "utf8"))
        elif is_search_companies:
            path=self.path.split('=')[1]
            drugs= parser.get_drugs(path)
            html = HTML.get_page_drugs(drugs)
            self.wfile.write(bytes(html, "utf8"))
        elif is_list_patient_sex:
            path=self.path.split('=')[1]
            patientsex= parser.get_patient_sex(path)
            html= HTML.get_page_patient_sex(patientsex)
            self.wfile.write(bytes(html, "utf8"))
        elif is_list_effects:
            path=self.path.split('=')[1]
            effects= parser.get_drug_effects(path)
            html= HTML.get_page_effects(effects)
            self.wfile.write(bytes(html, "utf8"))
        elif is_not_url:
            html= HTML.get_page_error_404()
            self.wfile.write(bytes(html, "utf8"))



        return
