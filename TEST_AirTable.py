import RE_Crowdfunding
import Utilities
import browse
import time
import airtable
import pprint



if __name__ == "__main__":

	print('================================')
	print('Starting AirTable Test')
	print('================================')



	# Make airtable object to populate data into
	airtable_prospective_deals_obj = airtable.Airtable("app8veAxXaYiCGhO3", "Prospective Deals",api_key="keyrVOeTWn2XwESXT")
	airtable_closed_deals_obj = airtable.Airtable("app8veAxXaYiCGhO3", "Closed Deals",api_key="keyrVOeTWn2XwESXT")
	# airtable_sponsors_obj = airtable.Airtable("app8veAxXaYiCGhO3", "Sponsors", api_key="keyrVOeTWn2XwESXT")

	# START TESTING
	airtable_record = {'Deal Summary': None,
 'Deal Title': 'Hunt Club Apartments',
 'Deal URL': 'https://www.realtyshares.com/investments/hunt-club-apartments',
 'Distribution Commencement': '',
 'Distribution Period': '',
 'Funds Due': None,
 'Investment Profile': '',
 'Min Investment': '10000.0',
 'Offers Due': None,
 'Percent Funded': None,
 'Pictures & Attachments': [{'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/A2EA922757A3D13D07871B169853260A0B14F51C5C02CD96C4397320F8B0C331'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/EEECE80784F9D622758F07F8BE302BF64C51889D6FE0677DCC9A53D14549409A'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/228946658D63C439B889EA660F8976D14B6B82027409D5821F921D6660DDF3DD'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/CB55750928CC0B8DCAA9DDDD89E7832D63B5551BAFA1F065E9E60E4C0063B72F'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/A1ADBAD9885FEF1FFDC7FF8DAE1B621CF373EE3913420C2BA6E245E71C1468DD'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/185288FEB2F1F818D8BE5ADA83BE111AD9B110EBFE33B9C5196EDC10132F3CEA'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/A9FB2C41E936B17D6C9642CCAEF828F21DC926F7770711DD3C16DF2A322CCBA9'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/869F1DFCE37950E5C885F7DED6D8BEDE188C5124D54B7C7DC5CA0EAB387E3318'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/A195507C98EDDD2AD582E198AF5898E899E8A5010438EFD2A4FA04A639D443EB'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/B9D9C327D577A3ABD070406C679357D86FFFCF53F273CDC78482363AC140944C'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/2E82632DA7D6673D8B591855D123837AE6B55B36E87531EF1C0E517F2F1DFD0D'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/AD4BA7BC3E61A1E2F9C2E813F5B247D5A803543EFE0636ABAB22A58D003B0B30'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/66E13CDE741C257B748BE76BC9CA64AF55B2DF327FD240F4AD648376DF8B1CA6'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/2274333384FB163CEE70AD0E19D8672D8D15A89BDF6253D96386530E6599CAB3'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/C414FD7C63006BF2E10F1D8E378147CB99453DE1365F033C07B436179383D86D'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/4B81189F0D07E3346343DF54751768F0E25875C52F65CC110BA8BA8FE7CEC836'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/FCC4AE0B5756FEF024175C47896551EC7709373067B9CBF842F2F122F51C7560'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/2E62ED580CB6D8EFD121B131EFA8CF4EB06D4CF54F639B14C5536F2D96259776'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/F234F24015BC585A9DC4D6CEA94EA16F76523E1B478B1FB91C4A63E516026BF3'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/0D1FA0DFD2BCB1605A2ECC116A5BA4E2B44B214770AFCE9CC865F3CE130B78E0'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/B96A197CDD7D7504D66A01CBC4AEB35795D3A86A28CC4357F493D51B6533FB82'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/A888BBB96EFFB5B0376A7A132C3A175C7D1BD43B515E2F878D5D7903C6DA5986'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/CAF6B13EA3AD3EADB29A7A1674B4E3021A397BD0D68D49654A72B801E06BA18A'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/A9D6F9076BE0017279CE3D1E0AEA8F120BE272A3BDAFEB7D2C3CE2AF5D447E3C'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/6F0093DD8B366D7B8F0F450FAB56545F5D7DC4C6BE11629B61E6CACFB4CA28AC'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/2FEB883630600F2253C81AB9A511DF1AAEF9724E3B4A77B77990EE144070B1BA'},
                            {'url': 'https://s3-us-west-2.amazonaws.com/realtyshares-web-media-production/images/4203364822206551/D0A3953CC3F6AD899AF269A42F7A93A4A7B5C211F375C293E5B7BBBF2DFEEFE3'}],
 'Platform': 'https://www.realtyshares.com',
 'Property Type': 'Multifamily',
 'Property closing date': None,
 'Purchase Price': '$1,515,000',
 'Sponsor Co-Investment': '',
 'Sponsor Fees': '',
 'Target Avg Cash Yield': None,
 'Target Equity Multiple': None,
 'Target Fund Size': '',
 'Target IRR': '',
 'Target Investment Period (yrs)': None,
 'Target Project Level Returns': None,
 'Waterfall Distribution': 'Distribution Structure\n'
                           '\n'
                           'Distributable proceeds from operating cash flow '
                           'and capital events are to be distributed in order '
                           'as follows:\n'
                           '\n'
                           'Senior debt service payments;\n'
                           'Then, to all deal-level investors pro-rata and '
                           'pari-passu until such investors have earned an '
                           '9.0% annual IRR (compounded annually);\n'
                           'Thereafter, 25.0% to Sponsor and 75.0% to '
                           'deal-level investors pro-rata and pari-passu until '
                           'such investors have earned an 17.0% annual IRR '
                           '(compounded annually);\n'
                           'Then 30.0% to Sponsor and and 70.0% to deal-level '
                           'investors.  \n'
                           '\n'
                           'Please refer to the Documents section for more '
                           'financial information.\n'
                           '\n'
                           'Note: Equity distributions are determined on a '
                           'quarterly basis. It is at the discretion of the '
                           'Sponsor to pay out distributions as there is no '
                           'set distribution schedule. It may take several '
                           'quarters for distributions to begin, depending on '
                           'the sponsor’s business plan and performance of the '
                           'property.\n'
                           '\n'}

	# See if the record is already in the DB
	record = airtable_prospective_deals_obj.match('Deal URL', airtable_record['Deal URL'])
	if len(record) > 0:
		# If record is there, then just modify
		airtable_prospective_deals_obj.replace(record['id'], airtable_record)

	else:
		# If not add to the DB
		airtable_prospective_deals_obj.insert(airtable_record)
		# Check to see if the record is mistakenly in the Closed Deals table and delete if so
		closed_record = airtable_closed_deals_obj.match('Deal URL', airtable_record['Deal URL'])
		if len(closed_record) > 0:
			# Delete the record from the Closed Deals Table.
			airtable_closed_deals_obj.delete(closed_record['id'])

	# END TESTING
