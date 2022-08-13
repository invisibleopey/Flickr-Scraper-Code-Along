from selenium import webdriver
from selenium.webdriver.chrome.service import Service

s = Service('/home/invisibleopey/Dataloop/Flickr Scraper Code Along/chromedriver')  #Replace the path in this line with the path to the web driver you downloaded

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
wd = webdriver.Chrome(options=options, service=s)

