from actors import Robot, Controller
import random as rd
import matplotlib.pyplot as plt

class Simulation:
	# logging
	history_legend = {"inactive":" ","broken":"x","working":"-","broken down":"*"}
	tracked_stats = ["round score", "current step", "activated", "deactivated", "active"] + list(history_legend.keys())

	def __init__(self, nr_controllers:int, seed:int=None, controller_strategy=None):
		self.seed = seed
		self.controller_strategy = controller_strategy
		self.nr_controllers = nr_controllers
		self.reset()

	def reset(self):
		rd.seed(self.seed)
		nctrl = self.nr_controllers
		self.robots = [Robot(i, rd.randint(1, 30), rd.randint(30, 60)) for i in range(10_000)]
		# Controller robots are interleaved to distribute any leftover robots evenly between remaining Controllers
		self.controllers = [Controller(i, [r for r in self.robots if r.serial_number%nctrl==i], strategy=self.controller_strategy) for i in range(nctrl)]
		# The Prototype pattern could be used for the Controller class above to speed up instantiation
		self.current_step = 0
		# logging
		self.history = []
		self.robot_history = ["" for _ in range(10_000)]


	def robot_step(self):
		# reset robot logging
		for status in Simulation.history_legend.keys():
			self.log[status] = 0

		for r in self.robots:
			if r.start == self.current_step:
				r.active = True
				self.log["activated"] += 1

			if r.end == self.current_step:
				r.active = False
				self.log["deactivated"] += 1

			status = r.work()

			self.log[status] += 1
			self.robot_history[r.serial_number] += Simulation.history_legend[status]


	def controller_step(self):
		nr_fixed = 0

		for c in self.controllers:
			c.reset_ops()
			nr_fixed += c.strategy()

		broken = len([r for r in self.robots if r.active and not r.healthy])
		self.log["broken"] = broken
		self.log["fixed"]  = nr_fixed
		self.log["active"] = self.log["working"] + self.log["broken"]


	def run_sim(self, rounds=60):
		self.current_step = 0
		s = 0
		for _ in range(rounds):
			self.reset_log()

			self.current_step += 1
			self.robot_step()
			self.controller_step()

			s += self.round_score()

			self.log["round score"] = self.round_score()
			self.log["current step"] = self.current_step
			self.history.append(self.log)
		return s

	def round_score(self):
		score = 0

		# robot points
		for r in self.robots:
			if r.active:
				score += 1 if r.healthy else -10

		# controller costs
		score += -20 * len(self.controllers)

		return score

	def reset_log(self):
		self.log = dict()

		for stat in Simulation.tracked_stats:
			self.log[stat] = 0

	def plot_sim(self, *args:str):
		"""Plots a graph containing the desired data from the simulation's history.

		Arguments are the names of stats found in `Simulation.tracked_stats`
		"""
		for stat in args:
			if stat in self.log:
				plt.plot([s[stat] for s in self.history], label=stat)
		plt.legend()
		plt.title("Simulation results")
		plt.show()

	def save_hist(self, file):
		with open(file, "wt") as f:
			f.write(str(Simulation.history_legend) + "\n")
			f.write('\n'.join(self.robot_history))