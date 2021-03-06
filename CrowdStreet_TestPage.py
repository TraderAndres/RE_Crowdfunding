import browse
import time
import RE_Crowdfunding
import datetime

class TEST_CrowdStreet:
	def __init__(self, selenium_session, name="CrowdStreet", login_id='', password='', url="https://www.crowdstreet.com",
				 login_url="https://app.crowdstreet.com/accounts/login",
				 current_offerings_url = "https://app.crowdstreet.com/properties/#"):
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


	def TEST_get_deal_details(self, deal_url):
		# This function just goes through the page and puts all the URLs into an array
		# Load current offerings page.
		self.selenium_session.load_page(deal_url, use_sleep=False)

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

		# KEY DEAL POINTS
		temp_key_deal_points = []

		# DEAL NUMBERS
		# Return Projections

		temp_upside_irr = 0.0
		temp_target_equity_multiple = None
		temp_target_investment_period = 0
		temp_target_project_level_returns = None  # how is this different than IRR?
		temp_target_avg_cash_yield = 0.0

		temp_investment_profile = ''
		temp_min_investment = 0.0
		temp_offers_due = datetime.time(0,0,0)
		temp_funds_due = datetime.time(0,0,0)
		temp_property_type = ''
		temp_distribution_period = ''
		temp_distribution_commencement = ''
		temp_property_closing_date = datetime.time(0,0,0)
		# Property Details
		temp_purchase_price = 0
		temp_price_per_sqft = 0.0
		temp_sponsor_coinvestment = ''
		temp_sponsor_experience = ''

		# THE INVESTMENT SECTION ------
		# INVESTMENT: Summary of Terms
			# Equity Contribution
		temp_equity_amount = 0.0
		temp_sponsor_contribution = 0.0
		temp_investor_contribution = 0.0
			# Distribution Waterfall
		temp_waterfall_list = []
		temp_waterfall_str = ''
		temp_CS_investor_target_irr = 0.0
		temp_CS_investor_equity_multiple = 0.0
			# Summary Paragraph Text
		temp_summary_paragraphs = []


		# INVESTMENT: Financials Table 1
		temp_lender = ''
		temp_loan_amount = 0.0
		temp_interest_rate = ''
		temp_financials_term = ''
		temp_financials_amortization = ''
		temp_guaranties = ''
		temp_prepayment_terms = ''
		# INVESTMENT: Financials Table 2
		temp_initial_investment = 0.0

		# INVESTMENT: Sponsor Fees
		temp_raw_sponsor_fees = ''

		# INVESTMENT: Crowdstreet Marketplace Comparison
		temp_project_target_irr = 0.0
		temp_CS_avg_target_irr = 0.0
		temp_project_target_equity_multiple = 0.0
		temp_CS_avg_equity_multiple = 0.0
		temp_project_target_hold_period = ''
		temp_CS_avg_hold_period = ''
		temp_project_sponsor_coinvest = 0.0
		temp_CS_avg_coinvest = 0.0
		temp_project_target_COC = 0.0
		temp_CS_avg_COC = 0.0
		temp_project_loan_to_cost_ratio = 0.0
		temp_CS_avg_loan_to_cost_ratio = 0.0

		# INVESTMENT: Project vs Investor Returns
		temp_project_irr = 0.0
		temp_net_investor_irr = 0.0
		temp_irr_spread = 0.0
		temp_project_equity_multiple = 0.0
		temp_net_investor_equity_multiple = 0.0
		temp_equity_multiple_spread = 0.0
		temp_project_COC = 0.0
		temp_net_investor_COC = 0.0
		temp_CAC_spread = 0.0

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

		# WATERFALL & FEE STRUCTURE



		print("Getting Deal Details for: {} ".format(deal_url))

		#
		# # =============================
		# # HEADER
		# # =============================
		# # Title
		# try:
		# 	temp_title = self.selenium_session.get_single_xpath_text("//*[@class ='detail-title']/h2")
		# 	print("Title: {}".format(temp_title))
		# except:
		# 	temp_title = None
		#
		# # Summary Text
		# try:
		# 	temp_summary = self.selenium_session.get_single_xpath_text("//*[@class='detail-title']/p/i")
		# 	print("Summary: {}".format(temp_summary))
		# except:
		# 	temp_summary = None
		#
		# # Property images (pictures)
		# try:
		# 	pics = self.selenium_session.get_multi_element_data("//*[@id='header_detail_fader']/img", 'src')
		# 	for pic in pics:
		# 		temp_property_images.append({'url': pic})
		# except:
		# 	print("error loading image URLs")
		#
		#
		# # Key Deal Points (text)
		# try:
		# 	deal_points = self.selenium_session.get_multi_element_data("//*[@class='col-lg-12' and child::h3[text()='Key Deal Points']]//li", 'text')
		# 	for point in deal_points:
		# 		temp_key_deal_points.append({'text': point})
		# except:
		# 	print("error getting Key Deal Points")
		#
		#
		# # =============================
		# # SUMMARY TABLE
		# # =============================
		# # Targeted Investor IRR
		# try:
		# 	temp_target_irr = self.selenium_session.get_single_xpath_text(
		# 		"//*[@class='summary-table']//td[preceding-sibling::td/strong='Targeted Investor IRR:']")
		# 	print("Target IRR: {}".format(temp_target_irr))
		# except:
		# 	temp_target_irr = None
		#
		# # Fund Size
		# try:
		# 	temp_fund_size = self.selenium_session.get_single_xpath_text(
		# 		"//*[@class='summary-table']//td[preceding-sibling::td/strong='Fund Size:']")
		# 	print("Target Fund Size: {}".format(temp_fund_size))
		# except:
		# 	temp_fund_size = None
		#
		# # Target Equity Multiple
		# try:
		# 	temp_target_equity_multiple = self.selenium_session.get_single_xpath_text(
		# 		"//*[@class='summary-table']//td[preceding-sibling::td/strong='Targeted Equity Multiple:']")
		# 	print("Target Equity Multiple: {}".format(temp_target_equity_multiple))
		# except:
		# 	temp_target_equity_multiple = None
		#
		# # Target Investment Period
		# try:
		# 	temp_target_investment_period = self.selenium_session.get_single_xpath_text(
		# 		"//*[@class='summary-table']//td[preceding-sibling::td/strong='Targeted Investment Period:']")
		# 	print("Target Investment Period: {}".format(temp_target_investment_period))
		# except:
		# 	temp_target_investment_period = None
		#
		# # Investment Profile
		# try:
		# 	temp_investment_profile = self.selenium_session.get_single_xpath_text(
		# 		"//*[@class='summary-table']//td[preceding-sibling::td/strong='Investment Profile:']")
		# 	print("Investment Profile: {}".format(temp_investment_profile))
		# except:
		# 	temp_investment_profile = None
		#
		# # Minimum Investment
		# try:
		# 	temp_min_investment = float(self.selenium_session.get_single_xpath_text(
		# 		"//*[@class='summary-table']//td[preceding-sibling::td/strong='Minimum Investment:']"))
		# 	print("Min Investment: {}".format(temp_min_investment))
		# except:
		# 	temp_min_investment = None
		#
		# # Target Project Level IRR (temp_target_project_level_returns)
		# try:
		# 	temp_target_project_level_returns = self.selenium_session.get_single_xpath_text(
		# 		"//*[@class='summary-table']//td[preceding-sibling::td/strong='Targeted Project Level IRR:']")
		# 	print("Min Investment: {}".format(temp_target_project_level_returns))
		# except:
		# 	temp_target_project_level_returns = None
		#
		# # Targeted average cash yield
		# try:
		# 	temp_target_avg_cash_yield = self.selenium_session.get_single_xpath_text(
		# 		"//*[@class='summary-table']//td[preceding-sibling::td/strong='Targeted Average Cash Yield:']")
		# 	print("Min Investment: {}".format(temp_target_avg_cash_yield))
		# except:
		# 	temp_target_avg_cash_yield = None
		#
		# # Property Type
		# try:
		# 	temp_property_type = self.selenium_session.get_single_xpath_text(
		# 		"//*[@class='summary-table']//td[preceding-sibling::td/strong='Property Type:']")
		# 	print("Property Type: {}".format(temp_property_type))
		# except:
		# 	temp_property_type = None
		#
		# # Offers Due
		# try:
		# 	temp_offers_due = self.selenium_session.get_single_xpath_text(
		# 		"//*[@class='summary-table']//td[preceding-sibling::td/strong='Offers Due:']")
		# 	print("Funds Due: {}".format(temp_offers_due))
		# except:
		# 	temp_offers_due = None
		#
		# # Funds Due
		# try:
		# 	temp_funds_due = self.selenium_session.get_single_xpath_text(
		# 		"//*[@class='summary-table']//td[preceding-sibling::td/strong='Funds Due:']")
		# 	print("Funds Due: {}".format(temp_funds_due))
		# except:
		# 	temp_funds_due = None
		#
		# # Distribution Period
		# try:
		# 	temp_distribution_period = self.selenium_session.get_single_xpath_text(
		# 		"//*[@class='summary-table']//td[preceding-sibling::td/strong='Distribution Period:']")
		# 	print("Distribution Period: {}".format(temp_distribution_period))
		# except:
		# 	temp_distribution_period = None
		#
		# # Distribution Commencement
		# try:
		# 	temp_distribution_commencement = self.selenium_session.get_single_xpath_text(
		# 		"//*[@class='summary-table']//td[preceding-sibling::td/strong='Distribution Commencement:']")
		# 	print("Distribution Commencement: {}".format(temp_distribution_commencement))
		# except:
		# 	temp_distribution_commencement = None
		#
		# # Property Closing Date
		# try:
		# 	temp_property_closing_date = self.selenium_session.get_single_xpath_text(
		# 		"//*[@class='summary-table']//td[preceding-sibling::td/strong='Property Closing Date:']")
		# 	print("Property Closing date: {}".format(temp_property_closing_date))
		# except:
		# 	temp_property_closing_date = None
		#
		# # Purchase Price
		# try:
		# 	temp_purchase_price = self.selenium_session.get_single_xpath_text(
		# 		"//*[@class='summary-table']//td[preceding-sibling::td/strong='Purchase Price:']")
		# 	print("Purchase Price: {}".format(temp_purchase_price))
		# except:
		# 	temp_purchase_price = None
		#
		# # Sponsor Co-Investment
		# try:
		# 	temp_sponsor_coinvestment = self.selenium_session.get_single_xpath_text(
		# 		"//*[@class='summary-table']//td[preceding-sibling::td/strong='Sponsor Co-Investment:']")
		# 	print("Sponsor CoInvestment: {}".format(temp_sponsor_coinvestment))
		# except:
		# 	temp_sponsor_coinvestment = None
		#
		# # Sponsor Experience
		# try:
		# 	temp_sponsor_experience = self.selenium_session.get_single_xpath_text(
		# 		"//*[contains(@class,'experience-label')]")
		# 	print("Sponsor Experience: {}".format(temp_sponsor_experience))
		# except:
		# 	temp_sponsor_experience

		# =============================
		# THE INVESTMENT SECTION
		# =============================
		# Summary
		# Equity Contribution
		print('Summary Trying for Equity Contribution Table...')
		try:
			# get the title of the Equity Contribution
			equity_contribution_title = self.selenium_session.get_single_xpath_text(
				"//*[translate(text() ,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ' )='EQUITY CONTRIBUTION']")
			print(equity_contribution_title)
		except:
			print('Unable to get Summary Equity Contribution Table')

		# Distribution Waterfall
		print('Summary Trying for Distribution Waterfall Table...')
		try:
			# get the title of the Distribution Waterfall
			distribution_waterfall_title = self.selenium_session.get_single_xpath_text(
				"//*[translate(text() ,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ' )='DISTRIBUTION WATERFALL']")
			print(distribution_waterfall_title)

			# Analyze the Distribution in a while loop
			i = 1
			while i < 100:
				try:
					# Build array of all the distribution details one by one
					temp_key = self.selenium_session.get_single_xpath_text(
						"//*[translate(text() ,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ' )='DISTRIBUTION WATERFALL']/parent::tr/following-sibling::tr[" + str(i) + "]/td[1]")
					temp_waterfall_list.append({temp_key: ''})
					temp_text = self.selenium_session.get_single_xpath_text(
						"//*[translate(text() ,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ' )='DISTRIBUTION WATERFALL']/parent::tr/following-sibling::tr[" + str(i) + "]/td[2]")
					temp_waterfall_list[len(temp_waterfall_list)-1][temp_key] = temp_text
					i += 1
				except:
					print("breaking out of distribution loop at step {}".format(i))
					break

			# Convert the list to a string
			for dict in temp_waterfall_list:
				for key, value in dict.items():
					temp_waterfall_str += key + ': ' + value + '\n'

			print(temp_waterfall_str)
		except:
			print('Unable to get Summary Distribution Waterfall Table')


		# Financials
		print('Financials Table 1...')
		try:
			# get the title of the 1st table
			table1_title =self.selenium_session.get_single_xpath_text("//*[@id='investment-flows']//h4[1]")
			print(table1_title)
		except:
			print('Unable to get Table Title')
		try:
			# Lender
			temp_lender = self.selenium_session.get_single_xpath_text(
				"//*[@id='investment-flows']//td[preceding-sibling::td[text()='Lender']]")
			print("Lender: {}".format(temp_lender))
		except:
			print('Unable to get Lender')
		try:
			# Loan Amount
			temp_loan_amount_ft = self.selenium_session.get_single_xpath_text(
				"//*[@id='investment-flows']//td[preceding-sibling::td[text()='Loan Amount']]")
			print("Lender: {}".format(temp_lender))
		except:
			print('Unable to get Loan Amount')
		try:
			# Interest Rate
			temp_interest_rate = self.selenium_session.get_single_xpath_text(
				"//*[@id='investment-flows']//td[preceding-sibling::td[text()='Interest Rate']]")
			print("Interest Rate: {}".format(temp_interest_rate))
		except:
			print('Unable to get Interest Rate')
		try:
			# Term
			temp_financials_term = self.selenium_session.get_single_xpath_text(
				"//*[@id='investment-flows']//td[preceding-sibling::td[text()='Term']]")
			print("Loan Term: {}".format(temp_financials_term))
		except:
			print('Unable to get Term')
		try:
			# Amortization
			temp_financials_amortization = self.selenium_session.get_single_xpath_text(
				"//*[@id='investment-flows']//td[preceding-sibling::td[text()='Amortization']]")
			print("Amortization: {}".format(temp_financials_amortization))
		except:
			print('Unable to get Amortization')
		try:
			# Guaranties
			temp_guaranties = self.selenium_session.get_single_xpath_text(
				"//*[@id='investment-flows']//td[preceding-sibling::td[text()='Guaranties']]")
			print("Guaranties: {}".format(temp_guaranties))
		except:
			print('Unable to get Guaranties')
		try:
			# Prepayment Terms
			temp_prepayment_terms = self.selenium_session.get_single_xpath_text(
				"//*[@id='investment-flows']//td[preceding-sibling::td[text()='Prepayment Terms']]")
			print("Prepayment Terms: {}".format(temp_prepayment_terms))
		except:
			print('Unable to get Prepayment Terms')

		print('Financials Table 2...')
		try:
			# get the title of the 2nd table
			table2_title =self.selenium_session.get_single_xpath_text("//*[@id='investment-flows']//h4[2]")
			print(table2_title)
			# Initial Investment
			temp_lender = self.selenium_session.get_single_xpath_text("")
			print("Lender: {}".format(temp_lender))
			# Interest Rate
		except:
			print('Unable to get Financials Table 2')


		# Sponsor Fees
		print('Sponsor Fees...')
		try:
			# Raw Sponsor Fees
			fee_lines = self.selenium_session.get_multi_element_data("//*[@id='investment-fees']//li", 'text')
			for fee in fee_lines:
				temp_raw_sponsor_fees += fee + '\n'
				print("Raw Sponsor Fees: {}".format(temp_raw_sponsor_fees))
		except:
			print('Unable to get Sponsor Fees')

		# Crowdstreet Marketplace Comparison
		print('Crowdstreet Marketplace Comparison numbers...')
		try:
			# Target IRRs
			temp_project_target_irr = self.selenium_session.get_single_xpath_text("//*[@id='investment-MPcomp']//td[preceding-sibling::td[text()='Targeted Investor IRR']][1]")
			print("Project Target IRR: {}".format(temp_project_target_irr))
			temp_CS_avg_target_irr = self.selenium_session.get_single_xpath_text("//*[@id='investment-MPcomp']//td[preceding-sibling::td[text()='Targeted Investor IRR']][2]")
			print("Crowdstreet Average IRR: {}".format(temp_CS_avg_target_irr))
			# Target Equity Multiples
			temp_project_target_equity_multiple = self.selenium_session.get_single_xpath_text("//*[@id='investment-MPcomp']//td[preceding-sibling::td[text()='Targeted Equity Multiple']][1]")
			print("Project Target Equity Multiple: {}".format(temp_project_target_equity_multiple))
			temp_CS_avg_equity_multiple = self.selenium_session.get_single_xpath_text("//*[@id='investment-MPcomp']//td[preceding-sibling::td[text()='Targeted Equity Multiple']][2]")
			print("Crowdstreet Average Equity Multiple: {}".format(temp_CS_avg_equity_multiple))
			# Target Investment Hold Period
			temp_project_target_hold_period = self.selenium_session.get_single_xpath_text("//*[@id='investment-MPcomp']//td[preceding-sibling::td[text()='Targeted Investment Hold Period']][1]")
			print("Project Target Hold Period: {}".format(temp_project_target_hold_period))
			temp_CS_avg_hold_period = self.selenium_session.get_single_xpath_text("//*[@id='investment-MPcomp']//td[preceding-sibling::td[text()='Targeted Investment Hold Period']][2]")
			print("Crowdstreet Average Hold Period: {}".format(temp_CS_avg_hold_period))
			# Sponsor co-invest
			temp_project_sponsor_coinvest = self.selenium_session.get_single_xpath_text("//*[@id='investment-MPcomp']//td[preceding-sibling::td[text()='Sponsor Co-Invest']][1]")
			print("Project Sponsor Co-Invest: {}".format(temp_project_sponsor_coinvest))
			temp_CS_avg_coinvest = self.selenium_session.get_single_xpath_text("//*[@id='investment-MPcomp']//td[preceding-sibling::td[text()='Sponsor Co-Invest']][2]")
			print("Crowdstreet Average Co-Invest: {}".format(temp_CS_avg_coinvest))
			# Targeted Cash on Cash return
			temp_project_target_COC = self.selenium_session.get_single_xpath_text("//*[@id='investment-MPcomp']//td[preceding-sibling::td[text()='Targeted Average Annual Cash-On-Cash Return']][1]")
			print("Project Target Cash-on-Cash Return: {}".format(temp_project_target_COC))
			temp_CS_avg_COC = self.selenium_session.get_single_xpath_text("//*[@id='investment-MPcomp']//td[preceding-sibling::td[text()='Targeted Average Annual Cash-On-Cash Return']][2]")
			print("Crowdstreet Average Cash-on-Cash Return: {}".format(temp_CS_avg_COC))
			# Loan-to-Cost (LTC) Ratio
			temp_project_loan_to_cost_ratio = self.selenium_session.get_single_xpath_text("//*[@id='investment-MPcomp']//td[preceding-sibling::td[text()='Loan-To-Cost (LTC) Ratio']][1]")
			print("Project Loan to Cost Ratio: {}".format(temp_project_loan_to_cost_ratio))
			temp_CS_avg_loan_to_cost_ratio = self.selenium_session.get_single_xpath_text("//*[@id='investment-MPcomp']//td[preceding-sibling::td[text()='Loan-To-Cost (LTC) Ratio']][2]")
			print("Crowdstreet Average Loan to Cost Ratio: {}".format(temp_CS_avg_loan_to_cost_ratio))
		except:
			print('Unable to get Crowdstreet Marketplace Comparison')

		# Project vs Investor Returns
		try:
			# IRRs
			temp_project_irr = self.selenium_session.get_single_xpath_text("//*[@id='investment-project']//td[preceding-sibling::th[text()='IRR']][1]")
			print("Project IRR: {}".format(temp_project_irr))
			temp_net_investor_irr = self.selenium_session.get_single_xpath_text("//*[@id='investment-project']//td[preceding-sibling::th[text()='IRR']][2]")
			print("Net Investor IRR: {}".format(temp_net_investor_irr))
			temp_irr_spread = self.selenium_session.get_single_xpath_text("//*[@id='investment-project']//td[preceding-sibling::th[text()='IRR']][3]")
			print("IRR Spread: {}".format(temp_irr_spread))
			# Equity Multiples
			temp_project_equity_multiple = self.selenium_session.get_single_xpath_text("//*[@id='investment-project']//td[preceding-sibling::th[text()='Equity Multiple']][1]")
			print("Project Equity Multiple: {}".format(temp_project_equity_multiple))
			temp_net_investor_equity_multiple = self.selenium_session.get_single_xpath_text("//*[@id='investment-project']//td[preceding-sibling::th[text()='Equity Multiple']][2]")
			print("Net Investor Equity Multiple: {}".format(temp_net_investor_equity_multiple))
			temp_equity_multiple_spread = self.selenium_session.get_single_xpath_text("//*[@id='investment-project']//td[preceding-sibling::th[text()='Equity Multiple']][3]")
			print("Equity Multiple Spread: {}".format(temp_equity_multiple_spread))
			# CAC
			temp_project_COC = self.selenium_session.get_single_xpath_text("//*[@id='investment-project']//td[preceding-sibling::th[text()='Cash on Cash']][1]")
			print("Project Cash on Cash: {}".format(temp_project_COC))
			temp_net_investor_COC = self.selenium_session.get_single_xpath_text("//*[@id='investment-project']//td[preceding-sibling::th[text()='Cash on Cash']][2]")
			print("Net Investor Cash on Cash: {}".format(temp_net_investor_COC))
			temp_CAC_spread = self.selenium_session.get_single_xpath_text("//*[@id='investment-project']//td[preceding-sibling::th[text()='Cash on Cash']][3]")
			print("Cash on Cash Spread: {}".format(temp_CAC_spread))
		except:
			print('Unable to get Project vs Investor Returns')



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
			# Summary
			temp_waterfall_distribution=temp_waterfall_str,
			# Sponsor Fees
			raw_sponsor_fees=temp_raw_sponsor_fees
		)

		return deal_obj

