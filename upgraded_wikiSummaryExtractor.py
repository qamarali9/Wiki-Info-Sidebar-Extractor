import requests
from bs4 import BeautifulSoup
import threading
import json
import time

result = [] # List of dictionaries containing final output to be appended in file.

"""fetch_data fetches the relevant data as key:value pairs(dictionary) given a url(wikipedia).
Then appends the data fetched to result.""" 
def fetch_data(url):
    # try fetching a response, in case of exception raise error
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser') #For parsing
        response.close()
    except requests.exceptions.RequestException as exc:
        print(url)
        print('The following exception occured...')
        print(exc)
        print('Error code: ', exc.code)
    else:
        # everything is fine
        # extract the relevant data
        data = {}
        table = soup.find('table', attrs={'class':'infobox vcard'})

        try:
            rows = table.find_all('tr')
        except:
            print(url)
            return

        for row in rows:
            th = row.find('th')
            td = row.find('td')
            if th is not None and td is not None:
                key = th.get_text().strip().encode('utf8')
                val = td.get_text().strip().encode('utf8')
                data[str(key)] = str(val)
            else:
                print(url)

        result.append(data) # append relevant data to the final result


def get_company_urls(state_companyListing_url):
    try:
        response = requests.get(state_companyListing_url) # US companies
        soup = BeautifulSoup(response.text,'html.parser') #For parsing
        response.close()
    except requests.exceptions.RequestException as exc:
        print(url)
        print('The following exception occured...')
        print(exc)
        print('Error code: ', exc.code)
    else:
        tables = soup.find_all('table', attrs={'class':'wikitable'})
        print("length table elements:{}".format(len(tables)))
        categories = tables + soup.find_all('ul') 
        """if len(tables)==0:
            print("No table found, selecting <ul> elements")
            categories = soup.find_all('ul')
        else:
            categories = tables"""
        print(len(categories))
        #categories = soup.find_all('div', attrs={'class':"div-col columns column-width", 
        #    'style':"-moz-column-width: 30em; -webkit-column-width: 30em; column-width: 30em;"})
        stop_flag = False
        for category in categories:
            if stop_flag == True:
                break
            companies = category.find_all('a',href=True)
            for company in companies:
                href_to_append = company['href']
                if(href_to_append.startswith('#top')):
                    stop_flag = True
                    break
                print("In get company url: {}".format(href_to_append))
                if( (href_to_append=='/wiki/Wings_of_Alaska') or 
                        (href_to_append=='/wiki/Bank_of_the_West') or
                        (href_to_append=='/wiki/Associated_Grocers_of_the_South') or
                        (href_to_append=='/wiki/Blue_Cross_and_Blue_Shield_of_Alabama') or
                        (href_to_append=='/wiki/Retirement_Systems_of_Alabama') or
                        (href_to_append=='/wiki/Bank_of_America_Home_Loans') or
                        (href_to_append=='/wiki/Bank_of_the_West') or
                        (href_to_append=='/wiki/Blue_Shield_of_California') or
                        (href_to_append=='/wiki/Chicken_of_the_Sea') or
                        (href_to_append=='/wiki/Jack_in_the_Box') or
                        (href_to_append=='/wiki/Bank_of_California') or
                        (href_to_append=='/wiki/Frederick%27s_of_Hollywood') or

                        (href_to_append=='/wiki/Morgan,_Lewis_%26_Bockius') or
                        (href_to_append=='/wiki/Schnader,_Harrison,_Segal_%26_Lewis') or
                        (href_to_append=='/wiki/Children%27s_Hospital_of_Philadelphia') or
                        (href_to_append=='/wiki/Pennsylvania_Academy_of_Fine_Arts') or
                        (href_to_append=='/wiki/Subaru_of_America') or
                        (href_to_append=='/wiki/Wolf,_Block,_Schorr_and_Solis-Cohen') or
                        (href_to_append=='/wiki/Buchanan,_Ingersoll_%26_Rooney') or
                        (href_to_append=='/wiki/Farmers_and_Merchants_Bank_of_Western_Pennsylvania') or
                        (href_to_append=='/wiki/Armstrong_Group_of_Companies') or
                        (href_to_append=='/wiki/University_of_Pittsburgh_Medical_Center') or
                        (href_to_append=='/wiki/The_Bank_of_New_York_Mellon') or
                        (href_to_append=='/wiki/Hamilton_House_(Providence,_Rhode_Island)') or
                        (href_to_append=='/wiki/Stone,_Carpenter_%26_Willson') or
                        (href_to_append=='/wiki/Bank_of_America') or
                        (href_to_append=='/wiki/International_Bank_of_Commerce') or
                        (href_to_append=='/wiki/Oblon,_Spivak,_McClelland,_Maier_%26_Neustadt') or
                        (href_to_append=='/wiki/Infectious_Diseases_Society_of_America') or
                        (href_to_append=='/wiki/National_Association_of_Convenience_Stores') or
                        (href_to_append=='/wiki/ZERO%E2%80%94The_End_of_Prostate_Cancer') or
                        (href_to_append=='/wiki/Volkswagen_Group_of_America') or

                        (href_to_append.startswith('/wiki/') and 'template' not in href_to_append and 'Category' not in href_to_append and 
                        '_in_' not in href_to_append and '_of_' not in href_to_append and '_from_' not in href_to_append and 
                        'related_articles' not in href_to_append and 'Wikipedia:' not in href_to_append and 
                        'Special:' not in href_to_append and 'Help:' not in href_to_append and 'File:' not in href_to_append and
                        'Portal:' not in href_to_append and 
                        'Template:' not in href_to_append and 'Template_talk:' not in href_to_append and
                        href_to_append != '/wiki/Main_Page' and
                        href_to_append != '/wiki/Denver' and
                        href_to_append != '/wiki/Colorado_Western_Slope' and
                        href_to_append != '/wiki/Uinta_Basin' and
                        href_to_append != '/wiki/Uinta_Mountains' and
                        href_to_append != '/wiki/Southwest_Colorado' and
                        href_to_append != '/wiki/South-Central_Colorado' and
                        href_to_append != '/wiki/Sangre_de_Cristo_Mountains' and
                        href_to_append != '/wiki/San_Luis_Valley' and
                        href_to_append != '/wiki/Roaring_Fork_Valley' and
                        href_to_append != '/wiki/Roan_Plateau' and
                        href_to_append != '/wiki/Colorado_Plateau' and
                        href_to_append != '/wiki/Colorado_Piedmont' and
                        href_to_append != '/wiki/Northwestern_Colorado' and
                        href_to_append != '/wiki/Northern_Colorado' and
                        href_to_append != '/wiki/Colorado_Mineral_Belt' and
                        href_to_append != '/wiki/High_Rockies' and
                        href_to_append != '/wiki/High_Plains_(United_States)' and
                        href_to_append != '/wiki/Grand_Valley_(Colorado-Utah)' and
                        href_to_append != '/wiki/Front_Range_Urban_Corridor' and
                        href_to_append != '/wiki/Eastern_Plains' and
                        href_to_append != '/wiki/Denver-Aurora-Lakewood,_CO_Metropolitan_Statistical_Area' and
                        href_to_append != '/wiki/Central_Colorado' and
                        href_to_append != '/wiki/Colorado_State_Public_Defender' and
                        href_to_append != '/wiki/Germany' and
                        href_to_append != '/wiki/Australia' and
                        href_to_append != '/wiki/Sweden' and
                        href_to_append != '/wiki/United_Kingdom' and
                        href_to_append != '/wiki/Switzerland' and
                        href_to_append != '/wiki/Japan' and
                        href_to_append != '/wiki/France' and
                        href_to_append != '/wiki/Luxembourg' and
                        href_to_append != '/wiki/Belgium' and
                        href_to_append != '/wiki/Canada' and
                        href_to_append != '/wiki/Banking' and
                        href_to_append != '/wiki/Computer_security' and
                        href_to_append != '/wiki/Salt_Lake_City' and
                        href_to_append != '/wiki/Tourism' and
                        href_to_append != '/wiki/Diamond#Industrial-grade_diamonds' and
                        href_to_append != '/wiki/Aerospace_engineering' and
                        href_to_append != '/wiki/Dietary_supplement' and
                        href_to_append != '/wiki/Motion_picture' and
                        href_to_append != '/wiki/Ice_cream' and
                        href_to_append != '/wiki/Retail' and
                        href_to_append != '/wiki/Social_networking_service' and
                        href_to_append != '/wiki/Architecture' and
                        href_to_append != '/wiki/Software' and
                        href_to_append != '/wiki/Information_technology' and
                        href_to_append != '/wiki/Clothing' and
                        href_to_append != '/wiki/Baking' and
                        href_to_append != '/wiki/Handbag' and
                        href_to_append != '/wiki/Digital_identity' and
                        href_to_append != '/wiki/Chemical_industry' and
                        href_to_append != '/wiki/Web_design' and
                        href_to_append != '/wiki/Software' and
                        href_to_append != '/wiki/Computer_hardware' and
                        href_to_append != '/wiki/Video_game_development' and
                        href_to_append != '/wiki/Sugar_refinery' and
                        href_to_append != '/wiki/Publishing#Book_publishing' and
                        href_to_append != '/wiki/Payment_gateway' and
                        href_to_append != '/wiki/Printing' and
                        href_to_append != '/wiki/Enterprise_feedback_management' and
                        href_to_append != '/wiki/Music' and
                        href_to_append != '/wiki/Accounting_software' and
                        href_to_append != '/wiki/Consumer_electronics' and
                        href_to_append != '/wiki/Cosmetics' and
                        href_to_append != '/wiki/Essential_oil' and
                        href_to_append != '/wiki/Internet_service_provider' and
                        href_to_append != '/wiki/Project_management_software' and
                        href_to_append != '/wiki/Ladder' and
                        href_to_append != '/wiki/Groceries' and
                        href_to_append != '/wiki/Construction' and
                        href_to_append != '/wiki/Tire' and
                        href_to_append != '/wiki/Solar_energy' and
                        href_to_append != '/wiki/Home_security' and
                        href_to_append != '/wiki/Electric_vehicle' and
                        href_to_append != '/wiki/Mining' and
                        href_to_append != '/wiki/Personal_care' and
                        href_to_append != '/wiki/Alcoholic_drink' and
                        href_to_append != '/wiki/Board_game' and
                        href_to_append != '/wiki/Call_centre' and
                        href_to_append != '/wiki/Outdoor_recreation' and
                        href_to_append != '/wiki/Airline' and
                        href_to_append != '/wiki/Holding_company' and
                        href_to_append != '/wiki/Petroleum' and
                        href_to_append != '/wiki/Firearm' and
                        href_to_append != '/wiki/Smartphone' and
                        href_to_append != '/wiki/Research_software_engineering' and
                        href_to_append != '/wiki/Robotics' and
                        href_to_append != '/wiki/Amusement_ride' and
                        href_to_append != '/wiki/Health_care' and
                        href_to_append != '/wiki/Content_management' and
                        href_to_append != '/wiki/Furniture' and
                        href_to_append != '/wiki/Model_rocket' and
                        href_to_append != '/wiki/Experience_management' and
                        href_to_append != '/wiki/Mattress' and
                        href_to_append != '/wiki/Ski_resort' and
                        href_to_append != '/wiki/Software_as_a_service' and
                        href_to_append != '/wiki/Retail' and
                        href_to_append != '/wiki/Web_analytics' and
                        href_to_append != '/wiki/Personal_care' and
                        href_to_append != '/wiki/Cloud_storage' and
                        href_to_append != '/wiki/Financial_technology' and
                        href_to_append != '/wiki/Petroleum' and
                        href_to_append != '/wiki/For-profit_prisons' and
                        href_to_append != '/wiki/Insurance' and
                        href_to_append != '/wiki/Amusement_park' and
                        href_to_append != '/wiki/Education_software' and
                        href_to_append != '/wiki/Real_estate_development' and
                        href_to_append != '/wiki/Energy' and
                        href_to_append != '/wiki/Food' and
                        href_to_append != '/wiki/Semiconductor' and
                        href_to_append != '/wiki/Exercise' and
                        href_to_append != '/wiki/Historical_document' and
                        href_to_append != '/wiki/Nanotechnology' and
                        href_to_append != '/wiki/Alcoholic_beverages' and
                        href_to_append != '/wiki/Distance_learning' and
                        href_to_append != '/wiki/Marketing' and
                        href_to_append != '/wiki/Advertising' and
                        href_to_append != '/wiki/Cheese' and
                        href_to_append != '/wiki/Education' and
                        href_to_append != '/wiki/Genealogy' and
                        href_to_append != '/wiki/Inventory_management_software' and
                        href_to_append != '/wiki/Self_storage' and
                        href_to_append != '/wiki/Waste_management' and
                        href_to_append != '/wiki/Telecommunications' and
                        href_to_append != '/wiki/Bookselling' and
                        href_to_append != '/wiki/Aerial_lift' and
                        href_to_append != '/wiki/Natural_gas' and
                        href_to_append != '/wiki/Internet_security' and
                        href_to_append != '/wiki/Audio_equipment' and
                        href_to_append != '/wiki/Music_store' and
                        href_to_append != '/wiki/Fast_food' and
                        href_to_append != '/wiki/Extreme_sport' and
                        href_to_append != '/wiki/Restaurant_chain' and
                        href_to_append != '/wiki/Travel' and
                        href_to_append != '/wiki/Healthcare_industry' and
                        href_to_append != '/wiki/Musical_instrument' and
                        href_to_append != '/wiki/Hot_tub' and
                        href_to_append != '/wiki/Broadcasting' and
                        href_to_append != '/wiki/Boring_(earth)' and
                        href_to_append != '/wiki/Blender' and
                        href_to_append != '/wiki/Domain_Name_System' and
                        href_to_append != '/wiki/Technical_support' and
                        href_to_append != '/wiki/Human_Resources' and
                        href_to_append != '/wiki/Consumers%27_co-operative' and
                        href_to_append != '/wiki/Consumers%27_co-operative' and
                        href_to_append != '/wiki/Water_resources' and
                        href_to_append != '/wiki/Genealogy' and
                        href_to_append != '/wiki/Confectionery' and
                        href_to_append != '/wiki/Shooting_range' and
                        href_to_append != '/wiki/Contact_lens' and
                        href_to_append != '/wiki/San_Antonio' and
                        href_to_append != '/wiki/Houston' and
                        href_to_append != '/wiki/Dallas' and
                        href_to_append != '/wiki/David_Oreck' and
                        href_to_append != '/wiki/Rhode_Island#Education' and
                        href_to_append != '/wiki/Rhode_Island#Economy' and
                        href_to_append != '/wiki/Rhode_Island#Demographics' and
                        href_to_append != '/wiki/Hard_clam' and
                        href_to_append != '/wiki/Thirteen_Colonies' and
                        href_to_append != '/wiki/Narragansett_people' and
                        href_to_append != '/wiki/Rhode_Island#Geography' and
                        href_to_append != '/wiki/Colonial_colleges' and
                        href_to_append != '/wiki/Greater_Pittsburgh_Region' and
                        href_to_append != '/wiki/Western_Pennsylvania_English' and
                        href_to_append != '/wiki/Pittsburgh_Stock_Exchange' and
                        href_to_append != '/wiki/Allegheny_HYP_Club' and
                        href_to_append != '/wiki/Duquesne_Club' and
                        href_to_append != '/wiki/Allegheny_Conference' and
                        href_to_append != '/wiki/Pittsburgh_Public_Schools' and
                        href_to_append != '/wiki/Allegheny_County_Sheriff' and
                        href_to_append != '/wiki/Allegheny_County_District_Attorney' and
                        href_to_append != '/wiki/Pittsburgh_Police' and
                        href_to_append != '/wiki/Pittsburgh_Intergovernmental_Cooperation_Authority' and
                        href_to_append != '/wiki/Pittsburgh_City_Council' and
                        href_to_append != '/wiki/Allegheny_County_Courthouse' and
                        href_to_append != '/wiki/Pittsburgh_City-County_Building' and
                        href_to_append != '/wiki/David_L._Lawrence_Convention_Center' and
                        href_to_append != '/wiki/Allegheny_County_Airport_Authority' and
                        href_to_append != '/wiki/United_States' and
                        href_to_append != '/wiki/New_York_Stock_Exchange' and
                        href_to_append != '/wiki/Employment' and
                        href_to_append != '/wiki/Fortune_1000' and
                        href_to_append != '/wiki/Pennsylvania_State_Capitol' and
                        href_to_append != '/wiki/Harrisburg_School_District_(Pennsylvania)' and
                        href_to_append != '/wiki/South_Central_Pennsylvania' and
                        href_to_append != '/wiki/Harrisburg_metropolitan_area' and
                        href_to_append != '/wiki/Central_Pennsylvania_dialect' and
                        href_to_append != '/wiki/City_Island_(Pennsylvania)' and
                        href_to_append != '/wiki/Central_Penn_Business_Journal' and
                        href_to_append != '/wiki/YTI_Career_Institute' and
                        href_to_append != '/wiki/Dauphin_County' and
                        href_to_append != '/wiki/WellSpan_Health' and
                        href_to_append != '/wiki/PinnacleHealth_System' and
                        href_to_append != '/wiki/Philhaven' and
                        href_to_append != '/wiki/Lebanon_Valley_College' and
                        href_to_append != '/wiki/Lancaster_General_Hospital' and
                        href_to_append != '/wiki/Holy_Spirit_Hospital' and
                        href_to_append != '/wiki/Highmark' and
                        href_to_append != '/wiki/Dickinson_College' and
                        href_to_append != '/wiki/Yellowstone_National_Park' and
                        href_to_append != '/wiki/Old_Faithful_Inn' and
                        href_to_append != '/wiki/Wind_farm' and
                        href_to_append != '/wiki/Wind_River_Range' and
                        href_to_append != '/wiki/North_Antelope_Rochelle_Mine' and
                        href_to_append != '/wiki/Jackson_Hole' and
                        href_to_append != '' and
                        (',_' not in href_to_append or ',_Incorporated' in href_to_append or 
                            ',_Inc.' in href_to_append or ',_Limited' in href_to_append or ',_Ltd.' in href_to_append))):
                    print("Appending : {}".format(baseUrl + company['href']))
                    urls.add(baseUrl + company['href'])

            print("\n\n---end of part---\n\n\n")

    #mw-content-text > div.mw-parser-output > ul:nth-child(7) > li:nth-child(1) > a


# creating wikipedia urls
baseUrl = "https://en.wikipedia.org"
urls = set()
state_companyListing_urls = []
try:
    response = requests.get("https://en.wikipedia.org/wiki/List_of_companies_of_the_United_States") # US companies
    soup = BeautifulSoup(response.text,'html.parser') #For parsing
    response.close()
except requests.exceptions.RequestException as exc:
    print(url)
    print('The following exception occured...')
    print(exc)
    print('Error code: ', exc.code)
else:
    #categories = soup.find_all('div', attrs={'class':"div-col columns column-width"}) 
        #,'style':"-moz-column-width: 30em; -webkit-column-width: 30em; column-width: 30em;"})
    categories = soup.find_all('ul')
    stop_flag = False
    for category in categories:
        if stop_flag == True:
            break
        companies = category.find_all('a',href=True)
        for company in companies:
            href_to_append = company['href']
            if(href_to_append == '/wiki/Template:Lists_of_companies_by_U.S._state'):
                stop_flag = True
                break
            if(href_to_append.startswith('/wiki/') and 
                    ',_Oklahoma' not in href_to_append and
                    ',_Tennessee' not in href_to_append and
                    ',_Pennsylvania' not in href_to_append):
                print("Url added from main page: {}".format(baseUrl + href_to_append))
                urls.add(baseUrl + href_to_append)

    categories = soup.find_all('div', attrs={'role':"note", 'class':"hatnote navigation-not-searchable"})
    print("Number of notes of urls directing to company listing of particular states: {}".format(len(categories)))
    for category in categories:
        listing_urls_aTags = category.find_all('a',href=True)
        for listing_urls_aTag in listing_urls_aTags:
            state_companyListing_urls.append(baseUrl + listing_urls_aTag['href'])


print("state_companyListing_urls:\n{}".format(state_companyListing_urls))
for state_companyListing_url in state_companyListing_urls:
    get_company_urls(state_companyListing_url)


# creating threads for fetching data in parallel (limiting amount of concurrent thread to 100)
print("Number of Urls: {}".format(len(urls)))

f = open('output.json','a')
urls = list(urls)

i = 0
while(i+100<len(urls)):
    threads = [threading.Thread(target=fetch_data, args=(url,)) for url in urls[i:i+100]]
    print()
    i += 100
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print("Sleeping...")
    time.sleep(3)
    print("Woke up...")
    print(len(result))
    print(result[-100:])
    
    # writing to file in json format which is in sync with mongoDB data format
    for row in result:
        f.write(json.dumps(row, sort_keys=True, 
            indent=4, separators=(',', ': ')))
        f.write('\n')
    result = []

threads = [threading.Thread(target=fetch_data, args=(url,)) for url in urls[i:len(urls)]]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print(len(result))
print(result[:10])

# writing to file in json format which is in sync with mongoDB data format
for row in result:
    print(row)
    f.write(json.dumps(row, sort_keys=True, 
        indent=4, separators=(',', ': ')))
    f.write('\n')

f.close()
