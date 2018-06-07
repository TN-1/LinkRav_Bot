#!/usr/bin/python
# pattern object
# fill() and to_string()

from constants import *
from settings import *

import logging
logger = logging.getLogger('linkrav_bot')

class Pattern:

	def __init__(self, data):
		self.data = data
		self.name = ""
		self.permalink = ""
		self.author = ""
		self.author_permalink = ""
		self.categories = []
		self.needles = []
		self.yarn_weight = ""
		self.gauge = 0
		self.yardage = 0
		self.price = ""
		self.difficulty = 0
		self.projects = 0
		self.rating = 0
		self.photos = []

	# populates fields
	# returns true if successful, false if unsuccessful
	def fill(self):
		if self.data is None:
			return False
		
		try:
			pattern = self.data.get('pattern', default_string)
			if pattern is None or pattern == default_string:
				return False
			
			# name and permalink
			self.name = pattern.get('name', default_string)
			self.permalink = pattern.get('permalink', default_string)
			self.permalink = RAV_PERM + PAT_MATCH + self.permalink

			# author and author_permalink
			pattern_author = pattern.get('pattern_author', default_string)
			self.author = pattern_author.get('name', default_string)
			pattern_author_permalink = pattern_author.get('permalink', default_string)
			self.author_permalink = RAV_PERM + DESIGNER_MATCH + pattern_author_permalink

			# categories
			pattern_categories = pattern.get('pattern_categories', default_string)
			if pattern_categories is not None and pattern_categories != default_string:
				pattern_category = pattern_categories[0]
				while pattern_category is not None:
					category_name = pattern_category.get('name')
					if category_name != "Categories":
						self.categories.insert (0, category_name)
					pattern_category = pattern_category.get('parent')

			# needles
			pattern_needle_sizes = pattern.get('pattern_needle_sizes', default_string)
			if pattern_needle_sizes is not None and pattern_needle_sizes != default_string:
				for pattern_needle_size in pattern_needle_sizes:
					self.needles.append(pattern_needle_size.get('name', default_string))
	
			# yarn_weight
			yarn_weight = pattern.get('yarn_weight', default_string)
			if yarn_weight is not None and yarn_weight != default_string:
				self.yarn_weight = yarn_weight.get('name', default_string)
			
			# gauge and yardage
			self.gauge = pattern.get('gauge', default_string)
			self.yardage = pattern.get('yardage', default_string)

			# price
			self.free = pattern.get('free',default_string)
			if self.free == True:
				self.price = "Free"
			elif self.free == False:
				self.price = pattern.get('price',default_string)
				currency = pattern.get('currency',"")
				self.price = u"{} {}".format(self.price, currency)
    
			# details
			self.difficulty = pattern.get('difficulty_average',default_int)
			self.projects = pattern.get('projects_count',default_string)
			self.rating = pattern.get('rating_average',default_int)

			# photos
			photos = pattern.get('photos', default_string)
			for photo in photos:
				self.photos.append(photo.get('medium_url'))

			return True

		except ValueError, e:
			logger.error('ValueError: %s', str(e.args))
			return False

	# format reply string with fields
	# returns reply string
	def to_string(self):

		categories_comment = ""
		for category in self.categories:
			categories_comment += u" {} > ".format(category)
		categories_comment = categories_comment[:-3]

		needles_comment = ""
		for needle in self.needles:
			needles_comment += u"{}, ".format(needle)
		if needles_comment == "":
			needles_comment = " None"
		else:
			needles_comment = needles_comment[:-2]

		photos_comment = ""
		i = 1
		for photo in self.photos:
			photos_comment += u" [Img {}]({})".format(i, photo)
			i += 1
			if i > max_photos:
				break

		comment = u"**PATTERN:** [{}]({}) by [{}]({})\n\n".format(self.name, self.permalink, self.author, self.author_permalink)
		comment += u"* Category:{}\n".format(categories_comment)
		comment += u"* Photo(s):{}\n".format(photos_comment)
		comment += u"* Price: {}\n".format(self.price)
		comment += u"* Needle/Hook(s):{}\n".format(needles_comment)
		comment += u"* Weight: {} | Gauge: {} | Yardage: {}\n".format(self.yarn_weight, self.gauge, self.yardage)
		comment += u"* Difficulty: {:.2f} | Projects: {} | Rating: {:.2f}\n\n".format(self.difficulty, self.projects, self.rating)

		return comment.encode('utf-8')
