from email.mime import base
from urllib import response
from click import pass_obj
import scrapy
import json
import csv
import os 

class CohoPscSpider(scrapy.Spider):
    name = "persons-with-significant-control"
    
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
                ____    ___   ___         ___   ___    ___   _____   ___   ____   _  _  
                )  _)\  (  _( / _(  ____  ) __( \   \  )_ _( )__ __( )_ _( / __ \ ) \/ ( 
                | '__/  _) \  ))_  )____( | _)  | ) (  _| |_   | |   _| |_ ))__(( |  \ | 
                )_(    )____) \__(        )___( /___/ )_____(  )_(  )_____(\____/ )_()_( 
                                                                         
                                                                                                                    
        ''')
        base_url ='https://api.company-information.service.gov.uk/company/'
        company_numbers=[13693711]
        with open('companynumberswithoutheaders.csv') as csvfile:
            data = list(csv.reader(csvfile))
        company_numbers = [x[0] for x in data]

        for company_number in company_numbers:
            psc_url = base_url + str(company_number) + '/persons-with-significant-control' + '?items_per_page=' + '100'
            yield scrapy.Request(psc_url, callback=self.parse, headers={'Authorization': '_GET YOUR OWN_'})
    
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

    def parse(self, response):
        # print(response.json())
        # yield response.json()
        base_url ='https://api.company-information.service.gov.uk'
        url = self.paginate(base_url, response)
        if url is not None:
            yield response.follow(url,callback=self.parse, headers={'Authorization': '_GET YOUR OWN_'})

        company_number_path = 'data/' + response.json()['links']['self'].split("/")[2]
        start_index = str(response.json()['start_index'])
        isExist = os.path.exists(company_number_path)
        if not isExist:
            os.makedirs(company_number_path)
        for item in response.json()['items']:
            psc= item['links']['self'].split("/")[5]
            with open(company_number_path + '/' + psc + '_' + start_index +".json", 'w') as fp:
                json.dump(response.json(), fp)
     
        # TODO extract officer ID to a new list
        # TODO Save the raw data into file