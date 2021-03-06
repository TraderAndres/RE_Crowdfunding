import browse
import time
import RE_Crowdfunding
import datetime

class RealtyShares:
	def __init__(self, selenium_session, name="RealtyShares", login_id='', password='', url="https://www.realtyshares.com",
				 login_url="https://www.realtyshares.com/login",
				 current_offerings_url = "https://www.realtyshares.com/investments"):
		self.selenium_session = selenium_session
		self.name = name
		self.url = url
		self.login_url = login_url
		self.current_offerings_url = current_offerings_url
		self.login_id = login_id
		self.password = password

		# Array to store all current offering URLS
		self.current_offering_urls = []
		#TODO: This should eventually load existing deals from "database" - will need to create an input under __init__
		self.current_deals = []

	def login(self):
		# Load login page.
		self.selenium_session.load_page(self.login_url)

		# Fill in Login ID

		# Fill in pw


		# allow enough time to log in manually
		seconds = 10
		print("Alloting {} seconds to log in".format(seconds))
		while seconds > 0:
			print("{} seconds left".format(seconds))
			time.sleep(1)
			seconds -= 1

	def get_current_offering_urls(self):
		# This function just goes through the page and puts all the URLs into an array
		# Load current offerings page.
		self.selenium_session.load_page(self.current_offerings_url)
		print("Getting current offering URLs for {} ".format(self.name))
		current_offerings_urls = []

		try:
			# Check what the button says first.  If it says "learn More" then it's investable
			# This feels fucked up but should get all deal URLS with a "learn More" button enabled
			current_offerings_urls = self.selenium_session.get_multi_element_data(
				"//*[@class='InvestmentsPage__investmentsListItems']//button[text()='Learn More']//ancestor::*[@class = 'RshPropertyCard__propertyCardContentWrapper']/div[1]/a[1]", "href")

			# this converts the list to a set and back to a list.
			# Purpose is that set can only have distinct objects so this removes dupes
			current_offerings_urls = list(set(current_offerings_urls))

		except:
			current_offerings_urls = None

		print("Found a total of {} URLs".format(len(current_offerings_urls)))

		return current_offerings_urls

	def get_funded_offering_urls(self):
		# This function just goes through the page and puts all the URLs into an array
		# Load current offerings page.
		self.selenium_session.load_page(self.current_offerings_url)


	def get_deal_details(self, deal_url):
		# This function just goes through the page and puts all the URLs into an array
		# Load current offerings page.
		self.selenium_session.load_page(deal_url)

		# Create Temp Variables to store data
		# HEADER INFO
		temp_title = ''
		temp_summary = ''
		temp_location = ''
		temp_deal_url = deal_url

		# SUMMARY TABLE
		temp_target_irr = ''
		temp_fund_size = ''

		temp_investment_type = ''  # This means Direct investment or SPV
		temp_sponsor = ''  # This will be a Sponsor type
		temp_point_of_contact = ''  # this will be a DecisionMaker type
		temp_property_images = []

		# DEAL NUMBERS
		# Return Projections

		temp_upside_irr = 0.0
		temp_target_equity_multiple = None
		temp_target_investment_period = 0
		temp_target_project_level_returns = None  # how is this different than IRR?
		temp_target_avg_cash_yield = 0.0

		temp_investment_profile = ''
		temp_min_investment = ''
		temp_offers_due = None		# datetime.time(0,0,0)
		temp_funds_due = None		# datetime.time(0,0,0)
		temp_property_type = ''
		temp_distribution_period = ''
		temp_distribution_commencement = ''
		temp_property_closing_date = None	# datetime.time(0,0,0)
		# Property Details
		temp_purchase_price = 0
		temp_percent_funded = 0.0
		temp_price_per_sqft = 0.0
		temp_sponsor_coinvestment = ''
		temp_sponsor_experience = ''

		# THE FINANCIAL SUMMARY SECTION ------
		# DISTRIBUTION STRUCTURE (AKA Distribution Waterfall)
		temp_waterfall_list = []
		temp_waterfall_str = ''

		# DEBT DETAILS
		temp_debt_service_coverage_ratio = 0.0
		temp_loan_to_total_cost = 0.0
		temp_loan_interest_rate = 0.0
		temp_loan_amortization = 0
		temp_loan_term = 0

		# CAPITAL STACK
		temp_gp_equity = 0
		temp_lp_equity = 0
		temp_senior_debt = 0
		temp_total_capital_stack = temp_gp_equity + temp_lp_equity + temp_senior_debt


		print("Getting Deal Details for: {} ".format(deal_url))


		# =============================
		# HEADER
		# =============================
		# Title
		try:
			temp_title = self.selenium_session.get_single_xpath_text(
				"//*[@class='RshDashboardHeadline__themeDefault RshDashboardHeadline__headline RshHeadline__headline RshHeadline__headlineH2 RshHeadline__textAlignLeft']")
			print("Title: {}".format(temp_title))
		except:
			temp_title = None

		# Summary Text
		try:
			summary_array = self.selenium_session.get_multi_element_data(
				"//*[@class='RshDealPageV2Card__dealCard' and child::div[text()='Investment Overview']]//p", "text")
			for paragraph in summary_array:
				temp_summary += paragraph
			print("Summary: {}".format(temp_summary))
		except:
			temp_summary = None

		# Property images (pictures)
		try:
			pics = self.selenium_session.get_multi_element_data("//*[@class='RshResponsiveCarousel__carouselSlider']//img", 'src')
			for pic in pics:
				temp_property_images.append({'url': pic})
		except:
			print("error loading image URLs")

		# =============================
		# SUMMARY TABLE
		# =============================
		# Targeted Investor IRR
		try:
			# temp_target_irr = self.selenium_session.get_single_xpath_text(
			# 	"//*[@class='summary-table']//td[preceding-sibling::td/strong='Targeted Investor IRR:']")
			print("Target IRR: {}".format(temp_target_irr))
		except:
			temp_target_irr = None

		# Fund Size
		try:
			# temp_fund_size = self.selenium_session.get_single_xpath_text(
			# 	"//*[@class='summary-table']//td[preceding-sibling::td/strong='Fund Size:']")
			print("Target Fund Size: {}".format(temp_fund_size))
		except:
			temp_fund_size = None

		# Target Equity Multiple
		try:
			# temp_target_equity_multiple = self.selenium_session.get_single_xpath_text(
			# 	"//*[@class='summary-table']//td[preceding-sibling::td/strong='Targeted Equity Multiple:']")
			print("Target Equity Multiple: {}".format(temp_target_equity_multiple))
		except:
			temp_target_equity_multiple = None

		# Target Investment Period
		try:
			temp_target_investment_period = self.selenium_session.get_single_xpath_text(
				"//*[@class='RshStats__statsItem']/div[following-sibling::div[text()='Maturity']]")
			print("Target Investment Period: {}".format(temp_target_investment_period))
		except:
			temp_target_investment_period = None

		# Investment Profile
		try:
			# temp_investment_profile = self.selenium_session.get_single_xpath_text(
			# 	"//*[@class='summary-table']//td[preceding-sibling::td/strong='Investment Profile:']")
			print("Investment Profile: {}".format(temp_investment_profile))
		except:
			temp_investment_profile = None

		# Minimum Investment
		try:
			temp_min_investment = str(float(self.selenium_session.get_single_xpath_text(
				"//*[@class='RshStats__statsItem']/div[following-sibling::div[text()='Minimum']]/span[@class='RshStatsFigureNumber']"))*1000)
			print("Min Investment: {}".format(temp_min_investment))
		except:
			temp_min_investment = None

		# Target Project Level IRR (temp_target_project_level_returns)
		try:
			# temp_target_project_level_returns = self.selenium_session.get_single_xpath_text(
			# 	"//*[@class='summary-table']//td[preceding-sibling::td/strong='Targeted Project Level IRR:']")
			print("Target Project Level IRR: {}".format(temp_target_project_level_returns))
		except:
			temp_target_project_level_returns = None

		# Targeted average cash yield
		try:
			temp_target_avg_cash_yield = self.selenium_session.get_single_xpath_text(
				"//*[@class='RshStats__statsItem']/div[following-sibling::div[text()='Annual Interest']]/span[@class='RshStatsFigureNumber']")/100
			print("Targeted Average Cash Yield: {}".format(temp_target_avg_cash_yield))
		except:
			temp_target_avg_cash_yield = None


		# Property Type
		try:
			temp_property_type = self.selenium_session.get_single_xpath_text(
				"//*[@class='RshDetailsList__item']/div[preceding-sibling::div='Property Type']")
			print("Property Type: {}".format(temp_property_type))
		except:
			temp_property_type = None

		# Offers Due
		try:
			# temp_offers_due = self.selenium_session.get_single_xpath_text(
			# 	"//*[@class='summary-table']//td[preceding-sibling::td/strong='Offers Due:']")
			print("Funds Due: {}".format(temp_offers_due))
		except:
			temp_offers_due = None

		# Funds Due
		try:
			# temp_funds_due = self.selenium_session.get_single_xpath_text(
			# 	"//*[@class='summary-table']//td[preceding-sibling::td/strong='Funds Due:']")
			print("Funds Due: {}".format(temp_funds_due))
		except:
			temp_funds_due = None

		# Distribution Period
		try:
			# temp_distribution_period = self.selenium_session.get_single_xpath_text(
			# 	"//*[@class='summary-table']//td[preceding-sibling::td/strong='Distribution Period:']")
			print("Distribution Period: {}".format(temp_distribution_period))
		except:
			temp_distribution_period = None

		# Distribution Commencement
		try:
			# temp_distribution_commencement = self.selenium_session.get_single_xpath_text(
			# 	"//*[@class='summary-table']//td[preceding-sibling::td/strong='Distribution Commencement:']")
			print("Distribution Commencement: {}".format(temp_distribution_commencement))
		except:
			temp_distribution_commencement = None

		# Property Closing Date
		try:
			# temp_property_closing_date = self.selenium_session.get_single_xpath_text(
			# 	"//*[@class='summary-table']//td[preceding-sibling::td/strong='Property Closing Date:']")
			print("Property Closing Date: {}".format(temp_property_closing_date))
		except:
			temp_property_closing_date = None

		# Purchase Price
		try:
			temp_purchase_price = self.selenium_session.get_single_xpath_text(
				"//*[@class='RshPropertyCardProgressV2__propertyCardLabelWrapper']/span[@style='float: right;']")
			print("Purchase Price: {}".format(temp_purchase_price))
		except:
			temp_purchase_price = None

		# Percent funded
		try:
			temp_percent_funded = float(self.selenium_session.get_single_xpath_text(
				"//*[@class='RshPropertyCardProgressV2__propertyCardLabelWrapper']/text()"))
			print("Percent Funded: {}".format(temp_percent_funded))
		except:
			temp_percent_funded = None

		# Sponsor Co-Investment
		try:
			# temp_sponsor_coinvestment = self.selenium_session.get_single_xpath_text(
			# 	"//*[@class='summary-table']//td[preceding-sibling::td/strong='Sponsor Co-Investment:']")
			print("Sponsor CoInvestment: {}".format(temp_sponsor_coinvestment))
		except:
			temp_sponsor_coinvestment = None

		# Sponsor Experience
		try:
			temp_sponsor_experience = self.selenium_session.get_single_xpath_text(
				"//*[@class='RshFroalaEditor__rshFroalaEditor']//strong[text()='Track Record:']/parent::p")
			print("Sponsor Experience: {}".format(temp_sponsor_experience))
		except:
			temp_sponsor_experience



		# =============================
		# THE FINANCIAL SUMMARY SECTION
		# =============================
		# Distribution Structure (aka: Distribution Waterfall)
		print('Summary Trying for Distribution Structure Table...')
		try:
			# get the title of the Distribution Waterfall
			distribution_waterfall_title = self.selenium_session.get_single_xpath_text(
				"//*[translate(text() ,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ' )='DISTRIBUTION STRUCTURE']")
			print(distribution_waterfall_title)

			# Figure out what the next line after Distribution is
			# could say:
			# Fund Details
			# Exit Summary
			# Exit Objectives Summary
			try:
				search_text = self.selenium_session.get_single_xpath_text(
					"//*[translate(text() ,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ' )='FUND DETAILS']")
			except:
				print("No FUND DETAILS found")
			try:
				search_text = self.selenium_session.get_single_xpath_text(
					"//*[translate(text() ,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ' )='EXIT SUMMARY']")
			except:
				print("No EXIT SUMMARY found")
			try:
				search_text = self.selenium_session.get_single_xpath_text(
					"//*[translate(text() ,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ' )='EXIT OBJECTIVES SUMMARY']")
			except:
				print("No EXIT SUMMARY found")


			try:
				temp_texts = self.selenium_session.get_multi_xpath_text(
					"//*[text()='" + search_text + "']/parent::p/preceding-sibling::node()")
				temp_waterfall_list = temp_texts
			except:
				print("No Distribution Structure elements found")


			# Convert the list to a string
			for item in temp_waterfall_list:
				temp_waterfall_str += item + '\n\n'

			print(temp_waterfall_str)
		except:
			print('Unable to get Distribution Structure')



		if temp_total_capital_stack > 0:
			temp_gp_equity_pct = temp_gp_equity / temp_total_capital_stack
			temp_lp_equity_pct = temp_lp_equity / temp_total_capital_stack
			temp_senior_debt_pct = temp_senior_debt / temp_total_capital_stack


		# Create a Deal Object
		deal_obj = RE_Crowdfunding.Deal(
			title=temp_title,
			summary=temp_summary,
			platform_url=self.url,
			fund_size=temp_fund_size,
			target_irr=temp_target_irr,
			target_equity_multiple=temp_target_equity_multiple,
			target_investment_period=temp_target_investment_period,
			target_project_level_returns=temp_target_project_level_returns,
			target_avg_cash_yield=temp_target_avg_cash_yield,
			investment_profile=temp_investment_profile,
			min_investment=temp_min_investment,
			offers_due=temp_offers_due,
			funds_due=temp_funds_due,
			property_type=temp_property_type,
			distribution_period=temp_distribution_period,
			distribution_commencement=temp_distribution_commencement,
			property_closing_date=temp_property_closing_date,
			purchase_price=temp_purchase_price,
			sponsor_coinvestment=temp_sponsor_coinvestment,
			sponsor_experience=temp_sponsor_experience,
			property_images=temp_property_images,
			percent_funded=temp_percent_funded,
			# Financial Summary
			temp_waterfall_distribution=temp_waterfall_str
		)

		return deal_obj
