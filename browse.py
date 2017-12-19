
from selenium import webdriver

#Following are optional required
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common import action_chains, keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time, re, os
from random import randint, random  # this ONLY imports the randint function from the random module. 

# For Tor
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


# Enum class
class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

# Bet types enum
BROWSERS = Enum(["CHROME", "FIREFOX", "TOR"])



# IMPORTANTISIMO!!!!  If selenium crashing and can't find profile might be because tmp folder is clogged up.  
# Make sure to empty the folder below from tmie to time
# C:\cygwin64\tmp
class Browse:
	def __init__(self, browser, base_url, real_ip="0.0.0.0"):
		self.base_url = base_url

		# OMG I think I know the answer why this wasn't working.  The Options / Profile you get must be in a different directory 
		# than the one Selenium is trying to load!!!!!
		# SEE: http://stackoverflow.com/questions/26886215/selenium-chrome-failed-to-start-when-using-options
		# REVISION, The above may not be the main issue, the MAIN issue is that you need to ensure Chrome has
		# FULLY shut down!!!  Can do this by using windows Process Explorer search to see if the profile
		# folder is being accessed by anything.  That Chrome.exe hitting the process folder is the culprit
		# SHUT IT DOWN, and in the future make sure that this program properly QUITS / CLOSES Chromedriver!!
		# http://stackoverflow.com/questions/21320837/release-selenium-chromedriver-exe-from-memory
		if browser == BROWSERS.CHROME:
			# service = service.Service(r'C:/chromedriver_win32/chromedriver.exe')
			# service.start()

			# username = os.getenv("USERNAME")
			# capabilities = {r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe': 'user-data-dir=C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data'}
			# driver = webdriver.Remote(service.service_url, capabilities)
			# driver.get('http://www.google.com/xhtml');
			# time.sleep(5) # Let the user actually see something!
			# driver.quit()

			# WORKING!!!  Now have real chrome profile!!
			username = os.getenv("USERNAME")
			# print(username)
			# userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data"
			options = webdriver.ChromeOptions()
			# options.add_argument("user-data-dir={}".format(userProfile))
			options.binary_location = r'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
			# options.add_argument("user-data-dir=C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data Selenium") #Path to your chrome profile
			options.add_argument("user-data-dir=C:\\chromedriver_win32\\User Data Selenium") #Path to your chrome profile
			# service_log_path = "{}/chromedriver.log".format(outputdir)
			# service_args = ['--verbose']
			# add here any tag you want.
			options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection"])
			# chromedriver = "C:\Python27\chromedriver\chromedriver.exe"
			chromedriver = r'C:/chromedriver_win32/chromedriver.exe'
			# os.environ["webdriver.chrome.driver"] = chromedriver
			self.driver = webdriver.Chrome(executable_path=chromedriver, 
				chrome_options=options)
				# ,
				# service_args=['--verbose',])#'--log-path=/dev/null'])

			# OG CHROME LAUNCH CODE. 
			# self.driver = webdriver.Chrome(executable_path=r'C:/chromedriver_win32/chromedriver.exe')#, chrome_options=chop)
		elif browser == BROWSERS.FIREFOX:
			ff_binary = r"C:/Program Files (x86)/Mozilla Firefox/firefox.exe"
			# if os.path.exists(ff_binary) is False:
			# 	raise ValueError("The ff_binary path to Tor firefox does not exist.")
			# ff_profile = r"C:/Users/Andres/Desktop/Tor Browser2/Browser/TorBrowser/Data/Browser/profile.default"
			# ff_profile = r"C:/Users/Andres/Desktop/Tor Browser2/Browser/TorBrowser/Data/Browser/u6gtxx2s.tortest"
			ff_profile = r"C:/Users/Andres/AppData/Roaming/Mozilla/Firefox/Profiles/f1luh6ea.default"
			proxy = None
			binary = FirefoxBinary(ff_binary)
			profile = FirefoxProfile(ff_profile)
			self.driver = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary, proxy=proxy)
			time.sleep(5)
		elif browser == BROWSERS.TOR:
			tor_binary = r"C:/Users/Andres/Desktop/Tor Browser2/Browser/firefox.exe"
			# if os.path.exists(tor_binary) is False:
			# 	raise ValueError("The tor_binary path to Tor firefox does not exist.")
			# tor_profile_path = r"C:/Users/Andres/Desktop/Tor Browser2/Browser/TorBrowser/Data/Browser/profile.default"
			tor_profile_path = r"C:/Users/Andres/Desktop/Tor Browser2/Browser/TorBrowser/Data/Browser/u6gtxx2s.tortest"
			proxy = None
			ff_tor_binary = FirefoxBinary(tor_binary)
			ff_tor_profile = FirefoxProfile(tor_profile_path)
			self.driver = webdriver.Firefox(firefox_profile=ff_tor_profile, firefox_binary=ff_tor_binary, proxy=proxy)
			self.driver.implicitly_wait(30)
			time.sleep(5)
			urls = (
				('tor browser check', 'https://check.torproject.org/'),
				# ('ip checker', 'http://icanhazip.com')
			)
			for url_name, url in urls:
				print ("getting", url_name, "at", url)
				self.load_page_with_full_url(url)
				self.driver.implicitly_wait(30)
				if url_name == 'tor browser check':
					try:
						success_text = self.get_single_xpath_text(".//h1[contains(@class, 'on')]")
						# print(success_text)
						apparent_ip = self.get_single_xpath_text(".//strong")
						# print(apparent_ip)
						if (success_text == "Congratulations. This browser is configured to use Tor." 
							and apparent_ip != real_ip):
							print("IP properly obfuscated and browser properly configured for TOR")
					except ValueError:
						print('WARNING: Did not find tor browser check page. Trying again.')
						time.sleep(30)
						# Try loading the tor check page again
						print ("getting", url_name, "at", url)
						self.load_page_with_full_url(url,3,6)
						self.driver.implicitly_wait(30)
						continue
				time.sleep(15)

		self.driver.implicitly_wait(30)
		


	# *args should be a list of the login field, the pwd field, and login button ids in that exact order
	def login(self, login_url_extension, login, password, ids):
		"""Logging in"""
		login_id, pwd_id, button_id = ids
		print("Login ID = " + login_id)
		print("PWD ID = " + pwd_id)
		print("Button ID = " + button_id)
		

		driver = self.driver
		driver.get(self.base_url + login_url_extension)
		time.sleep(randint(9, 14))
		driver.find_element_by_id(login_id).clear()
		driver.find_element_by_id(login_id).send_keys(login)
		driver.find_element_by_id(pwd_id).clear()
		driver.find_element_by_id(pwd_id).send_keys(password)
		driver.find_element_by_id(button_id).click()

	def close_current_tab(self):
		print("Closing current Tab")
		self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

	def load_page(self, url_extension, use_sleep=True):
		"""Loading Page"""
		driver = self.driver
		if use_sleep:
			time.sleep(randint(5, 10))
		driver.get(self.base_url + url_extension)
		if use_sleep:
			time.sleep(randint(8, 15))

	def check_popups_load_page(self, url_extension):
		"""Loading Page"""
		time.sleep(randint(4, 9))
		self.driver.get(self.base_url + url_extension)
		try:
			WebDriverWait(self.driver, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' +
				'confirmation popup to appear.')

			alert = self.driver.switch_to_alert()
			alert.accept()
			print ("alert accepted")
		except TimeoutException:
			print ("no alert")
		time.sleep(randint(3, 8))

	def load_browser_extension(self, unique_id, specificpage):
		"""Loading Page"""
		driver = self.driver
		time.sleep(randint(10, 15))
		driver.get('chrome-extension://'+ unique_id + '/' + specificpage)
		time.sleep(randint(8, 15))

	def click_element(self, xpath):
		driver = self.driver
		driver.find_element_by_xpath(xpath).click()
		time.sleep(randint(3,5))

	def click_element_by_element(self, element):
		element.click()
		time.sleep(randint(3,5))

	# This is effectively finding the element and hitting ENTER on it instead of clicking
	def click_element_with_enter(self, xpath):
		driver = self.driver
		driver.find_element_by_xpath(xpath).send_keys("\n")
		time.sleep(randint(3,5))

	def hover_mouse_over_element_and_click(self, xpath):
		element = self.driver.find_element_by_xpath(xpath)

		hover = ActionChains(self.driver).move_to_element(element)
		hover.perform()
		time.sleep(3)
		click = ActionChains(self.driver).click(element)
		click.perform()
		

	def send_data_to_element(self, data, xpath):
		driver = self.driver
		# driver.find_element_by_xpath(xpath).clear()
		driver.find_element_by_xpath(xpath).send_keys(data)

	def clear_element(self, xpath):
		driver = self.driver
		driver.find_element_by_xpath(xpath).clear()

	# pass in xpath with an attribute or nothing
	# This basically works the same way as overriding this function with another only taking 2 arguments
	def get_multi_element_data(self, xpath, attribute = None):
		"""Getting xpath data"""
		driver = self.driver
		results = driver.find_elements_by_xpath(xpath)

		if attribute == None:
			return results
		else:
			results_list = []
			for result in results:
				results_list.append(result.get_attribute(attribute))

			# for result_txt in results_list:
			# 	print(result_txt)

			return results_list

	# # HAVE A FEELING THIS MIGHT NOT ACTUALLY WORK LIKE THIS, JUST USE ABOVE FUNCTION AND PUT [0] at the end
	# # pass in xpath with an attribute or nothing
	# # This basically works the same way as overriding this function with another only taking 2 arguments
	def get_single_element_by_xpath(self, xpath):
		"""Getting xpath data"""
		driver = self.driver
		result = driver.find_element_by_xpath(xpath)

		return result

	# pass in xpath with an attribute as well
	def get_single_xpath_text(self, xpath):
		"""Getting xpath data"""
		driver = self.driver
		return driver.find_element_by_xpath(xpath).text

	# pass in xpath with an attribute as well
	def get_multi_xpath_text(self, xpath):
		"""Getting xpath data"""
		driver = self.driver
		results = driver.find_elements_by_xpath(xpath)
		
		if not results:
			return None
		results_list = []
		for result in results:
			results_list.append(result.text)
		return results_list

	def get_current_url(self):
		driver = self.driver
		print(driver.current_url)
		print(self.driver.current_url)
		# return driver.current_url

	def find_and_click_element_by_link_text(self, text):
		element = self.driver.find_element_by_link_text(text)
		element.click()


	def find_and_click_element_by_partial_link_text(self, text):
		element = self.driver.find_element_by_partial_link_text(text)
		element.click()
		

	def press_enter(self, xpath):
		self.driver.find_element_by_xpath(xpath).send_keys(Keys.RETURN)

	def press_down_arrow(self, xpath):
		self.driver.find_element_by_xpath(xpath).send_keys(Keys.ARROW_DOWN)		

	def driver_iframe_switch(self, iframe_index = None, iframe_element = None):
		if iframe_index != None:
			print("Switching to iframe based on index")
			self.driver.switch_to.frame(iframe_index)

		if iframe_element != None:

			print("Switching to iframe based on element")
			# self.driver.switch_to.frame(self.driver.find_element_by_xpath("//*[@id='c-side']/div/div[2]/iframe"))
			# frame = self.driver.find_element_by_xpath(iframe_element)
			# self.driver.switch_to.frame(frame.get_attribute("cd_frame_id"))
			self.driver.switch_to.frame(iframe_element)
		
		# # TEST
		# name = self.get_single_xpath_text(".//span[@class='personName ng-binding ng-scope']")
		# print("Name:  " + name)


	def driver_switch_to_default_content(self):
		self.driver.switch_to.default_content()



	# ONe WILD idea for a solution to Connectifier invisible links:
	# 1) http://stackoverflow.com/questions/27927964/selenium-element-not-visible-exception

	def find_element_in_developer_console(self, xpath):

		# action = ActionChains(self.driver)

		# print("Trying to open dev console")
		# # open up the developer console, mine on MAC, yours may be diff key combo
		# action.send_keys(Keys.CONTROL + Keys.SHIFT + 'i')
		# action.perform()
		# time.sleep(5)
		# # this below ENTER is to rid of the above "i"
		# action.send_keys(Keys.ENTER)
		# # inject the JavaScript...
		# print("Trying to inject JavaScript click???")
		# # action.send_keys("document.querySelectorAll('" + search_string + "')[1].click()" + keys.Keys.ENTER)
		# action.send_keys("document.querySelectorAll('span.gray-box-clickable.ng-scope')[1].click()" + keys.Keys.ENTER)

		# action.perform()

		print("Trying execute script")
		# ele = self.get_single_element_by_xpath(".//span[@class='gray-box-clickable ng-scope']");
		ele = self.get_single_element_by_xpath(xpath);
		self.driver.execute_script('arguments[0].setAttribute("style", "height: auto; visibility: visible;")', ele)

		print("Alt approach")
		elem = self.driver.find_element_by_css_selector("span.gray-box-clickable.ng-scope")
		time.sleep(3)
		elem[0].click()

		# Format
		# ele = get_element_by_xpath('//button[@id="xyzw"]');
		# drv.execute_script('arguments[0].setAttribute("style", "color: yellow; border: 2px solid yellow;")', ele)

		# self.driver.execute_script("document.getElementsByClassName('classname')[0].style.visibility='visible'")