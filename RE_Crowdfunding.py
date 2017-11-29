# class RECrowdfundPlatform:
# 	def __init__(self, name, url, deals_url, login_id, password):
# 		self.name = name
# 		self.url = url
# 		self.deals_url = deals_url
# 		self.login_id = login_id
# 		self.password = password
class RECrowdfundingSite:
	def __init__(self, new_deal_urls, existing_deal_urls, obj):
		self.new_deal_urls = new_deal_urls

		# Convert the list of just URLs to a dict so can track if still live or not
		self.existing_deal_urls = []
		for url in existing_deal_urls:
			self.existing_deal_urls.append(dict(
				url=url,
				live=False
			))

		self.obj = obj

class Sponsor:
	def __init__(self, name, url, experience):
		self.name = name
		self.url = url
		self.experience = experience


# this class will hold decision maker info
class DecisionMaker:
	def __init__(self, first_name, last_name, title='', email=''):
		self.first_name = first_name
		self.last_name = last_name
		self.title = title
		self.email = email

	# Overriden "toString" function
	def __str__(self):
		# print("FirstName: " + self.first_name)
		# print("LastName: " + self.last_name)
		# print("Title: " + self.title)
		# print("Email: " + self.email)
		return (self.first_name + " " + self.last_name + "\n" +
				self.title + "\n" +
				str(self.email))



class Deal:
	def __init__(self, title='', summary='', location='', deal_url='', platform_url='',investment_type='', sponsor='', point_of_contact='',
				 fund_size='', target_irr='', upside_irr='', target_equity_multiple='', target_investment_period='',
				 target_project_level_returns='', target_avg_cash_yield='', investment_profile='',
				 min_investment=0.0, offers_due='', funds_due='', property_type='', distribution_period='',
				 distribution_commencement='', property_closing_date='', purchase_price='', price_per_sqft='',
				 sponsor_coinvestment='', sponsor_experience='', debt_service_coverage_ratio='', loan_to_total_cost='',
				 loan_interest_rate='', loan_amortization='', loan_term='', gp_equity='', lp_equity='', senior_debt='',
				 property_images=[], percent_funded=0.0):
		# OVERVIEW INFO
		self.title = title
		self.summary = summary
		self.location = location
		self.deal_url = deal_url
		self.platform_url = platform_url
		self.investment_type = investment_type  # This means Direct investment or SPV
		self.sponsor = sponsor  # This will be a Sponsor type
		self.point_of_contact = point_of_contact  # this will be a DecisionMaker type
		self.property_images = property_images

		# SUMMARY INFO
		self.fund_size = fund_size

		# DEAL NUMBERS
		# Return Projections
		self.target_irr = target_irr
		self.upside_irr = upside_irr
		self.target_equity_multiple = target_equity_multiple
		self.target_investment_period = target_investment_period
		self.target_project_level_returns = target_project_level_returns  # how is this different than IRR?
		self.target_avg_cash_yield = target_avg_cash_yield

		self.investment_profile = investment_profile
		self.min_investment = min_investment
		self.offers_due = offers_due
		self.funds_due = funds_due
		self.property_type = property_type
		self.distribution_period = distribution_period
		self.distribution_commencement = distribution_commencement
		self.property_closing_date = property_closing_date
		# Property Details
		self.purchase_price = purchase_price
		self.percent_funded = percent_funded
		self.price_per_sqft = price_per_sqft
		self.sponsor_coinvestment = sponsor_coinvestment
		self.sponsor_experience = sponsor_experience

		# DEBT DETAILS
		self.debt_service_coverage_ratio = debt_service_coverage_ratio
		self.loan_to_total_cost = loan_to_total_cost
		self.loan_interest_rate = loan_interest_rate
		self.loan_amortization = loan_amortization
		self.loan_term = loan_term

		# CAPITAL STACK
		self.gp_equity = gp_equity
		self.lp_equity = lp_equity
		self.senior_debt = senior_debt
		# self.total_capital_stack = gp_equity + lp_equity + senior_debt
		# if self.total_capital_stack > 0:
		#     self.gp_equity_pct = gp_equity / self.total_capital_stack
		#     self.lp_equity_pct = lp_equity / self.total_capital_stack
		#     self.senior_debt_pct = senior_debt / self.total_capital_stack
