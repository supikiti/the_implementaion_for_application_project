import numpy as np


from windfarm import Windfarm
from environment_data import Environment

class Windfarm_state():
	def __init__(self, environment, total_windfarm_num=200):
		self.environment = environment
		self.all_windfarm = [Windfarm(k, environment.wind_hist) \
							for k in range(total_windfarm_num)]

		self.need_inspection_all = self.check_need_inspection_all()
		self.need_repair_all = self.check_need_repair_all()
		self.progress_repair_time_all = self.check_progress_repair_all()
		self.progress_inspection_time_all = \
			self.check_progress_inspection_all()
		self.time_from_last_inspection_all_ = \
			self.time_from_last_inspection_all()

		self.total_generated_power = self.total_calc_generated_kwh()


	def check_need_inspection_all(self):
		return [wf.return_check_present_situation('inspection')[0] \
				for wf in self.all_windfarm]

	def check_need_repair_all(self):
		return [wf.return_check_present_situation('repair')[0] \
				for wf in self.all_windfarm]

	def check_progress_inspection_all(self):
		return [wf.return_check_present_situation('inspection')[1] \
				for wf in self.all_windfarm]

	def check_progress_repair_all(self):
		return [wf.return_check_present_situation('repair')[1] \
				for wf in self.all_windfarm]

	def time_from_last_inspection_all(self):
		tmp = [wf.time_from_last_inspection
				for wf in self.all_windfarm]
		return tmp

	# 動ける風車の数を返す
	def total_driving_windfarm(self, windfarm):
		count = 0
		for wi in windfarm:
			if wi.need_inspection or wi.need_repair:
				count += 1
		return count

	def total_calc_generated_kwh(self):
		return sum([wf.generated_power for wf in self.all_windfarm]) * 36

	def time_step(self, t, windfarm):
		self.all_windfarm = windfarm
		for wd in self.all_windfarm:
			wd.check_present_situation('inspection', t, \
										self.environment.can_work)
			wd.check_present_situation('repair', t, \
										self.environment.can_work)
