#Import Libraries
import pandas as pd
from selenium import webdriver
import warnings
import pickle
import re
from datetime import datetime
import csv
warnings.filterwarnings("ignore")

classmodel = pickle.load(open('Models/classModel.pkl', 'rb'))
class_count_vect = pickle.load(open('Models/class_count_vect', 'rb'))
tagmodel = pickle.load(open('Models/tagModel.pkl', 'rb'))
tag_count_vect = pickle.load(open('Models/tag_count_vect', 'rb'))



############################ Function to Sort Useful Links #########################################

def find_usefull_links(links, classmodel, class_count_vect):
    """
    This model takes a list of links, sort the useful links and return them in as an other list 
    """

    import re
    final_links = []
    seclinks = links
    for link in links:
        fulllink = link
        if link == None:
            continue
        else:
            link = link.replace('://', ' ')
            link = link.replace('@', ' ')
            link = link.replace('#', ' ')
            link = link.replace('/', ' ')
            link = link.replace('-', ' ')
            link = link.replace('.', ' ')
            link = link.replace('https', '')
            link = link.replace('http', '')
            link = link.replace('www', '')
            link = link.replace('&', ' ')
            link = link.replace('=', ' ')
            linkpd = pd.Series(link.strip())
            link_feature = class_count_vect.transform(linkpd)
            result = classmodel.predict(link_feature)

            result = result.tolist()
            result = str(result)
            if result == '[1]':
                final_links.append(fulllink)
    final_links = list(dict.fromkeys(final_links))
    
    if len(final_links) == 0 or len(final_links) < 5:
        for linksec in seclinks:
            linkwords = ['cabinet', 'gover', 'goverment', 'composition', 'ministers', 'minister',
                         'president', 'composicao', 'parliament', 'person', 'who', 'mini', 'compo',
                         'governor', 'secretariat', 'secretary']
            for w in linkwords:
                if re.search(w, linksec):
                    final_links.append(linksec)
                else:
                    continue
    final_links = list(dict.fromkeys(final_links))
    return (final_links)



########################### Function to extract useful classnames ######################################

def find_usefull_tags(tags, tagmodel, tag_count_vect):
    """
    It takes a list of all class names on a given website, predicts the useful classnames and return a list of them.
    """

    final_tags = []
    for tag in tags:
        if tag == None:
            continue
        else:
            tagpd = pd.Series(tag)
            tag_feature = tag_count_vect.transform(tagpd)
            result = tagmodel.predict(tag_feature)

            result = result.tolist() 
            result  = str(result)
            if result == '[1]':
                final_tags.append(tag)
    final_tags = list(dict.fromkeys(final_tags))
    return(final_tags)



################### Function to extract all classnames #################################

def extract_all_tags(final_link, driver):
    """
    It takes in a website link as input and return all the classnames used on the website.
    """

    #driver = webdriver.Chrome(executable_path="ChromeDriver/chromedriver.exe")
    driver.get(str(final_link))
    classes = []
    tags = ['div', 'td', 'li', 'a']
    for tag in tags:
        a = driver.find_elements_by_tag_name(str(tag))
        b = len(a)
        for i in range(b):
            try:
                if a[i].get_attribute("class") == None or a[i].get_attribute("class") == '' or a[i].get_attribute("class") == ' ' or a[i].get_attribute("class") == '  ':
                    continue
                else:
                    className = a[i].get_attribute("class").strip().split(" ")
                    for classN in className:
                        classes.append(str(tag) + '.' + str(classN))

            except:
                continue

    #driver.quit()
    classes = list(dict.fromkeys(classes))
    return(classes)



############################## Function to data to excel ###################################

def dump_data(infotext, sociallinks, imageslinks):
    """
    It takes all the useful data as input and write it to .csv file.
    """
    import csv
    import re
    usewords = ['Birth','Certificate','Driving','License','Pan' ,'Card','Contact','Details','Twitter','Facebook' 
                ,'Account','Articles' ,'Live','Follow' ,'List', 'birth', 'certificate','driving' ,'license','pan'
                , 'card','contact','details','twitter','facebook' ,'account','articles','follow' ,'list',"ECONOMY"
                ,"NATIONAL SECURITY","BUDGET","IMMIGRATION","CORONAVIRUS.GOV","LIVE","JOBS","GET INVOLVED"
                ,"COPYRIGHT POLICY","PRIVACY POLICY","economy","national security","budget","immigration"
                ,"coronavirus.gov","live","jobs","get involved","copyright policy","privacy policy"
                ,"WATCH","LISTEN","HOME","PUBLICATIONS","ADMINISTRATION","HAVE YOUR SAY","ARRANGE A TOUR"
                ,"ATTEND A DEBATE","DIRECTIONS","CONTACT DETAILS"]
    for word in usewords:
        for text in infotext:
            if re.search(word, text):
                infotext.remove(text)
            else:
                continue
             
    if len(infotext) != 0:
        with open('ScrappedData/Intermediate.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(infotext + sociallinks + imageslinks)



####################### Function to scrap the useful data ##################################

def scrape_data(final_link, tags, driver):
    """
    It takes a website link and useful tags(classnames) as input, scrap the data and call dumpdata function to write the useful data to .csv file. 
    """
    #driver = webdriver.Chrome(executable_path="ChromeDriver/chromedriver.exe")
    driver.get(str(final_link))
    errcount = 0
    for tag in tags:
        try:
            children = driver.find_elements_by_css_selector(tag)
            for child in children:
                try:
                    links = child.find_elements_by_tag_name('a')
                    images = child.find_elements_by_tag_name('img')
                    if len(child.text) == 0:
                        continue
                    else:
                        infotext = []
                        sociallinks = []
                        imageslinks = [] 
                        checklen = len(child.text.split("\n"))
                        if checklen > 0 and checklen < 30:
                            infotext = child.text.split("\n")

                        for link in links:
                            sociallinks.append(link.get_attribute('href'))

                        for linki in imageslinks:
                            imageslinks.append(linki.get_attribute('href'))

                except:
                    continue
                
                infolen = len(infotext)
                sociallen  = len(sociallinks)
                if sociallen > 0 and sociallen <= 10 and infolen != 0:
                    dump_data(infotext, sociallinks, imageslinks)
                    
                else:
                    if infolen == 0 or sociallen == 0:
                        errcount += 1
                          
        except:
            continue
            
        if errcount == len(tags):
            scrape_data_tag(final_link, driver)
        
        elif errcount > 0:
            scrape_data_tag(final_link, driver)
            
    #driver.quit()


def scrape_data_tag(final_link, driver):
    """
    If no useful classnames are found, scrape_data_tag function is used to scrape data on the basis of html tags.
    """

    import time
    #driver = webdriver.Chrome(executable_path="ChromeDriver/chromedriver.exe")
    driver.get(final_link)
    time.sleep(2)
    tags = ['li', 'p', 'tr']
    for tag in tags:
        children = driver.find_elements_by_tag_name(tag)
        for child in children:
            try:
                links = child.find_elements_by_tag_name('a')
                images = child.find_elements_by_tag_name('img')
                if len(child.text) == 0:
                    continue
                else:
                    infotext = []
                    sociallinks = []
                    imageslinks = [] 
                    checklen = len(child.text.split("\n"))
                    if checklen > 0 and checklen < 30:
                        infotext = child.text.split("\n")

                    for link in links:
                        sociallinks.append(link.get_attribute('href'))
                        
                    for link in imageslinks:
                        imageslinks.append(link.get_attribute('href'))

            except:
                continue

            infolen = len(infotext)
            sociallen  = len(sociallinks)
            if sociallen > 0 and sociallen <= 10 and infolen != 0:
                try:
                    dump_data(infotext, sociallinks, imageslinks)
                except:
                    continue
            elif sociallen == 0 and infolen != 0:
                try:
                    sociallinks = ['No Available Social Media Links']
                    dump_data(infotext, sociallinks, imageslinks)
                except:
                    continue
                

    #driver.quit()


########################## Funtion for web crawling and scrapig useful data on the way ################################

def deep_link_scraping(final_links, driver):
    """
    1. It takes all the useful links from the home website as input.
    2. Enforce web crawling and extract all useful found
    3. Extract the useful data from all the useful links extracted
    """

    import re
    second_links = [] 
    for website2 in final_links:
        links2 = extract_all_links(website2, driver)
        final_links1 = find_usefull_links(links2, classmodel, class_count_vect)
        final_links2 = list(set(final_links1) - set(final_links))
        second_links += final_links2

           
    second_links = list(dict.fromkeys(second_links))
    second_links1 = find_usefull_links(second_links, classmodel, class_count_vect)
    second_links2 = []
    for link in second_links1:
        if re.search('#', link):
            x = re.search('#', link)
            link = link[:int(x.span()[0])]
            second_links2.append(link)
        else:
            second_links2.append(link)

    second_links2 = list(dict.fromkeys(second_links2))
    for final_link in second_links2:
        tags = extract_all_tags(final_link, driver)
        if len(tags) != 0:
            final_tags = find_usefull_tags(tags, tagmodel, tag_count_vect)
            if len(final_tags) != 0:
                scrape_data(final_link, final_tags, driver)
            else:
                scrape_data_tag(final_link, driver)
        else:
            scrape_data_tag(final_link, driver)
    return second_links2


################### Function to scrape data for the useful extracted from home page ###############

def link_scraping(final_links, driver):
    """
    It takes useful links as an input and calls the function scrape_data or scrape_data_tag on the basis if useful tags are received
    """

    for final_link in final_links:
        tags = extract_all_tags(final_link, driver)
        if len(tags) != 0:
            final_tags = find_usefull_tags(tags, tagmodel, tag_count_vect)
            if len(final_tags) != 0:
                print('Extracting(classname): ', final_link)
                scrape_data(final_link, final_tags, driver)
            else:
                print('Extracting(tag): ', final_link)
                scrape_data_tag(final_link, driver)
        else:
            print('Extracting(tag): ', final_link)
            scrape_data_tag(final_link, driver)


############################ Sorting Data ###############################

def extract_name(info):
    from nameparser.config import Constants
    constants = Constants()
    constants.titles.add('Shri','Smt')
    from nameparser import HumanName
    name = HumanName(info,constants=constants)
    if name.middle != '':
        fullname = name.first + ' ' + name.middle + ' ' + name.last
    else:
        fullname = name.first + ' ' + name.last
    return(fullname, name)

def extract_salutaion(info):
    import re
    salutation = ''
    remove = []
    salutations = ["Master",'Shri','Smt',"Mr","Miss","Ms","Mrs","Mx","Sir","Gentleman","Sire","Mistress","Madam","Ma'm","Dame","Lord","Lady","Esq"
     ,"Excellency","His Honour","Her Honour","The Honourable","The Right Honourable","Hon","The Most Honourable","Dr","Professor"
     ,"QC","CI","Counsel","SCI","Senoir Counsel","Eur Ing","Chancellor","Vice-Chancellor","Principal","Warden"
     ,"Dean","Regent","Rector","Provost","Director","Chief Executive","His Holiness","His All Holiness","His Excellency"
     ,"His Most Eminent Highness","His Eminence","Most Reverend Eminence","The Most Reverend","His Grace","The Right Reverend"
     ,"The Reverend","Reverand","Rev","Revd","His Lordship","Elder","Rabbi","Cantor","Chief Rabbi"
     ,"Grand Rabbi","Rebbetzin","Imam","Shaikh","Shaykh","Mufti","Hafiz","Qari","Mawlana","Haji","Sayyid","Sharif","Eminent"
     ,"Venerable", 'HER EXCELLENCY', 'Her Excellency',"master","mr","miss","ms","mrs","mx","sir","gentleman","sire","mistress","madam","ma'm","dame","lord","lady","esq"
     ,"excellency","his honour","her honour","the honourable","the right honourable","hon","the most honourable","professor"
     ,"qc","ci","counsel","sci","senoir counsel","eur ing","chancellor","vice-chancellor","warden"
     ,"dean","regent","rector","provost","director","chief executive","his holiness","his all holiness","his excellency"
     ,"his most eminent highness","his eminence","most reverend eminence","the most reverend","his grace","the right reverend"
     ,"the reverend","reverand","rev","revd","his lordship","elder","rabbi","cantor","chief rabbi"
     ,"grand rabbi","rebbetzin","imam","shaikh","shaykh","mufti","hafiz","qari","mawlana","haji","sayyid","sharif","eminent"
     ,"venerable", 'her excellency', 'her excellency',"MASTER","MR","MISS","MS","MRS","MX","SIR","GENTLEMAN","SIRE","MISTRESS","MADAM","MA'M","DAME","LORD","LADY","ESQ"
     ,"EXCELLENCY","HIS HONOUR","HER HONOUR","THE HONOURABLE","THE RIGHT HONOURABLE","HON","THE MOST HONOURABLE","HIS HOLINESS","HIS ALL HOLINESS","HIS EXCELLENCY"
     ,"HIS MOST EMINENT HIGHNESS","HIS EMINENCE","MOST REVEREND EMINENCE","THE MOST REVEREND","HIS GRACE","THE RIGHT REVEREND"
     ,"THE REVEREND","REVERAND","REV","REVD","HIS LORDSHIP","ELDER","RABBI","CANTOR","CHIEF RABBI"
     ,"GRAND RABBI","REBBETZIN","IMAM","SHAIKH","SHAYKH","MUFTI","HAFIZ","QARI","MAWLANA","HAJI","SAYYID","SHARIF","EMINENT"
     ,"VENERABLE", 'HER EXCELLENCY', 'HER EXCELLENCY', 'HIS HIGHNESS', 'HER HIGHNESS', 'SHEIKH']
    for word in salutations:
        if re.search(word, info):
            salutation = "| ".join((salutation, word))
        else:
            continue
    return(salutation)

def extract_designation(info):
    import re
    designation = ''
    removeD = []
    designations = ['Minister', 'Ministry', 'Secretary', 'Cabinet', 'minister', 'ministry', 'secretary', 'cabinet',
                   'MINISTER', 'MINISTRY', 'SECRETARY', 'CABINET','Department', 'DEPARTMENT', 'Secretária', 'Secretário',
                    'Ministra', 'Ministro', 'Primeiro']
    for word in designations:
        if re.search(word, info):
            designation = " ".join((designation, info))
        else:
            continue
    return(designation)

def sort_data(infotext):
    salutation = ''
    desig = ''
    for info in infotext:
        try:
            if extract_name(info) == None:
                continue              
            else:
                fullname, namelist = extract_name(info)
                break
        except:
            fullname = ""
            namelist = None
            continue
        
    for info in infotext:
        try:
            if extract_salutaion(info) == None:
                continue
            else:
                salutation = extract_salutaion(info)
                break
        except:
            continue
                
    for info in infotext:
        try:
            if extract_designation(info) == None:
                continue
            else:
                designation = extract_designation(info)
                desig = "| ".join((desig, designation))
                
        except:
            continue
            
    return(fullname,salutation,desig, namelist)

def dumpintoexcel(fullname, salutation, designation, namelist, sociallinks, countries, imagelinks, last_updated):
    try:
        from genderize import Genderize
        x = Genderize().get([namelist.first])
        for y in x:
            if y['gender'] != None or y['gender'] != '':
                Gender = y['gender']
            else:
                Gender = 'Unknown'
    except:
        Gender = 'Unknown'
    
    
    links = ','.join([str(elem) for elem in sociallinks])
    images = ','.join([str(elem) for elem in imagelinks])
    if namelist:
        first_name = namelist.first
        middle_name = namelist.middle
        last_name = namelist.last
    else:
        first_name = ""
        middle_name = ""
        last_name = ""

    infotext = [{
        'Country': countries[0],
        'Full Name': fullname,
        'First Name': first_name,
        'Middle Name': middle_name,
        'Last Name': last_name,
        'Gender': Gender,
        'Title': salutation,
        'Designation': designation,
        'Contact': links,
        'Images': images,
        'Last Updated': last_updated,
    }]
    keys = ['Country','Full Name','First Name','Middle Name','Last Name','Gender','Title', 'Designation', 'Contact', 'Images', 'Last Updated']
    
    with open('ScrappedData/PoliticalLeaders.csv','a') as dept:
        writer = csv.DictWriter(dept, fieldnames=keys)
        writer.writerows(infotext)

def clean_data(countries):
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
    with open('ScrappedData/Intermediate.csv', 'r') as rawfile:
        for row in rawfile:
            infotext = []
            sociallinks = []
            imagelinks = []
            listrow = row.split(',')
            for li in listrow:
                if re.search('http', li):
                    if re.search(r'\.jpg|\.png|\.jpeg|\.svg', li):
                        imagelinks.append(li)

                    elif re.search(r'instagram|twitter|youtube|linkedin|facebook|mail', li):
                        sociallinks.append(li)
                else:
                    infotext.append(li)
            
            if infotext:
                fullname,salutation,designation, namelist = sort_data(infotext)
            
            if len(fullname) != 0:
                dumpintoexcel(fullname, salutation, designation, namelist, sociallinks, countries, imagelinks, dt_string)
            else:
                continue
