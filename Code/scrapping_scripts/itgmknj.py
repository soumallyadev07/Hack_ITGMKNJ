from datetime import datetime
from func_timeout import func_timeout, FunctionTimedOut, func_set_timeout
from selenium import webdriver
import pandas as pd
import csv, functions, pickle, re, time, warnings
import os


custom_options = webdriver.ChromeOptions()
custom_options.add_argument("--lang=en")
custom_options.add_argument('--ignore-certificate-errors')
custom_options.add_argument('--ignore-ssl-errors')

warnings.filterwarnings("ignore")

classmodel = pickle.load(open('Models/classModel.pkl', 'rb'))
class_count_vect = pickle.load(open('Models/class_count_vect', 'rb'))
tagmodel = pickle.load(open('Models/tagModel.pkl', 'rb'))
tag_count_vect = pickle.load(open('Models/tag_count_vect', 'rb'))

all_links_list = []
all_links = set()
level = 0
flag = ""


def extract_domain(url, remove_http=True):
    from urllib.parse import urlparse
    uri = urlparse(url)
    if remove_http:
        domain_name = f"{uri.netloc}"
    else:
        domain_name = f"{uri.netloc}://{uri.netloc}"

    domain_name = domain_name.split('.')
    subdomain = '.' + domain_name[-1]
    return subdomain


def checklink(flink):
    
    exceptwords = [ 'register', 'login', 'profile', 'facebook', 'twitter', 'instagram',
                    'google', 'linkedin', 'news', 'glance', 'gsearch', 'gallery', 'covid',
                    'download', 'upload', '.pdf', '.jpg', '.png', '.svg', '.jpeg', 
                    'form', '%', '\?', 'app', 'document', 'sitemap', 'manual', 'scheme', 'publications', 'video',
                    'password', 'Password', 'search', 'privacy', 'disclaimer', 'copyright', r'[1234567890][1234567890][1234567890][1234567890][1234567890]',
                    'terms', 'podcast', 'speech', 'youtube', 'agenda', 'found', '404', 'initiative', 'vision', 'strateg','briefings-statements'
                    #regional language codes
                    '/hi', '/ar', '/af', '/sq', '/eu', '/be', '/bg', '/ca', '/zh', '/hr', '/cs', '/da', '/nl', '/et', '/fo', '/fa', '/fi',
                    '/fr', '/gd', '/de', '/el', '/he', '/hu', '/is', '/id', '/ga', '/it', '/ja', '/ko', '/ku', '/lv', '/lt', '/mk', '/ml',
                    '/ms', '/mt', '/no', '/nb', '/nl', '/pl', '/pt', '/pa', '/rm', '/ro', '/ru', '/sr', '/sk', '/sl', '/sb', '/es', '/sv',
                    '/ts', '/th', '/tn', '/tr', '/uk', '/ur', '/ve', '/vi', '/cy', '/xh', '/ji', '/zu' ]
    
    flag = 1
    for ewords in exceptwords:
        try:
            if re.search(ewords, flink):
                flag = 0
                break
        except:
            continue

    return flag

@func_set_timeout(60)
def driverfunc(link):
    driver.get(link)

######################## Function for extraction of all links ###################################

def extract_all_links(links, level, driver):
    """
    This function extracts all the links on a given website.
    """
    all_links_list.append([])
    for link in links:
        print("Extracting Links from: ", link)
        try:
            driverfunc(link)
            
            a = driver.find_elements_by_tag_name('a')
            b = len(a)
            for i in range(b):
                try:
                    ref = a[i].get_attribute('href')
                    if re.search('#', ref):
                        x = re.search('#', ref)
                        ref = ref[:int(x.span()[0])]

                    if checklink(ref) and re.search('http', ref) and re.search(subdomain, ref) and ref not in all_links:
                        all_links_list[level].append(ref)
                        all_links.add(ref)
                except:
                    continue
        except:
            continue
    return


country_name=input("Enter Country Name: ")
country_link=input("Enter Country link (English): ")
countries = [country_name]
subdomain = extract_domain(country_link)

all_links_list.append([country_link])
all_links.add(country_link)
level += 1


while True:
    driver = webdriver.Chrome(executable_path="ChromeDriver/chromedriver.exe", options=custom_options)
    extract_all_links(all_links_list[level-1], level, driver)

    usefulllinks = functions.find_usefull_links(all_links_list[level], classmodel, class_count_vect)
    all_links_list[level].clear()
    all_links_list[level] = usefulllinks

    functions.link_scraping(all_links_list[level], driver)
    driver.quit()

    time.sleep(10)

    keys = ['Country','Full Name','First Name','Middle Name','Last Name','Gender','Title', 'Designation', 'Contact', 'Images', 'Last Updated']
    
    with open('ScrappedData/PoliticalLeaders.csv','a') as dept:
        writer = csv.DictWriter(dept, fieldnames=keys)
        writer.writeheader()

    functions.clean_data(countries)
    os.remove(os.path.join(os.getcwd(),"ScrappedData","Intermediate.csv"))
    level += 1

    while True:
        flag = input("Do you wish to continue scrapping the data? (yes/no)")
        if  flag == "yes" or flag == "no":
            break
        else:
            print("Invalid option.")

    if flag == "no":
        break
