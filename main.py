import argparse
import numpy as np
import matplotlib.pyplot as plt
import sys

from environment_data import Environment
from windfarm_state import Windfarm_state
from ship_plan import Ship_plan

def arg_parse():
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--total_number_of_ships',
						type=int, default=4)
	parser.add_argument('-t', '--total_step_by_three_hour',
						type=int, default=int(20*365*(24/3)))
	args = parser.parse_args()
	return args

def main():
	args = arg_parse()
	print("read environment ...")
	environment = Environment()

	print("construct windfarm_state ...")
	windfarm_state = Windfarm_state(environment)
	plot_array = np.zeros([200, \
						   args.total_step_by_three_hour])
	need_inspection_list = []
	need_repair_list = []
	total_generated_power = []

	# 初期状態は, 0 ~ total_nubmer_of_shipsの風車が点検されている状態
	for i in range(args.total_number_of_ships):
		# 風車に船をセット
		windfarm_state.all_windfarm[i].there_is_ship = True
		# 風車を点検中にする
		windfarm_state.all_windfarm[i].need_inspection = True
	ship_plan = Ship_plan(args.total_number_of_ships, environment, \
						  windfarm_state)
	after_windfarm = windfarm_state.all_windfarm

	for t in range(args.total_step_by_three_hour):
		if t%1000 == 0:
			print("t = {}".format(t))
		windfarm_state.time_step(t, after_windfarm)
		after_windfarm = ship_plan.time_step(t, windfarm_state)
		plot_array[:, t] = [wf.generating_power for wf in \
							windfarm_state.all_windfarm]
		"""
		print([s.target_windfarm for s in ship_plan.all_ships], \
				[s.stay_harbor for s in ship_plan.all_ships])
		"""

		count_need_inspection, count_need_repair = \
			windfarm_state.total_not_driving_windfarm(after_windfarm)
		need_inspection_list.append(count_need_inspection)
		need_repair_list.append(count_need_repair)
		total_generated_power.append(windfarm_state.total_calc_generated_kwh())

	print("total_calc_generated_kwh", windfarm_state.total_calc_generated_kwh())
	print("total_driving_cost", ship_plan.total_driving_cost)
	print("repayment cost", 400000000 * args.total_number_of_ships)
	print("total_profit", windfarm_state.total_calc_generated_kwh() -
						  ship_plan.total_driving_cost - 400000000 *
						  args.total_number_of_ships)
	"""
	for i in range(int(args.total_step_by_three_hour/1000)):
		plt.figure()
		plt.imshow(plot_array[:, i * 1000:((i + 1) * 1000)])
		plt.savefig("data/total_generating_power/" + str(i) + ":" + str(i + 1000) + ".png")
	"""
	plt.figure(figsize=(20, 5))
	plt.plot(np.arange(args.total_step_by_three_hour), need_inspection_list, c="b", label="need_inspection")
	plt.plot(np.arange(args.total_step_by_three_hour), need_repair_list, c="g", label="need_repair")
	plt.legend()
	plt.savefig("data/not_driving_windfarm.png")
	plt.figure(figsize=(20, 5))
	plt.plot(np.arange(args.total_step_by_three_hour), total_generated_power)
	plt.savefig("data/total_generated_power.png")



if __name__ == "__main__":
	sys.exit(main())
