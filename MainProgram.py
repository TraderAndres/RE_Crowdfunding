import RE_Crowdfunding
import Utilities
import CrowdStreet
import RealtyShares
import browse
import time
import Input_Output
import airtable

# TIME TRACKING
# 11-29-17 Start 10:17
# 11-29-17 End 11:27
# 12-1-17: Start 9:24
# 12-1-17: End 10:15


if __name__ == "__main__":

	print('================================')
	print('Starting Analayis')
	print('================================')



	# # create object and session in perparation for social media and other uses
	selenium_session = browse.Browse(browse.BROWSERS.CHROME, "")
	selenium_session.load_page("https://www.google.com")  # Idea is to start from a different page."https://www.google.com"


	# Make airtable object to populate data into
	airtable_prospective_deals_obj = airtable.Airtable("app8veAxXaYiCGhO3", "Prospective Deals",api_key="keyrVOeTWn2XwESXT")
	airtable_closed_deals_obj = airtable.Airtable("app8veAxXaYiCGhO3", "Closed Deals",api_key="keyrVOeTWn2XwESXT")
	# airtable_sponsors_obj = airtable.Airtable("app8veAxXaYiCGhO3", "Sponsors", api_key="keyrVOeTWn2XwESXT")

	# Testing
	# record = airtable_prospective_deals_obj.match('Deal URL', 'https://www.realtyshares.com/investments/slate-apartments')]
	# airtable_record = record['fields']
	# pics_attaches = airtable_record.pop('Pictures & Attachments', None)
	# clean_pics = []
	# for pic in pics_attaches:
	# 	clean_pics.append({'url': pic.pop('url', None)})
	#
	# airtable_record['Pictures & Attachments'] = clean_pics
	# # Ignore the fields below because formulas already calculated on the sheet.
	# airtable_record.pop('GP Equity %',None)
	# airtable_record.pop('LP Equity %', None)
	# airtable_record.pop('Senior Debt %', None)
	# airtable_closed_deals_obj.insert(airtable_record)
	# END TESTING

	# Array to store all different site URLs and objects
	# all_site_deal_urls = []
	all_site_deals = []

	# RealtyShares
	realtyshares_obj = RealtyShares.RealtyShares(selenium_session)
	realtyshares_obj.login()
	realtyshares_new_deal_urls = realtyshares_obj.get_current_offering_urls()
	realtyshares_records = airtable_prospective_deals_obj.search('Platform', realtyshares_obj.url)
	realtyshares_existing_deal_urls = [ item['fields']['Deal URL'] for item in realtyshares_records ]
	all_site_deals.append(RE_Crowdfunding.RECrowdfundingSite(realtyshares_new_deal_urls, realtyshares_existing_deal_urls, realtyshares_obj))

	# Crowdstreet
	crowdstreet_obj = CrowdStreet.CrowdStreet(selenium_session)
	crowdstreet_obj.login()
	crowdstreet_new_deal_urls = crowdstreet_obj.get_current_offering_urls()
	crowdstreet_records = airtable_prospective_deals_obj.search('Platform', crowdstreet_obj.url)
	crowdstreet_existing_deal_urls = [item['fields']['Deal URL'] for item in realtyshares_records]
	all_site_deals.append(RE_Crowdfunding.RECrowdfundingSite(crowdstreet_new_deal_urls, crowdstreet_existing_deal_urls, crowdstreet_obj))
	# all_site_deal_urls.extend(crowdstreet_obj.get_current_offering_urls())

	# once have additional sites would do something lik




	for site in all_site_deals:
		for deal_url in site.new_deal_urls:
			deal_detail = site.obj.get_deal_details(deal_url)
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
				'Platform': deal_detail.platform_url
				# 'Sponsor Experience': deal_detail.sponsor_experience
			}

			# See if the record is already in the DB
			record = airtable_prospective_deals_obj.match('Deal URL', deal_url)
			if len(record) > 0:
				# If record is there, then just modify
				airtable_prospective_deals_obj.replace(record['id'], airtable_record)
				# Change the existing_deal_urls live value to true
				for item in site.existing_deal_urls:
					if item['url'] == deal_url:
						item['live'] = True
						break
			else:
				# If not add to the DB
				airtable_prospective_deals_obj.insert(airtable_record)

			# IO_obj.append_output_file(deal_detail)
			# temp_deal_details.append(deal_detail)
			time.sleep(Utilities.rand_int_with_occassional_big_int(5,30,115))


		# Now that found all new deals for THIS SIDE and categorized old deals,
		# go through all existing_deal_urls and move any where live=False
		for item in site.existing_deal_urls:
			# if live = False, then move to "Closed Deals" Table
			if item['live'] == False:
				record = airtable_prospective_deals_obj.match('Deal URL', item['url'])
				airtable_record = record['fields']
				pics_attaches = airtable_record.pop('Pictures & Attachments', None)
				clean_pics = []
				for pic in pics_attaches:
					clean_pics.append({'url': pic.pop('url', None)})

				airtable_record['Pictures & Attachments'] = clean_pics
				# Ignore the fields below because formulas already calculated on the sheet.
				airtable_record.pop('GP Equity %', None)
				airtable_record.pop('LP Equity %', None)
				airtable_record.pop('Senior Debt %', None)
				airtable_closed_deals_obj.insert(airtable_record)
				# Delete the record from the Prospective Deals Table.
				airtable_prospective_deals_obj.delete(record['id'])

