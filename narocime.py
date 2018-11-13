import requests
from datetime import datetime
import time
import re
from urllib.parse import unquote

class Client(object):

	def __init__(self):
		self.session = requests.Session()
		self.updateApiSignature()

	def getApiSignature(self):
		url = "https://sportul.naroci.me/narocilo/workout/embedded"
		response = self.session.get(url)
		result = re.search(r"x_api_signature=([\w\-%\/]+)&", response.text)
		if result:
			return unquote(result.group(1))
		return None

	def updateApiSignature(self):
		self.apiSignature = self.getApiSignature()

	def getEvents(self, dateFrom, dateTo):
		url = "https://api.naroci.me/api/v1/workout/appointment/list"
		getParameters = {
			"x_api_signature": self.apiSignature,
			"user_agent": "Naroci.Me-OnlineWidget"
		}
		searchData = {
			"staff": "",
			"workplace": "",
			"workout": "",
			"start": int(time.mktime(dateFrom.timetuple())),
			"end":  int(time.mktime(dateTo.timetuple()))
		}
		response = self.session.post(url, params=getParameters, data=searchData)
		if response.status_code != 200:
			self.updateApiSignature()
			return []
		events = [Event.fromJson(eventData) for eventData in response.json()]
		return events

	def signup(self, user, event):
		url = "https://api.naroci.me/api/v1/workout/signup/ver"
		getParameters = {
			"x_api_signature": self.apiSignature,
			"user_agent": "Naroci.Me-OnlineWidget"
		}
		signupData = {
			"event_id": event.id,
			"gdpr": True,
			"get_email_notifications": False,
			"get_txt_notifications": False,
			"verify_number": "",
			"step": 1
		}
		allSignupData = {**signupData, **user.getData()}
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
		}
		response = self.session.post(url, headers=headers, params=getParameters, data=allSignupData)
		return EventResult.fromJson(response.json())

	def cancel(self, eventResult):
		url = "http://sportul.naroci.me/workout/cancel/{}".format(eventResult.code)
		response = self.session.post(url)

class EventResult(object):

	def __init__(self, jsonData):
		self.jsonData = jsonData

	def fromJson(jsonData):
		return EventResult(jsonData)
		

class User(object):

	def __init__(self, first_name, last_name, email, phone, vpisna_stevilka, fakulteta):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.phone = phone
		self.vpisna_stevilka = vpisna_stevilka
		self.fakulteta = fakulteta

	def getData(self):
		return {
			"first_name": self.first_name,
			"last_name": self.last_name,
			"phone": self.phone,
			"email": self.email,
			"record-clanica": self.fakulteta,
			"record-vpisna_stevilka": self.vpisna_stevilka
		}

class Event(object):

	def __init__(self, id, title, start, end, capacity, count):
		self.id = id
		self.title = title
		self.start = start
		self.end = end
		self.capacity = capacity
		self.count = count

	def fromJson(jsonData):
		startTime = datetime.strptime(jsonData["start"], '%Y-%m-%d %H:%M:%S')
		endTime = datetime.strptime(jsonData["end"], '%Y-%m-%d %H:%M:%S')
		return Event(jsonData["id"], jsonData["title"], startTime, endTime, int(jsonData["event"]["capacity"]), int(jsonData["event"]["count"]))

	def __repr__(self):
		return "Event(id='{}', title='{}', startTime='{}', endTime='{}')".format(self.id, self.title, self.start, self.end)