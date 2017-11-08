import RE_Crowdfunding
import Utilities
import CrowdStreet
import RealtyShares
import browse
import time
import Input_Output
import airtable



if __name__ == "__main__":

	print('================================')
	print('Starting Analayis')
	print('================================')



	# # create object and session in perparation for social media and other uses
	selenium_session = browse.Browse(browse.BROWSERS.CHROME, "")
	selenium_session.load_page("https://www.google.com")  # Idea is to start from a different page."https://www.google.com"

	# Testing
	# airtable_prospective_deals_obj = airtable.Airtable("app8veAxXaYiCGhO3", "Prospective Deals",api_key="keyrVOeTWn2XwESXT")
	# airtable_record = {
	# 	'GP Equity': 1500000.00
	# }
	# airtable_prospective_deals_obj.insert(airtable_record)
	# END TESTING

	# Array to store all different site URLs
	all_site_deal_urls = []

	# RealtyShares
	realtyshares_obj = RealtyShares.RealtyShares(selenium_session)
	realtyshares_obj.login()
	realtyshares_deal_urls = realtyshares_obj.get_current_offering_urls()

	# crowdstreet_obj = CrowdStreet.CrowdStreet(selenium_session)
	# crowdstreet_obj.login()
	# all_site_deal_urls = crowdstreet_obj.get_current_offering_urls()
	# all_site_deal_urls.extend(crowdstreet_obj.get_current_offering_urls())

	# once have additional sites would do something lik


	# Make airtable object to populate data into
	airtable_prospective_deals_obj = airtable.Airtable("app8veAxXaYiCGhO3", "Prospective Deals", api_key="keyrVOeTWn2XwESXT")
	# airtable_sponsors_obj = airtable.Airtable("app8veAxXaYiCGhO3", "Sponsors", api_key="keyrVOeTWn2XwESXT")


	for deal_url in realtyshares_deal_urls:
		deal_detail = realtyshares_obj.get_deal_details(deal_url)
		airtable_record = {
			'Deal Title': deal_detail.title,
			'Deal Summary': deal_detail.summary,
			'Pictures & Attachments': deal_detail.property_images,
			'Deal URL': deal_url,
			'Target Fund Size': deal_detail.fund_size,
			'Target IRR': deal_detail.target_irr,
			'Target Equity Multiple': deal_detail.target_equity_multiple,
			'Target Investment Period (yrs)': deal_detail.target_investment_period,
			'Investment Profile': deal_detail.investment_profile,
			'Min Investment': deal_detail.min_investment,
			'Target Project Level Returns': deal_detail.target_project_level_returns,
			'Target Avg Cash Yield': deal_detail.target_avg_cash_yield,
			'Offers Due': deal_detail.offers_due,
			'Funds Due': deal_detail.funds_due,
			'Property Type': deal_detail.property_type,
			'Distribution Period': deal_detail.distribution_period,
			'Distribution Commencement': deal_detail.distribution_commencement,
			'Property closing date': deal_detail.property_closing_date,
			'Purchase Price': deal_detail.purchase_price,
			'Percent Funded': deal_detail.percent_funded,
			'Sponsor Co-Investment': deal_detail.sponsor_coinvestment,
			'Platform': 'www.realtyshares.com'			# TODO: Fix this.
			# 'Sponsor Experience': deal_detail.sponsor_experience
		}

		# See if the record is already in the DB
		record = airtable_prospective_deals_obj.match('Deal URL', deal_url)
		if len(record) > 0:
			# If record is there, then just modify
			airtable_prospective_deals_obj.replace(record['id'], airtable_record)
		else:
			# If not add to the DB
			airtable_prospective_deals_obj.insert(airtable_record)

		# IO_obj.append_output_file(deal_detail)
		# temp_deal_details.append(deal_detail)
		time.sleep(Utilities.rand_int_with_occassional_big_int(5,30,115))



