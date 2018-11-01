import numpy as np

from ships import Ships

class Ship_plan():
	def __init__(self, total_number_of_ships, environment):
		self.total_number_of_ships = total_number_of_ships
		# 点検船
		self.all_ships = [Ships(s) for s in range(total_number_of_ships)]
		self.environment = environment
		self.total_driving_cost = 0
		self.driving_cost_per_three_hour = 125000

	def time_step(self, t, windfarm_state):
		self.windfarm = windfarm_state
		self.all_windfarm = windfarm_state.all_windfarm
		for i in range(len(self.all_ships)):
			self.ship_should_leave_current_windfarm(i, t)
			self.calc_driving_cost()
		return self.all_windfarm

    # 毎時間, 沖合に出ている船の数分の運転費を計算する
	def calc_driving_cost(self):
		# 港に残っている船の数
		number_of_ships_in_harbor = sum([sh.stay_harbor for sh in \
										 self.all_ships])
		# 港に残っていない船の数
		number_of_driving_ships = self.total_number_of_ships - \
									number_of_ships_in_harbor
		# 港に残っていない船の数 × 1stepあたりの運転費
		self.total_driving_cost += number_of_driving_ships * \
									self.driving_cost_per_three_hour

	def ship_should_leave_current_windfarm(self, ship_num, t):
		this_ship_target_windfarm = self.all_ships[ship_num].target_windfarm
		# 担当する風車の点検が終わったら
		if not self.all_windfarm[this_ship_target_windfarm].need_inspection:
			next_windfarm = self.select_next_windfarm()
			self.all_ships[ship_num].target_windfarm = next_windfarm
			self.all_windfarm[next_windfarm].there_is_ship = True

		# 担当する風車の点検がまだ終わっていない
		else:
			# まだ元の風車の点検が終わっていない
			# 夜かどうか
			if self.check_night(t):
				self.all_ships[ship_num].stay_harbor = True
			# 昼
			else:
				self.all_ships[ship_num].stay_harbor = False

	def select_next_windfarm(self):
		# 点検が必要な風車があればそちらに回る.

		#if sum(self.windfarm.check_need_inspection_all()) >= 1:
			#tmp = 
		tmp = np.argmax(self.windfarm.time_from_last_inspection_all())
		self.all_windfarm[tmp].there_is_ship = True
		self.all_windfarm[tmp].time_from_last_inspection = 0
		return tmp

	# environment.day = 1ならば昼, 0ならば夜
	# 夜ならばTrueが返る.
	def check_night(self, t):
		if self.environment.day[t] == 0:
			return True
		else:
			return False
