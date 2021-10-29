import os
import sys
import csv
#import numpy as np
import random


class DataHandler:
	def __init__(self):
		pass

	def get_list(self):
		data = []
		with open('game_titles.csv', newline='', encoding='utf-8') as f:
			reader = csv.reader(f)
			data = [item for sublist in list(reader) for item in sublist]
		return data


class MarkovChain:
	_bookend = '_'
	_model = {}
	_pad = None

	def __init__(self, pad_length):
		self.pad_length = pad_length

	def fit(self, data: []):
		self._build_model(self._pad_data(data.copy()))

	def generate(self):
		result = self._bookend * self.pad_length
		start = 0
		end = self.pad_length
		current = result[start:end]
		previous = None

		while True:
			sel = 1 - random.random()
			for kv in self._model[current].keys():
				# print('current kv ', kv)
				if sel > self._model[current][kv]:
					sel -= self._model[current][kv]
				else:
					result += kv
					previous = current
					current = current[1:] + kv
					break

			if current == self._pad and previous is not self._pad and len(
					result) > self.pad_length:
				break

		return self._strip_pad(result)

	def _pad_data(self, data):
		self._pad = self._bookend * self.pad_length
		for i, v in enumerate(data):
			data[i] = self._pad + v + self._pad

		return data

	def _build_model(self, data):
		for item in data:
			start = 0
			end = self.pad_length

			while end < len(item):
				c = item[start:end]
				if c not in self._model:
					self._model[c] = {item[end]: 1}
				else:
					if item[end] not in self._model[c]:
						self._model[c][item[end]] = 1
					else:
						self._model[c][item[end]] += 1
				start += 1
				end += 1

		for k in self._model.keys():
			sub_total = sum(self._model[k].values())
			for ky in self._model[k].keys():
				self._model[k][ky] /= sub_total

	def _strip_pad(self, text):
		return text.replace(self._bookend, '')


if __name__ == "__main__":
	dh = DataHandler()
	mc = MarkovChain(4)
	the_list = dh.get_list()
	
	mc.fit(data=the_list)
	for _ in range(10):
		title = mc.generate()
		if title not in the_list:
			print(title)
		else:
			print('*', title)
			

