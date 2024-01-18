import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import shutil
from reportlab.platypus import SimpleDocTemplate, Image, PageBreak
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A1
from Variables import *
from selenium.common.exceptions import NoSuchElementException

class Lesson:
    def __init__(self, title,topic,link):
        self.title = title
        self.topic = topic
        self.link = link

options = webdriver.ChromeOptions();
options.add_experimental_option("detach", True);
# options.add_argument("--start-maximized");
# options.add_argument("--window-size=1612,882")
driver = webdriver.Chrome(options=options);

def exportarPaginas(folder,subfolder):
    currentSlide = driver.find_element(By.XPATH,'//*[@id="pageNumberClone"]');
    allSlides = driver.find_elements(By.CSS_SELECTOR,'.page[data-page-number]');

    if not os.path.exists(courseFolderName): 
        os.mkdir(courseFolderName);
            
    if not os.path.exists(courseFolderName + '/' + folder): 
        os.mkdir(courseFolderName + '/' + folder);
    
    if not os.path.exists(courseFolderName + '/' + folder + '/images'): 
        os.mkdir(courseFolderName + '/' + folder + '/images');
    
    if not os.path.exists(courseFolderName + '/' + folder + '/' + subfolder): 
        os.mkdir(courseFolderName + '/' + folder + '/' + subfolder);
    
    doc = SimpleDocTemplate(courseFolderName + '/' + folder + '/' + subfolder + '/AllPages.pdf', pagesize = A1)
    parts = [];

    for index, slide in enumerate(allSlides):
        currentSlide.clear();
        currentSlide.send_keys(index+1)
        currentSlide.send_keys(Keys.RETURN);
         
        # if index > 0:
        #     parts.append(PageBreak());

        imagePath = courseFolderName + '/' + folder + '/images/page '+str(index+1)+'.png';
        slide.screenshot(imagePath);
        parts.append(Image(imagePath));
        time.sleep(1)
    
    doc.build(parts)
    shutil.rmtree(courseFolderName + '/' + folder + '/images');

def getAllStepsFromCourse():
    listSlideLinks = [];

    driver.get(courseURL);
    time.sleep(2)
    arrowList = driver.find_elements(By.CSS_SELECTOR,'.drop-list.fa.fa-chevron-down');
    for el in arrowList:
        driver.execute_script("arguments[0].click();", el)
    
    allTitlesAndTopics = driver.find_elements(By.CSS_SELECTOR,'div .lesson');

    for titleOrTopic in allTitlesAndTopics:
        elTitle = titleOrTopic.find_element(By.CSS_SELECTOR,'h4>a');
        title = elTitle.get_attribute("text").replace(".", "").replace("/", "");
        # Ignora o title se estiver na lista
        if title not in titlesToIgnore:
            allTopicsByTitle = titleOrTopic.find_elements(By.CSS_SELECTOR,'li>span>a');
            for el in allTopicsByTitle:
                topic = el.get_attribute("title").replace(".", "").replace("/", "");
                if topic not in topicsToIgnore:
                    lesson = Lesson(title,
                                    topic,
                                    el.get_attribute("href")
                                    )
                    listSlideLinks.append(lesson);

    for el in listSlideLinks:
        driver.get(el.link);
        try:
            fullScreenHref = driver.find_element(By.XPATH, '//a[contains(@class, "fullscreen-mode")]').get_attribute("href");
        except NoSuchElementException:
            continue
        driver.get(fullScreenHref);
        time.sleep(2)
        exportarPaginas(el.title, el.topic);


driver.get('https://focusonforce.com/login/');

cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)

getAllStepsFromCourse();
