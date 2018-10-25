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
	environment = Environment()
	windfarm_state = Windfarm_state(environment)

	# 初期状態は, 0 ~ 3まで船が点検している状態
	for i in range(args.total_number_of_ships):
		windfarm_state.all_windfarm[i].there_is_ship = True
		windfarm_state.all_windfarm[i].need_inspection = True
	ship_plan = Ship_plan(args.total_number_of_ships, environment, \
						  windfarm_state)
	for t in range(args.total_step_by_three_hour):
		windfarm_state.time_step(t)
		ship_plan.time_step(t)
	print("total_calc_generated_kwh", windfarm_state.total_calc_generated_kwh())
	print("total_driving_cost", ship_plan.total_driving_cost)
	print("repayment cost", 400000000 * args.total_number_of_ships)
	print("total_profit", windfarm_state.total_calc_generated_kwh() -
						  ship_plan.total_driving_cost - 400000000 *
						  args.total_number_of_ships)

if __name__ == "__main__":
	sys.exit(main())
