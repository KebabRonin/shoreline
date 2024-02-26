from actors import Robot, Controller, OutOfOpsException
import random as rd, matplotlib.pyplot as plt

PHASES = 4
class Simulation:
	def __init__(self, n_controllers, seed=None):
		rd.seed(seed)
		# N_CONTROLLERS = 125 # int(10_000/(PHASES*100))
		RB = int(10_000 / n_controllers)
		self.robots = [Robot(i, rd.randint(1, 30), rd.randint(30, 60)) for i in range(10_000)]
		self.controllers = [Controller(i, self.robots[i*RB: (i+1)*RB]) for i in range(n_controllers)]
		self.current_step = 0
		self.log = []
		self.history = ["" for _ in range(10_000)]

	def robot_step(self):
		points = 0
		activated, deactivated, broken_down, worked = 0, 0, 0, 0
		for r in self.robots:
			if r.start == self.current_step:
				activated += 1
				r.active = True

			r.work()
			# points += max(0, status)

			if r.end == self.current_step:
				deactivated += 1
				r.active = False

		act = len([r for r in self.robots if r.active])

		self.log.append([act])
		return points

	def controller_step(self):
		fixed = 0
		sn  = None
		broken = len([r for r in self.robots if r.active and not r.healthy])
		for c in self.controllers:
			c.reset_ops()

			phase = self.current_step % PHASES
			robs = [r for idx, r in enumerate(self.robots) if idx % PHASES == phase]

			try:
				i = 0
				while True:
					r = self.robots[i % len(self.robots)]
					i += 1

					if c.read_health(r) == False:
						c.fix(r)
						fixed += 1
						sn = r.serial_number
			except OutOfOpsException:
				pass
		self.log[-1] += [broken, fixed]
		return sn

	def run_sim(self, rounds=60):
		self.current_step = 0
		s = 0
		for _ in range(rounds):
			self.current_step += 1
			self.robot_step()
			sn = self.controller_step()
			s += sum(list(map(lambda x: 0 if not x.active else 1 if x.healthy else -10, self.robots)))
			s += -20 * len(self.controllers)
		return s

	def plot_sim(self):
		plt.plot(list(map(lambda x: x[0], s.log)), label="active")
		plt.plot(list(map(lambda x: x[1], s.log)), label="broken")
		plt.plot(list(map(lambda x: x[2], s.log)), label="fixed")
		plt.legend()
		plt.show()


if __name__ == '__main__':
	s = Simulation(125, seed=10)
	print("Score:", s.run_sim())
	s.plot_sim()