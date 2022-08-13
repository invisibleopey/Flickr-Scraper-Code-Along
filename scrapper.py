import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
import time


def get_urls():
	#Input is a dictionary with keywords and numbers: {"pasta": 2, "tofu":2}
	user_input = input('Enter your query:')

	s = Service('/home/invisibleopey/Dataloop/Flickr Scraper Code Along/chromedriver')  #Replace the path in this line with the path to the web driver you downloaded

	options = webdriver.ChromeOptions()
	options.add_argument("start-maximized")
	options.add_argument("disable-infobars")
	options.add_argument("--disable-extensions")
	wd = webdriver.Chrome(options=options, service=s)

	# Flickr credentials
	user_email = "opey.muritala@gmail.com"
	password = "uu*&xTgS$qK,7j4"
	isloggedIn = False

	def login_to_flickr():
		wd.get("https://identity.flickr.com/")

		email_field = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.ID, "login-email")))
		email_field.send_keys(user_email)
		next_button = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.flickr-button')))
		next_button.click()
		password_field = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.ID, "login-password")))
		password_field.send_keys(password)
		login_button = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.flickr-button')))
		login_button.click()

	def get_images_from_flickr(wd, delay, max_images, search_term):
		if not isloggedIn:
			login_to_flickr()
		def scroll_down(wd):
			wd.execute_script("window.scrollBy(0,document.body.scrollHeight)")
			time.sleep(delay)

		search_field = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.ID, "search-field")))
		search_field.clear()
		search_field.send_keys(search_term)
		search_field.send_keys(Keys.ENTER)

		

		image_urls = set()
		skips = 0

		while len(image_urls) + skips < max_images:
			scroll_down(wd)
			thumbnails = wd.find_elements(By.CSS_SELECTOR, 'a.overlay')

			thumbnails_set = set(thumbnails)

			for img in thumbnails_set:
				try:
					img.click()
				except:
					continue

			image = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "main-photo")))

			if image.get_attribute('src') in image_urls:
						max_images += 1
						skips += 1
						break

			if image.get_attribute('src') and 'http' in image.get_attribute('src'):
				image_urls.add(image.get_attribute('src'))
				print(f"Found {len(image_urls)}")
			wd.execute_script("window.history.go(-1)")

		return image_urls

	query_dict = json.loads(user_input)
	returned_urls = []

	for term in query_dict:
		urls = get_images_from_flickr(wd, 5, query_dict[term], term)
		obj = {
			term: urls
		}
		returned_urls.append(obj)
		isloggedIn = True

	wd.quit()

	return returned_urls