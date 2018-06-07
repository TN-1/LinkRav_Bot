#!/usr/bin/python
# yarn object
# fill() and to_string()

from constants import *
from settings import *

import logging
logger = logging.getLogger('linkrav_bot')

class Yarn:

	def __init__(self, data):
		self.data = data
		self.name = ""
		self.permalink = ""
		self.yarn_company = ""
		self.yarn_company_permalink = ""
		self. yarn_weight = ""
		self.grams = 0
		self.yarn_fibers = []
		self.yardage = 0
		self.machine_washable = False
		self.rating = 0
		self.photos = []

	# populates fields
	# return true if successful, false if unsuccessful
	def fill(self):
		if self.data is None:
			return False

		try:
			yarn = self.data.get('yarn',default_string)
			if yarn is None or yarn == default_string:
				return False
			
			#name and permalink
			self.name = yarn.get('name',default_string)
			permalink = yarn.get('permalink',default_string)
			self.permalink = RAV_PERM + YARN_MATCH + permalink
			
			# yarn_company and yarn_company_permalink
			yarn_company = yarn.get('yarn_company', default_string)
			yarn_company_id = yarn_company.get('id', default_string)
			if yarn_company_id is not None and yarn_company_id != default_string:
				self.yarn_company = yarn_company.get('name', default_string)
				yarn_company_permalink = yarn_company.get('permalink', default_string)
				self.yarn_company_permalink = RAV_PERM + COMPANY_MATCH + yarn_company_permalink

			# details
			yarn_weight = yarn.get('yarn_weight',default_string)
			self.yarn_weight = yarn_weight.get('name', default_string)
			self.grams = yarn.get('grams',default_string)
			self.yardage = yarn.get('yardage',default_string)
			self.rating = yarn.get('rating_average',default_int)
			
			machine_washable = yarn.get('machine_washable',default_string)
			if machine_washable:
				self.machine_washable = "Yes"
			else:
				self.machine_washable = "No"

			# fibers
			yarn_fibers = yarn.get('yarn_fibers',default_string)
			for yarn_fiber in yarn_fibers:
				fiber_type = (yarn_fiber.get('fiber_type',default_string))
				self.yarn_fibers.append(fiber_type.get('name'))

			# photos
			photos = yarn.get('photos', default_string)
			for photo in photos:
				self.photos.append(photo.get('medium_url'))
			
			return True

		except ValueError, e:
			logger.error('ValueError: %s', str(e.args))
			return False

	# format reply string with fields
	# returns reply string
	def to_string(self):

		yarn_fibers_comment = ""
		for yarn_fiber in self.yarn_fibers:
			yarn_fibers_comment += u" {}.".format(yarn_fiber)

		photos_comment = ""
		i = 1
		for photo in self.photos:
			photos_comment += u" [Img {}]({})".format(i, photo)
			i += 1
			if i > 5:
				break

		comment = u"**YARN:** [{}]({}) by [{}]({})\n\n".format(self.name, self.permalink, self.yarn_company, self.yarn_company_permalink)
		comment += u"* Fiber(s):{} | MW: {}\n".format(yarn_fibers_comment, self.machine_washable)
		comment += u"* Photo(s):{}\n".format(photos_comment)
		comment += u"* Weight: {} | Grams: {} | Yardage: {}\n".format(self.yarn_weight, self.grams, self.yardage)
		comment += u"* Rating: {}\n\n".format(self.rating)

		return comment.encode('utf-8')

