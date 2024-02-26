import random as rd

class Robot:
	def __init__(self, serial_number, start, end, seed=None):
		# private, const:
		self.serial_number = serial_number
		self.start, self.end = start, end
		# private:
		self.active, self.healthy = False, True

	def __repr__(self):
		return f"Robot <{self.serial_number:<4}|{self.start:<3}->{self.end:>3}> Lifetime: {self.end - self.start + 1}"

	def work(self):
		if self.active:
			if self.healthy and rd.randint(1, 100) <= 90:
				return 1
			else:
				self.healthy = False
				return -10
		else:
			return 0


class OutOfOpsException(Exception):
	pass

def naive(c):
	try:
		while True:
			for r in c.robots:
				if c.read_health(r) == False:
					c.fix(r)
	except OutOfOpsException:
		pass

class Controller:
	def __init__(self, ident, robots):
		self.ident = ident
		self.robots = robots
		self.ops = 100
		# self.strategy = naive.__get__(self)

	def __repr__(self):
		def r_id(idx):
			return self.robots[idx].serial_number
		return f"Ctrlr [{self.ident:<4}| <monitors {len(self.robots)} robots>({r_id(0)}, {r_id(1)}, {r_id(2)}, .. {r_id(-2)}, {r_id(-1)})]"


	def reset_ops(self):
		self.ops = 100

	def read_health(self, r):
		if self.ops > 0:
			self.ops -= 1
			# print("read_health", r.serial_number)
			return r.healthy
		else:
			raise OutOfOpsException

	def read_active(self, r):
		if self.ops > 0:
			self.ops -= 1
			# print("read_active", r.serial_number)
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