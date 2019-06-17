# coding:utf-8
import os
import requests
import json
import pandas as pd
from pyquery import PyQuery as pq
from bossZhiPin.bossZhiPin_config import bossZhiPin_config


def get_city_code():
	'''

	:return:
	'''
	city_code = {}
	file_path = bossZhiPin_config().city_code_path
	with open(file_path) as file:
		line = file.readline()
		code_dict = json.loads(line)
	city_code_list = code_dict['zpData']['cityList']
	for item in city_code_list:
		code = item['code']
		name = item['name']
		city_code[name] = code
		sub_city_list = item['subLevelModelList']
		for sub_item in sub_city_list:
			code = sub_item['code']
			name = sub_item['name']
			city_code[name] = code
	return city_code


class bossZhiPin_spider:
	def __init__(self, city=None, job=None, max_page=None):
		self.config = bossZhiPin_config()
		self.code_dict = get_city_code()
		self.city = city
		self.city_code = self.code_dict.get(self.city, 100010000)  ###默认为全国代码
		self.job = job
		self.max_page = max_page
		self.base_url = 'https://www.zhipin.com/c%s/?query=%s'%(self.city_code, self.job) + '&page=%s&ka=page-%s'
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

	def get_html(self, url=None):
		'''

		:param url:
		:return:
		'''
		html = requests.get(url, headers=self.headers)
		if html.status_code == 200:
			return html.text
		else:
			print('get url fail')
			return None

	def get_item(self, text=None):
		'''

		:param text:
		:return:
		'''
		doc = pq(text)
		items = doc('div.job-primary').items()
		for i, item in enumerate(items):
			result = {}
			job_info = item('div.info-primary')
			company_info = item('div.info-company')
			public_info = item('div.info-publis')
			job_name = job_info('div.job-title').text()
			job_salary = job_info('span.red').text()
			job_url = 'https://www.zhipin.com' + job_info('h3.name a').attr('href')
			job_tags = job_info('p').text()
			company_name = company_info('h3.name a').text()
			company_tags = company_info('p').text()
			public_name = public_info('h3.name').text()

			result['job_name'] = job_name
			result['job_salary'] = job_salary
			result['job_url'] = job_url
			result['job_tags'] = job_tags
			result['company_name'] = company_name
			result['company_tags'] = company_tags
			result['public_name'] = public_name
			yield result

	def get_csv(self, items=None):
		data = pd.DataFrame(items)
		data.to_csv(os.path.join(self.config.data_path, '%s_%s.csv'%(self.city, self.job)))

	def main(self):
		'''

		:return:
		'''
		items = []
		for i in range(1, self.max_page + 1):
			print('start to spider page: %s'%i)
			url = self.base_url % (i, i)
			text = self.get_html(url)
			for item in self.get_item(text):
				items.append(item)
		self.get_csv(items)


if __name__ == '__main__':
	factory = bossZhiPin_spider(city='上海', job='数据挖掘', max_page=10)
	factory.main()
	# url = 'https://www.zhipin.com/c101020100/?query=数据分析&page=2&ka=page-2'
	# text = factory.get_html(url)
	# for i, j in enumerate(factory.get_item(text)):
	# 	print(i, j)
