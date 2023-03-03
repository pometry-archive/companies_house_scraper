from email.mime import base
from urllib import response
from click import pass_obj
import scrapy
import json
import csv
import os

class CohoSpider(scrapy.Spider):
    name = "officers"
    
    def start_requests(self):
        print('''
                                                                                                                      
                            ,--,                                ,-.----.                                              
  ,----..                 ,--.'|                      .--.--.   \    /  \     ,---,    ,---,        ,---,.,-.----.    
 /   /   \             ,--,  | :                     /  /    '. |   :    \ ,`--.' |  .'  .' `\    ,'  .' |\    /  \   
|   :     :  ,---.  ,---.'|  : '   ,---.      ,---,.|  :  /`. / |   |  .\ :|   :  :,---.'     \ ,---.'   |;   :    \  
.   |  ;. / '   ,'\ |   | : _' |  '   ,'\   ,'  .' |;  |  |--`  .   :  |: |:   |  '|   |  .`\  ||   |   .'|   | .\ :  
.   ; /--` /   /   |:   : |.'  | /   /   |,---.'   ,|  :  ;_    |   |   \ :|   :  |:   : |  '  |:   :  |-,.   : |: |  
;   | ;   .   ; ,. :|   ' '  ; :.   ; ,. :|   |    | \  \    `. |   : .   /'   '  ;|   ' '  ;  ::   |  ;/||   |  \ :  
|   : |   '   | |: :'   |  .'. |'   | |: ::   :  .'   `----.   \;   | |`-' |   |  |'   | ;  .  ||   :   .'|   : .  /  
.   | '___'   | .; :|   | :  | ''   | .; ::   |.'     __ \  \  ||   | ;    '   :  ;|   | :  |  '|   |  |-,;   | |  \  
'   ; : .'|   :    |'   : |  : ;|   :    |`---'      /  /`--'  /:   ' |    |   |  ''   : | /  ; '   :  ;/||   | ;\  \ 
'   | '/  :\   \  / |   | '  ,/  \   \  /           '--'.     / :   : :    '   :  ||   | '` ,/  |   |    \:   ' | \.' 
|   :    /  `----'  ;   : ;--'    `----'              `--'---'  |   | :    ;   |.' ;   :  .'    |   :   .':   : :-'   
 \   \ .'           |   ,/                                      `---'.|    '---'   |   ,.'      |   | ,'  |   |.'     
  `---`             '---'                                         `---`            '---'        `----'    `---'       
                                                                                                                        
        
        ''')
        base_url ='https://api.company-information.service.gov.uk/company/'
        company_numbers=[13693711]
        # with open('companynumberswithoutheaders.csv') as csvfile:
        #     data = list(csv.reader(csvfile))
        # company_numbers = [x[0] for x in data]

        for company_number in company_numbers:
            officer_url = base_url + str(company_number) + '/officers' + '?items_per_page=' + '100'
            yield scrapy.Request(officer_url, callback=self.parse, headers={'Authorization': '_GET YOUR OWN_'})
    
    def paginate(self, base_url, response):
        start_index=response.json()['start_index']
        items_per_page=response.json()["items_per_page"]
        total_results=response.json()["total_results"]
        if(start_index + items_per_page < total_results):
            next_index=start_index+items_per_page
            url=base_url + response.json()['links']['self'] + '?start_index=' + str(next_index) + '&items_per_page=' + str(items_per_page)
            return url
        else:
            return None

    def parse_officer(self, response):
        base_url ='https://api.company-information.service.gov.uk'
        url = self.paginate(base_url, response)
        if url is not None:
            yield response.follow(url,callback=self.parse_officer, headers={'Authorization': '_GET YOUR OWN_'})

        # yield response.json()
        filename=response.json()['links']['self'].split("/")[2]
        start_index = str(response.json()['start_index'])
        # if officer does not have a folder make them one
        officer_id = response.json()['links']['self'].split('/')[2]
        office_path = "data/"+str(officer_id)
        isExist = os.path.exists(office_path)
        if not isExist:
            os.makedirs(office_path)
        with open(office_path+'/'+filename+'_'+start_index+".json", 'w') as fp:
            json.dump(response.json(), fp)


    def parse(self, response):
        # print(response.json())
        # yield response.json()
        base_url ='https://api.company-information.service.gov.uk'
        url = self.paginate(base_url, response)
        if url is not None:
            yield response.follow(url,callback=self.parse, headers={'Authorization': '_GET YOUR OWN_'})

        for item in response.json()['items']:
            appointment_list_url=base_url+item['links']['officer']['appointments']+'?start_index=0&items_per_page=100'
            yield response.follow(appointment_list_url, callback=self.parse_officer, headers={'Authorization': '_GET YOUR OWN_'})

        # TODO extract officer ID to a new list
        # TODO Save the raw data into file
