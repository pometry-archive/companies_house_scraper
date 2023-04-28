import scrapy
import json
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class BarbaraSpiderRun():
    def __init__(self, key):
        self.key = key

    def start(self):
        process = CrawlerProcess(get_project_settings())
        process.crawl(BarbaraSpider, self.key)
        process.start() # the script will block here until the crawling is finished


class BarbaraSpider(scrapy.Spider):
    name = "barbara"  


    def __init__(self, key):
        self.key = key

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
        base_url = 'https://api.company-information.service.gov.uk/company/'
        
        officer_url = base_url + '08802828' + '/officers' + '?items_per_page=' + '100'
        yield scrapy.Request(officer_url, callback=self.parse, headers={'Authorization': self.key})

    def paginate(self, base_url, response):
        start_index = response.json()['start_index']
        items_per_page = response.json()["items_per_page"]
        total_results = response.json()["total_results"]
        if (start_index + items_per_page < total_results):
            next_index = start_index + items_per_page
            url = base_url + response.json()['links']['self'] + '?start_index=' + str(
                next_index) + '&items_per_page=' + str(items_per_page)
            return url
        else:
            return None

    def parse_officer(self, response):
        base_url = 'https://api.company-information.service.gov.uk'
        url = self.paginate(base_url, response)
        if url is not None:
            yield response.follow(url, callback=self.parse_officer, headers={'Authorization': self.key})

        # yield response.json()
        filename = response.json()['links']['self'].split("/")[2]
        start_index = str(response.json()['start_index'])
        # if officer does not have a folder make them one
        officer_id = response.json()['links']['self'].split('/')[2]
        office_path = "data/" + str(officer_id)
        isExist = os.path.exists(office_path)
        if not isExist:
            os.makedirs(office_path)
        with open(office_path + '/' + filename + '_' + start_index + ".json", 'w') as fp:
            json.dump(response.json(), fp)

    def parse(self, response):
        # print(response.json())
        # yield response.json()
        base_url = 'https://api.company-information.service.gov.uk'
        url = self.paginate(base_url, response)
        if url is not None:
            yield response.follow(url, callback=self.parse, headers={'Authorization': self.key})

        for item in response.json()['items']:
            appointment_list_url = base_url + item['links']['officer'][
                'appointments'] + '?start_index=0&items_per_page=100'
            yield response.follow(appointment_list_url, callback=self.parse_officer,
                                  headers={'Authorization': self.key})

        # TODO extract officer ID to a new list
        # TODO Save the raw data into file

    

