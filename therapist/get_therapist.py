from bs4 import BeautifulSoup
import requests


def name_and_status(source_code):
    try:
        name = []
        status = []
        
        full_soup = BeautifulSoup(source_code.text, 'lxml')
        name_and_status_div = full_soup.find_all('div', class_='template-directory__info')
        

        for item in name_and_status_div:
            item = item.text
            item = item.strip()
            item = item.split("\n\n\n")
            item = [b.strip() for b in item]
            name.append(item[0])
            status.append(item[1])

        name = name[0]
        status = status[0]
    except:
        name = "Nil" 
        status = "Nil"
    
    return name, status

def get_phone_number(source_code):
    try:
        full_soup = BeautifulSoup(source_code.text, 'lxml')
        div_soup = full_soup.find_all('dl', class_='template-directory__contact-info')

        phone_number = [a.text.strip().split("\n") for a in div_soup][0][1]
    except:
        phone_number = 'Nil'
    
    return phone_number


def get_other_details(source_code):
    try:
        full_soup = BeautifulSoup(source_code.text, 'lxml')
        
        try:
            job_title = full_soup.find_all('h2', class_='directory-section__title')
            job_title = [a.text.strip() for a in job_title][0]
        except:
            job_title = "Nil"
        
        try:
            pricing = full_soup.find_all('div', class_='directory-section__price')
            pricing = [a.text.strip() for a in pricing][0]
        except:
            pricing = "Nil"
        
        try:
            url_link = full_soup.find_all('div', class_='directory-section__address content')
            url_link = [a.text.strip() for a in url_link][0]
        except:
            url_link = 'Nil'

        try:
            address = full_soup.find_all('div', class_='directory-section__address')
            address = [a.text.strip() for a in address][0]
        except:
            address = 'Nil'
        
        try:
            profile_img = full_soup.find_all('div', class_='media template-directory__image')[0].find("img")
            profile_img = profile_img['src']
        except:
            profile_img = 'Nil'
        
        try:
            number_code = full_soup.find_all('div', class_='template-directory__role')[0].find("img")
            number_code = number_code['src']
            number_code = number_code.split("=")
            number_code = [a.split("&")[0] for a in number_code][1]
        except:
            number_code = 'Nil'
        
        
    except:
        pass
    
    return job_title, pricing, url_link, address, profile_img, number_code



def process_sorce_code(source_code):
    full_soup = BeautifulSoup(source_code.text, 'lxml')
    div_soup = full_soup.find_all('div', class_='directory-section__body')


    soup = []
    for item in div_soup:
        review = item.find_all('div', class_="content")

        for c in review:
            soup.append(c)
        
    soup = soup[0]
    
    for span_tags in soup.findAll('span'):
        span_tags.unwrap()
    
    
    return soup



def change_soup_to_text(soup):
    try:
        text = soup.get_text()

        text_details = text.split("\n\n")

        key = []
        value = []
        untouched_text = text_details[-1]
        for item in text_details:
            index = text_details.index(item)


            if index % 2 != 1:
                item = item.strip()
                key.append(item)
            else:
                value.append(item)

        key.pop(-1)


        untouched_text = untouched_text.split("\n")
        key1 = []
        value1 = []
        for item in untouched_text:
            index = untouched_text.index(item)

            if index % 2 != 1:
                key1.append(item)
            else:
                value1.append(item)

        values = value+value1
        keys = key+key1

        key_value = dict(zip(keys,values))

        key_value.pop("Availability")
        key_value.pop("Practice description")
        key_value.pop("How I deliver therapy")
    except:
        pass
    
    return key_value
    



def get_details_of_therapist(profile_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    
    
    source_code = requests.get(profile_url, headers=headers)
    
    name, status = name_and_status(source_code)
    phone_number = get_phone_number(source_code)
    job_title, pricing, url_link, address, profile_img, number_code = get_other_details(source_code)
    
    

    details_dict = {"name":name, "status":status,"phone_number":phone_number,
                    "job_title":job_title, "pricing":pricing, "url_link":url_link,
                    "address":address, "profile_img":profile_img, "number_code":number_code } 

    
    soup = process_sorce_code(source_code)
    key_value = change_soup_to_text(soup)


    dict_record = {**details_dict, **key_value}
    
    return dict_record


# profile_url = "https://www.bacp.co.uk/profile/3325be08-b041-e911-a95f-000d3aba65fd/therapist?location=Hertford"
# details_dict = get_details_of_therapist(profile_url)
# print(details_dict)