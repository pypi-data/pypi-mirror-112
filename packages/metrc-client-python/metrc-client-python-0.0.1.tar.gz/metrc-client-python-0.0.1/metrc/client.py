import requests

class Client(object):

	def __init__(self, vendor_keys,environment):
		self.vendor_keys = vendor_keys
		self.environment = environment

	states ={
		'sandbox_states':{
			'MD': 'https://sandbox-api-md.metrc.com',
			'OR': 'https://sandbox-api-or.metrc.com',
			'CO': 'https://sandbox-api-co.metrc.com',
			'LA': 'https://sandbox-api-or.metrc.com',
			'ME': 'https://sandbox-api-md.metrc.com',
			'AK': 'https://sandbox-api-or.metrc.com'
		},
		'production_states':{
			'MD': 'https://api-md.metrc.com',
			'OR': 'https://api-or.metrc.com',
			'CO': 'https://api-co.metrc.com',
			'LA': 'https://api-or.metrc.com',
			'ME': 'https://api-md.metrc.com',
			'AK': 'https://api-or.metrc.com'
		}
	}

	def validate(self, state, user_key):

		environment = self.environment
		if(environment =='sandbox'):
			base_url = Client.states['sandbox_states'][state]
		elif(environment=='production'):
			base_url = Client.states['production_states'][state]

		vendor_key = self.vendor_keys[state]

		validate_url = base_url + "/facilities/v1/"
		print(validate_url)

		r = requests.get(validate_url, auth=(vendor_key, user_key))

		return r.status_code == 200