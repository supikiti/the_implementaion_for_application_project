class Ships():
	def __init__(self, target_windfarm):
		# この船がどこの風車にいるか
		# 港に残り続けるなら -1
		self.target_windfarm = target_windfarm
		# 港にいるかどうか
		#self.stay_harbor = False
