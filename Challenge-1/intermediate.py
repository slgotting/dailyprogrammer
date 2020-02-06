
from datetime import datetime, timedelta

from random import randint
import pymongo
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

def validate(input_, field):
		if field == 'name':
			return input_
		elif field == 'day':
			try:
				datetime.strptime(input_, '%m/%d/%y')
				return input_
			except:
				validate(input("Invalid date format, try again (mm/dd/yy): "), field)
		elif field == 'hour':
			try:
				datetime.strptime(input_, '%I:%M')
				return input_
			except:
				validate(input('Please provide a valid 12 hour format (hh:mm): '), field)
		elif field == 'ampm':
			return input_ if input_ == 'AM' or input == 'PM' else validate(input('Input AM or PM: '), field)
		elif field == 'length':
			try:
				return int(input_)
			except:
				validate(input('Please enter a valid integer (minutes): '), field)
			
		['name', 'day', 'hour', 'ampm', 'length']
	
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
		
		accepted_values = ['1', '2', '3', '4', '5', '6']
		if value not in accepted_values:
			raise ValueError(f"Value {value} is not supported at this time")
		
		if value == '1':
			cls.add_event(db=db)
		elif value == '2':
			cls.delete_event(db=db)
		elif value == '3':
			cls.list_events(db)
		elif value == '4':
			cls.list_events(db, sort_by=[('datetime', pymongo.DESCENDING)])
		elif value == '5':
			cls.list_events(db, sort_by=[('date_created', -1)])
		elif value == '6':
			Event.add_event(test=True, db=db)

	@classmethod
	def create_event(cls, json, store=False, db=None):
		stored_json = json.copy()
		validated = validate_json(json, Event.required_fields)
		if validated:
			print(stored_json)
			if store == True:
				stored_json['db'] = db
				cls(**stored_json).add_to_db(db) #instantiates class and adds it to the database
			else:
				return cls(**stored_json)
		else:
			raise ValueError(f"JSON object was of unsupported type")

	@classmethod
	def add_event(cls, json={}, return_json=False, test=False, db=None):
		if test == True:
			json = {'name': "Doctor's Office", 'day': '01/21/20',
					'hour': '01:30', 'ampm': 'PM', 'length': '60'}
			return Event.create_event(json, store=True, db=db)
		else:
			for item in Event.required_fields:
				item_to_add = validate(input(f"{item.capitalize()} of Event ({Event.formatting_req_fields[item]}): "), item)
				json[item] = item_to_add
			return json if return_json else Event.create_event(json, store=True, db=db)

	@classmethod
	def list_events(cls, db, *user_params, sort_by=None):
		user_params = dict(*user_params)
		cols = db.get_every_key_in_collection()
		if sort_by:
			items = db.sort_by(sort_by)
		else:
			items = db.retrieve_all_from_coll()
	
		item_list = []
		for item in items:
			instance_items = []
			for col in cols:
				try:
					instance_items.append(item[col])
				except:
					instance_items.append('')
			item_list.append(instance_items)
		
		print(tabulate(item_list, headers=cols, tablefmt='grid'))

	def add_to_db(self, db, date_created=True):
		if date_created == True:
			self.data['date_created'] = datetime.now()
		db.add_to_db(self.data)

	@classmethod
	def delete_event(cls, db=None):
		event_id = input('Please enter the id of the event you wish to delete: ')
		db.delete_one({'id': int(event_id)})
		

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
		print("5: List events sorted by date created")
		print("6: Test add event")
		user_input = input("Enter the number you wish to choose: ")
		Event.handle_user_input(user_input, db=db)
		
		