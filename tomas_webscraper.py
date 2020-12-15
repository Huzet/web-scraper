#! python3

import requests, bs4, json, webbrowser, os.path
from os import path 
from selenium import webdriver

def get_website(prodcutURL):
    """This function pulls website HTML and Puts in JSON for FreeCodeCamp"""
    # gets html document
    res = requests.get(prodcutURL)
    #Makes sure return was valid, if not valid exits
    res.raise_for_status 
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    return soup

def top_article_fcb(soup):
    """Extracts top article from Beatiful Soup 4"""
    # Top article from FCB
    elems = soup.find_all(class_='post-card-title')
    article= elems[0].find('a')['href']
    return article

def selenium_search_yb_kalle():
    """Gets Kalles youtube top video"""
    browser = webdriver.Chrome()
    type(browser)
    browser.get('https://www.youtube.com/c/KalleHallden/videos')
    try:
        # elem = browser.find_element_by_class_name("style-scope ytd-grid-video-renderer")
        elem = browser.find_element_by_id("video-title")
        return elem.text
    except:
        print('ERROR: geting youtube Kalles latest video')
    
def initialize_json(website, article):
    """Initializes the JSON File"""
    # Puts in JSON format
    json_file = {}
    json_file[website] = article

    # write to file 
    with open('news_scrape.txt', 'w') as outfile:
        json.dump(json_file, outfile)

def put_in_json(website, article):
    """Adds new fields / updates JSON File"""
    # 1 Open File
    with open('news_scrape.txt', 'r') as outfile:
        json_file = json.load(outfile)
    json_file[website] = article

    # 2 write to File
    with open('news_scrape.txt', 'w') as outfile:
        json.dump(json_file, outfile)
    
def open_yesterday_article(website, todays_article):
    """Opens yesterdays article, if it does not exists creates new json"""
    # Checks if file exists first
    if path.exists("news_scrape.txt") == True: 
    # Then it tries to open article if no article creates one
        try:
            with open('news_scrape.txt', 'r') as json_file:
                data = json.load(json_file)
                yesterdays_article = data[website]
        except:
            put_in_json(website, todays_article)
            yesterdays_article = "new article"
    # If file does not exists it creates one
    else:
        initialize_json(website, todays_article)
        yesterdays_article = "new article"
    return yesterdays_article

def check_if_new_articles(website, todays_article, yesterdays_article, urls):
    """compares articles and prompts user if he wants to read them"""

    if todays_article == yesterdays_article:
        print('No new article in ' + website)
    else:
        print('There is a new article in ' + website + ' todays article is' + todays_article)
        user_input= input('would you like to read it? y/n \n')
        if user_input == 'y':
            webbrowser.open(urls + todays_article)
        # Updates JSON with todays article
        put_in_json(website, todays_article)
        

def main():
    # Free Code Camp
    soup = get_website('https://www.freecodecamp.org/news/')
    todays_article = top_article_fcb(soup)
    yesterdays_article = open_yesterday_article('Free_Code_Camp', todays_article)
    check_if_new_articles('Free_Code_Camp', todays_article, yesterdays_article, 'https://www.freecodecamp.org/news')

    # Kalle youtube
    todays_article = selenium_search_yb_kalle()
    yesterdays_article = open_yesterday_article('youtube_kalle', todays_article)
    check_if_new_articles('youtube_kalle', todays_article, yesterdays_article, 'https://www.youtube.com/c/KalleHallden/videos')

    # End of program
    print('end of program')

if __name__ == '__main__':
    main()





