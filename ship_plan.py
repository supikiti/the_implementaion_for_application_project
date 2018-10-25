import numpy as np

from ships import Ships

class Ship_plan():
	def __init__(self, total_number_of_ships, environment, windfarm):
		self.all_ships = [Ships(s) for s in range(total_number_of_ships)]
		self.environment = environment
		self.windfarm = windfarm
		self.total_driving_cost = 0
		self.driving_cost_per_three_hour = 125000
		self.all_windfarm = windfarm.all_windfarm

	def time_step(self, t):
		for sh in self.all_ships:
			self.ship_should_leave_current_windfarm(sh, t)

	def ship_should_leave_current_windfarm(self, ship, t):
		# 夕方 ~ 朝
		if self.check_day(t):
			if not self.check_day(t-1):
				self.total_driving_cost += self.driving_cost_per_three_hour
			#ship.stay_harbor = True
			self.leave_or_stay_current_windfarm(ship)
		# 朝 ~ 夕方
		else:
			self.all_windfarm[ship.target_windfarm].there_is_ship = True
			self.leave_or_stay_current_windfarm(ship)
			self.total_driving_cost += self.driving_cost_per_three_hour

	def leave_or_stay_current_windfarm(self, ship):
		# 移る
		if self.all_windfarm[ship.target_windfarm].need_inspection:
			pass
		else:
			# ここに次はどうするかの選択をする
			ship.target_windfarm = self.select_next_windfarm()

	def select_next_windfarm(self):
		return np.argmax(self.windfarm.time_from_last_inspection_all)

	def check_day(self, t):
		if self.environment.day[t] == 0:
			return True
		else:
			return False
