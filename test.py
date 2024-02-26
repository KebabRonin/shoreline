"""
    50_000 - target (budget = 540_000 = 9_000 / round)
-5_900_000 - worst robot performance
   590_000 - best  robot performance
   300_000 - real best robot performance


-20 * 60 * N_CONTROLLERS = -1_200 * N_CONTROLLERS (+20 daca nu se pune ultima runda)

"""
import matplotlib.pyplot as plt


def probs():
	p = 0.9 ** 10
	# probs = [p * (0.1 ** i) / (0.9 ** i) for i in range(10)]
	probs = [0.9 ** i for i in range(20)] # => dupa ~6 runde 50% e unhealthy

	plt.plot(probs)
	plt.show()
# probs()
import random as rd

class Robot:
	def __init__(self, serial_number, start, end):
		self.serial_number = serial_number
		self.start, self.end = start, end
		self.active, self.healthy = False, True

	def __repr__(self):
		return f"<{self.serial_number:<4}|{self.start:<3}->{self.end:>3}> == {self.end - self.start}"

class OutOfOpsException(Exception):
	pass

class Controller:
	def __init__(self, ident, start, end):
		self.ident = ident
		self.start, self.end = start, end
		self.ops = 100

	def __repr__(self):
		return f"[{self.ident:<4}|{self.start:<3}->{self.end:>3}]"

	def reset_ops(self):
		self.ops = 100

	def rh(self, r):
		if self.ops > 0:
			self.ops -= 1
			# print("rh", r.serial_number)
			return r.healthy
		else:
			raise OutOfOpsException
	def ra(self, r):
		if self.ops > 0:
			self.ops -= 1
			# print("ra", r.serial_number)
			return r.active
		else:
			raise OutOfOpsException
	def fix(self, r):
		if self.ops > 0:
			self.ops -= 1
			r.healthy = True
			# print("fix", r.serial_number)
		else:
			raise OutOfOpsException
log = []
PHASES = 4
class Simulation:
	def __init__(self, n_controllers):
		# N_CONTROLLERS = 125 # int(10_000/(PHASES*100))
		RB = int(10_000 / n_controllers)
		self.robots = [Robot(i, rd.randint(1, 30), rd.randint(30, 60)) for i in range(10_000)]
		self.controllers = [Controller(i, i*RB, (i+1)*RB-1) for i in range(n_controllers)]
		self.current_step = 0

	def robot_step(self):
		points = 0
		activated, dezactivated, broken_down, worked = 0, 0, 0, 0
		for r in self.robots:
			if r.start == self.current_step:
				activated += 1
				r.active = True

			# work
			work = rd.randint(1, 100)

			if r.active:
				if r.healthy and work <= 90:
					points += 1
					worked += 1
				else:
					if r.healthy:
						r.healthy = False
						broken_down += 1
					# points -= 10

			if r.end == self.current_step:
				dezactivated += 1
				r.active = False

		act    = len([r for r in self.robots if r.active])

		log.append([act])
		# print(f"=== Round {self.current_step} ===\nActivated:{activated}\nWorked:{worked}\nBroken:{broken_down}\nDez:{dezactivated}")
		return points

	def controller_step(self):
		fixed = 0
		for c in self.controllers:
			c.reset_ops()
			phase = self.current_step % PHASES
			robs = [r for idx, r in enumerate(self.robots[c.start:c.end+1]) if idx % PHASES == phase]

			try:
				i = 0
				while True:
					# r = self.robots[rd.randint(c.start, c.end)] # -320_840 (100)
					r = self.robots[(c.start + i) % len(self.robots)] # -1_155_998 (50)
					# r = self.robots[(c.start + i + phase * (c.end - c.start)/PHASES) % len(self.robots)] # -2_120_401 (100)
					# r = robs[i % len(robs)]
					i += 1

					if c.rh(r) == False:
						fixed += 1
						c.fix(r)
			except OutOfOpsException:
				pass
			# print(c.ops, end=' ')
		broken = len([r for r in self.robots if r.active and not r.healthy])
		log[-1] += [broken, fixed]
		# print(f"Fixed:{fixed} (Total broken remaining:{len([r for r in self.robots if r.active and not r.healthy])})")
		return -20 * len(self.controllers)

	def run_sim(self, rounds=60):
		self.current_step = 0
		s = 0
		for _ in range(60):
			self.current_step += 1
			s += self.robot_step()
			s += self.controller_step()
			# s -= 10 * len([r for r in self.robots if r.active and not r.healthy])
		return s

# rd.seed(10)
tot = 0
NRUNS = 1
for _ in range(NRUNS):
	c = Simulation(110).run_sim()
	tot += c
	print("Score:", c)
print("Mean:", tot / NRUNS)

print("Total broken:", sum(map(lambda x: x[1], log)))
plt.plot(list(map(lambda x: x[0], log)), label="active")
plt.plot(list(map(lambda x: x[1], log)), label="broken")
plt.plot(list(map(lambda x: x[2], log)), label="fixed")
plt.legend()
plt.show()