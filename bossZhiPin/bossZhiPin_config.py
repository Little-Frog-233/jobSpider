#coding:utf-8
import os
current_path = os.path.realpath(__file__)
father_path = os.path.dirname(os.path.dirname(current_path))


class bossZhiPin_config:
	def __init__(self):
		self.file_path = father_path
		self.data_path = os.path.join(self.file_path, 'data/bossZhiPin')
		self.city_code_path = os.path.join(self.data_path, 'BOSS直聘城市code.txt')

