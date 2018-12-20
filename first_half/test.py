from environment_data import Environment

env = Environment()
print(env.wind_power_rank[:100])
print(env.wind_power_rank.shape)
print(env.return_day().shape)
print(env.return_can_work_array().shape)
