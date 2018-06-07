#!/usr/bin/python
# project object
# fill() and to_string()

from constants import *
from settings import *

import logging
logger = logging.getLogger('linkrav_bot')

class Project:

	def __init__(self, data):
		self.data = data
		self.name = ""
		self.permalink = ""
		self.username = ""
		self.user_permalink = ""
		self.pattern = ""
		self.yarns = []
		self.progress = 0
		self.status = ""
		self.started = None
		self.completed = None
		self.photos = []

	# populates fields
	# return true if successful, false if unsuccessful
	def fill(self, ravelry):
		if self.data is None:
			return False
		
		try:
			project = self.data.get('project',default_string)
			if project is None or project == default_string:
				return False

			# name, permalink, user, user permalink
			self.name = project.get('name',default_string)
			id = project.get('id',default_string)
			permalink = project.get('permalink',default_string)
			user = project.get('user',default_string)
			self.username = user.get('username', default_string)
			self.permalink = RAV_PERM + PROJ_MATCH + "{}/{}".format(self.username,id)
			self.user_permalink = RAV_PERM + PEOPLE_MATCH + str(self.username)

			# pattern
			pattern_name = project.get('pattern_name', default_string)
			if pattern_name is not None and pattern_name != default_string:
				pattern_id = project.get('pattern_id', default_string)
				if pattern_id is not None and pattern_id != default_string:
						pattern_request = ravelry.get_json(PAT_API.format(pattern_id))
						pattern = pattern_request.get('pattern',default_string)
						pattern_permalink = pattern.get('permalink',default_string)
						pattern_permalink = RAV_PERM + PAT_MATCH + pattern_permalink
						self.pattern = u" [{}]({})".format(pattern_name, pattern_permalink)
				else:
					self.pattern = pattern_name
			else:
				self.pattern = pattern_name

			# yarns
			packs = project.get('packs', default_string)
			if packs is not None and packs != default_string:
				yarn_names = []
				yarn_colors = []

				for pack in packs:

					# yarn name and permalink
					yarn_comment = ""
					yarn_name = pack.get('yarn_name', default_string)
					yarn_id = pack.get('yarn_id', default_string)
					
					temp_list = [i[0] for i in yarn_names]
					if yarn_id in temp_list and yarn_id is not None:
						yarn_index = temp_list.index(yarn_id)
					else:
						if yarn_id is not None and yarn_id != default_string:
							yarn_json = YARN_API.format(yarn_id)
							yarn_request = ravelry.get_json(YARN_API.format(yarn_id))
							yarn = yarn_request.get('yarn',default_string)
							yarn_permalink = yarn.get('permalink',default_string)
							yarn_permalink = RAV_PERM + YARN_MATCH + yarn_permalink
							yarn_comment = u"[{}]({})".format(yarn_name, yarn_permalink)
						elif yarn_name is not None and yarn_name != default_string:
							yarn_comment = u"{}".format(yarn_name)
						else:
							continue
						yarn_names.append((yarn_id, yarn_comment))
						yarn_index = len(yarn_names)-1
						yarn_colors.append([])
					
					# colorway or color family
					color_comment = pack.get('colorway', "")
					if color_comment is None or color_comment == default_string or color_comment == "":
						color_families_id = pack.get('color_family_id', default_string)
						if color_families_id is not None and color_families_id != default_string:
							color_families = ravelry.get_json("https://api.ravelry.com/color_families.json").get('color_families')
							color_comment = color_families[color_families_id - 1].get('name', "")
					if color_comment != "":
						yarn_colors[yarn_index].append(color_comment)
					
				# format yarn, with color if it exists
				for id, name in yarn_names:
					colors = ""
					yarn_index = [i[0] for i in yarn_names].index(id)
					for color in yarn_colors[yarn_index]:
						colors+=(u"{}, ".format(color))

					if colors != "":
						self.yarns.append(u"{} in {}".format(name, colors))
					else:
						self.yarns.append(u"{}".format(name))

			# details
			self.status = project.get('status_name', default_string)
			self.started = project.get('started', default_string)
			self.completed = project.get('completed', default_string)

			# photos
			photos = project.get('photos', default_string)
			for photo in photos:
				self.photos.append(photo.get('medium_url'))
			
			return True

		except ValueError, e:
			logger.error('ValueError: %s', str(e.args))
			return False

	# format reply string with fields
	# returns reply string
	def to_string(self):

		yarns_comment = ""
		for yarn in self.yarns:
			if yarn[-2:] == ", ":
				yarn = yarn[:-2]
			yarns_comment += u" {}.".format(yarn)

		photos_comment = ""
		i = 1
		for photo in self.photos:
			photos_comment += u" [Img {}]({})".format(i, photo)
			i += 1
			if i > max_photos:
				break

		comment = u"**PROJECT:** [{}]({}) by [{}]({})\n\n".format(self.name, self.permalink, self.username, self.user_permalink)
		comment += u"* Pattern: {}\n".format(self.pattern)
		comment += u"* Yarn(s):{}\n".format(yarns_comment)
		comment += u"* Photo(s):{}\n".format(photos_comment)
		comment += u"* Started: {} | Status: {} | Completed: {}\n\n".format(self.started, self.status, self.completed)
  
		return comment.encode('utf-8')

