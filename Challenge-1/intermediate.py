
from datetime import datetime, timedelta

from random import randint
from pymongo import MongoClient
from intermediate_dbengine import *
from tabulate import tabulate




def build_json(dict):
	return json.dumps(dict)

def read_json(json):
	return json.load(json)

def validate_json(json, mapping):
	test_dict = {}
	if isinstance(mapping, list):
		for key in mapping:
			try:
				test_dict[key] = json.pop(key)
			except:
				raise ValueError(f"required key: {key} not found in JSON object")

	return True if len(json) < 1 else ask_for_verification(f"The passed JSON object had {len(json)} more keys than required", "validate_json")
	
def ask_for_verification(string_, func_name):
	verify = input(f"{func_name} produced the following error: \n"
				   f"{string_}\n"
				   f"Do you wish to continue anyway? (y/n): ")
	return True if verify == True else False



class Event:

	required_fields = ['name', 'day', 'hour', 'ampm', 'length']
	formatting_req_fields = {'name': 'text', 'day': 'mm/dd/yy',
							 'hour': 'hh:mm', 'ampm': 'AM or PM',
							 'length': 'minutes'}

	def __init__(self, name=None, day=None, hour=None,
				 ampm=None, length=None, id=None, db=None):
		self.name = name
		self.datetime = datetime.strptime(f"{day} {hour} {ampm.upper()}", '%m/%d/%y %I:%M %p')
		self.length = length
		self.td_length = timedelta(minutes=int(length))
		self.id = db.first_empty_id() if db else None
		self.data = {'id': self.id, 'name': self.name, 'datetime': self.datetime, 'length': self.length}
		
		
		
	@classmethod
	def handle_user_input(cls, value, db=None):

		accepted_values = ['1', '2', '3', '4', '5']
		if value not in accepted_values:
			raise ValueError(f"Value {value} is not supported at this time")
		
		if value == '1':
			Event.add_event()
		elif value == '2':
			self.delete_event()
		elif value == '3':
			cls.list_events(db, sort_by={'date_created': -1})
		elif value == '4':
			cls.list_events(db, sort_by={'datetime': -1})
		elif value == '5':
			Event.add_event(test=True, db=db)

	@classmethod
	def generate_inst_from_json(cls, json, store=False, db=None):
		stored_json = json.copy()
		validated = validate_json(json, Event.required_fields)
		if validated:
			print(stored_json)
			if store == True:
				stored_json['db'] = db
				new_event = cls(**stored_json)
				new_event.add_to_db(db)
			return new_event or cls(**stored_json)
		else:
			raise ValueError(f"JSON object was of unsupported type")

	@classmethod
	def add_event(cls, json={}, return_json=False, test=False, db=None):
		if test == True:
			json = {'name': "Doctor's Office", 'day': '01/21',
					'hour': '01:30', 'ampm': 'PM', 'length': '60'}
			return Event.generate_inst_from_json(json, store=True, db=db)
		else:
			for item in Event.required_fields:
				json[item] = input(f"{item.capitalize()} of Event ({Event.formatting_req_fields[item]}): ")
			return json if return_json else Event.generate_inst_from_json(json)

	@classmethod
	def list_events(cls, db, *user_params, sort_by=None):
		user_params = dict(*user_params)
		if sort_by:
			items = db.sort_by(sort_by)
		else:
			#TODO
			pass

	def add_to_db(self, db, date_created=True):
		if date_created == True:
			self.data['date_created'] = datetime.now()
		db.add_to_db(self.data)

	def delete_from_db(self, db):
		db.remove_all(self.data)

	def __str__(self):
		return f"EVENT: {self.name}\n" \
				f"WHEN: {self.datetime.strftime('%b %-d at %I:%M %p')}\n" \
				f"LENGTH: {self.length}\n"
				
if __name__ == "__main__":

	db = MongoEngine.establish_connection(host='mongodb://127.0.0.1:27017')

	while True:
		print("1: Add Event")
		print("2: Delete Event")
		print("3: List Events")
		print("4: List Events Sorted By Date")
		print("5: Test add event")
		user_input = input("Enter the number you wish to choose: ")
		Event.handle_user_input(user_input, db=db)
		
		