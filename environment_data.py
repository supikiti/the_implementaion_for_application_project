import pandas as pd
import numpy as np

class Environment():
	def __init__(self, csv_path="data/fukushima_wind.csv"):
		self.wind_data = self.read_wind_data_from_csv(csv_path)
		self.wind_power_rank = self.calc_wind_power_rank(self.wind_data)
		self.day = np.array([1, 1, 1, 1, 0, 0, 0, 0] * 365 * 20)
		self.can_work = self.calc_time_to_work()

	def read_wind_data_from_csv(self, csv_path):
		df = pd.read_csv(csv_path)[2:]
		wind_over_ten_meter = np.power(np.sum(np.power(df, 2), 1), 0.5)
		wind_over_ten_meter = (15. / 10.) ** (1.0 / 7.0) * wind_over_ten_meter
		return wind_over_ten_meter

	def calc_wind_power_rank(self, wind):
		wind_power_rank = np.where(wind>16.98, 4, np.where(wind>10.0, 3, \
						  np.where(wind>8.15, 2, np.where(wind>2.72, 1, 0))))
		return wind_power_rank

	def make_markov_array(self):
		markov_array = np.zeros([5, 5])
		pre_rank = self.wind_power_rank[0]
		for t in range(1, len(self.wind_power_rank)):
			temp_rank = self.wind_power_rank[t]
			markov_array[pre_rank, temp_rank] += 1
			pre_rank = temp_rank
		markov_array = markov_array / np.sum(markov_array, 1).reshape(-1, 1)
		return markov_array

	def make_wind_histgram(self):
		hist = [0, 0]
		markov_array = self.make_markov_array()
		for t in range(20 * 365 * 4 - 1):
			pre = hist[-1]
			tmp = np.random.choice(np.arange(5), p=markov_array[pre])
			hist.extend([tmp, tmp])
		self.wind_hist = np.array(hist)
		return self.wind_hist

	def calc_time_to_work(self):
		hist = self.make_wind_histgram()
		nice_weather = np.where(hist >= 3, 0, 1)
		return nice_weather & self.day

	def return_can_work_array(self):
		return self.can_work

	def return_day(self):
		return self.day
