#
# weibo_profile.py
#
# doufunao 2013-08-02
#

import re

class profile:
	"""
	Get the weibo user profile from the web page

	example:

		Instantiate class profile, text is the input strings
		p = profile(text)

		get the profile:
		profilelist = p.getprofile()

		get the follow list:
		followlist = p.getlist()
	"""
	listall = []

	text = ''

	userid = 'error'
	nickname = 'error'
	followernum = 'error'
	followingnum = 'error'
	weibonum = 'error'
	membertype = 'error'
	memberlevel = 'error'

	homerelist = {'uid': r'\[\'oid\'\]=\'(\d+)\'',
				'nickname': r'\[\'onick\'\]=\'(.+)\'',
				'followingnum': r'node-type=\\\"follow\\\">(\d+)<\\/strong>',
				'followernum': r'node-type=\\\"fans\\\">(\d+)<\\/strong>',
				'weibonum': r'node-type=\\\"weibo\\\">(\d+)<\\/strong>',
				'membertype': r'class=\\\"W_ico16 (\w+)\\\"',
				'memberlevel': r'class=\\\"W_level_num l(\d+)\\\"'}

	followrelist = {'uid_nickname_sex': r'action-type=\\\"itemClick\\\" action-data=\\\"uid=(\d+)&fnick=([^&]+)&sex=([fm])\\\"',
				'followurl_path': r'通过<a href=\\\"(http:\\\/\\\/[^"]+)\\\" class=\\\"S_link2\\\" >([^<]+)<\\\/a>关注'
				}

	def __init__(self,text):
		self.text = text
		#print(userid)

	def refunc(self,restr):
		text = self.text
		match = re.search(restr,text)
		if match == None:
			#print('refunc: pattern doesnt exist')
			return None
		else:
			#print('refunc:',match.group(1))	
			return match.group(1)

	def findallfunc(self,restr):
		text = self.text
		match = re.findall(restr,text)
		if match == None:
			#print('None is matched.')
			return None
		else:
			#print(match)
			return match			

	def printprofile(self):
		'''
		This function can print the profile of the current user

			return
		'''

		self.setprofile()
		print(self.userid,
			self.nickname,
			self.followernum,
			self.followingnum,
			self.weibonum,
			self.membertype,
			self.memberlevel)

	def getprofile(self):
		self.setprofile()
		profilelist = []
		profilelist.append({'uid':self.userid})
		profilelist.append({'nickname':self.nickname})
		profilelist.append({'followernum':self.followernum})
		profilelist.append({'followingnum':self.followingnum})
		profilelist.append({'weibonum':self.weibonum})
		profilelist.append({'membertype':self.membertype})
		profilelist.append({'memberlevel':self.memberlevel})
		return profilelist

	def setprofile(self):
		'''
		This function is used in http://weibo.com/p/pageid
		or http://weibo.com/nickname
		or http://weibo.com/u/uid
		'''
		restrlist = self.homerelist
		refunc = self.refunc
		text = self.text
		self.userid = refunc(restrlist['uid'])
		self.nickname = refunc(restrlist['nickname'])
		self.followernum = refunc(restrlist['followernum'])
		self.followingnum = refunc(restrlist['followingnum'])
		self.weibonum = refunc(restrlist['weibonum'])
		self.membertype = refunc(restrlist['membertype'])
		self.memberlevel = refunc(restrlist['memberlevel'])

	def getlist(self):
		'''
		This function can get :	 
			The list of users whom current user is following.
		or	The list of users who is following the current user.
		is decided by the text.	
		'''

		findallfunc = self.findallfunc
		followrelist = self.followrelist
		text = self.text

		list1 = findallfunc(followrelist['uid_nickname_sex'])
		list2 = findallfunc(followrelist['followurl_path'])
		#print(list2)

		'''
		tuples to list
		'''

		listall = []
		for x1, x2 in zip(list1, list2):
			listall.append(x1 + x2)
		listall2 = []
		for x in listall:
			'''
			data example:
				x[0]=2163484125
				x[1]=完全披露
				x[2]=m
				x[3]=http://app.weibo.com/t/feed/c66T5g
				x[4]=Android客户端
			'''
			dict_temp = {}
			dict_temp['uid'] = x[0]
			dict_temp['nickname'] = x[1]
			dict_temp['sex'] = x[2]
			dict_temp['followpathurl'] = x[3].replace('\\','')
			dict_temp['followpath'] = x[4]
			listall2.append(dict_temp)
			#print(dict_temp)
		return listall2
