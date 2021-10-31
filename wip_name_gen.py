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
	__model = {}

	def __init__(self, pad_length):
		self.pad_util = MarkovUtility('_', pad_length)

	def transform(self):
		result = self.pad_util.get_pad()
		start = 0
		end = self.pad_util.get_pad_length()
		current = result[start:end]
		previous = None

		while True:
			sel = 1 - random.random()
			for kv in self.__model[current].keys():
				if sel > self.__model[current][kv]:
					sel -= self.__model[current][kv]
				else:
					result += kv
					previous = current = result[-(self.pad_util.get_pad_length()):]
					break

			if current == self.pad_util.get_pad(
			) and previous is not self.pad_util.get_pad() and len(
					result) > self.pad_util.get_pad_length():
				break

		return self.pad_util.strip_pad(result)

	def fit(self, list):
		data = self.pad_util.pad_data(list.copy())
		for item in data:
			start = 0
			end = self.pad_util.get_pad_length()

			while end < len(item):
				c = item[start:end]
				if c not in self.__model:
					self.__model[c] = {item[end]: 1}
				else:
					if item[end] not in self.__model[c]:
						self.__model[c][item[end]] = 1
					else:
						self.__model[c][item[end]] += 1
				start += 1
				end += 1

		for k in self.__model.keys():
			sub_total = sum(self.__model[k].values())
			for ky in self.__model[k].keys():
				self.__model[k][ky] /= sub_total


class MarkovUtility:
	def __init__(self, pad_char, pad_length):
		self.__pad_char = pad_char
		self.__pad = self.__pad_char * pad_length

	def get_pad(self):
		return self.__pad

	def get_pad_length(self):
		return len(self.__pad)

	def pad_data(self, data):
		data = [self.__pad + x + self.__pad for x in data]
		return data

	def strip_pad(self, text):
		return text.replace(self.__pad_char, '')


if __name__ == "__main__":
	dh = DataHandler()
	mc = MarkovChain(5)
	the_list = dh.get_list()

	mc.fit(the_list)
	for _ in range(20):
		title = mc.transform()
		if title not in the_list:
			print(title)
		else:
			print('Title in list -> ', title)

