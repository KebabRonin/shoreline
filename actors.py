import random as rd


class Robot:
	def __init__(self, serial_number, start_rnd, end_rnd, seed=None):
		# private, const:
		self.serial_number = serial_number
		self.start, self.end = start_rnd, end_rnd
		# private, setters/getters:
		self.active, self.healthy = False, True

	def __str__(self):
		return f"Robot <{self.serial_number:<4}|{self.start:<3}->{self.end:>3}> Lifetime: {self.end - self.start + 1}"

	def work(self):
		if self.active:
			if self.healthy and rd.randint(1, 100) <= 90:
				return "working"
			else:
				if self.healthy:
					self.healthy = False
					return "broken down"
				return "broken"
		else:
			return "inactive"




class OutOfOpsException(Exception):
	pass


def three_checks(c):
	fixed = 0
	try:
		for r in c.robots:
			if c.read_active(r) == True and c.read_health(r) == False:
				c.fix(r)
				fixed += 1
	except OutOfOpsException:
		pass
	return fixed

def two_checks(c):
	fixed = 0
	try:
		for r in c.robots:
			if c.read_health(r) == False:
				c.fix(r)
				fixed += 1
	except OutOfOpsException:
		pass
	return fixed


DEFAULT_CONTROLLER_STRATEGY = two_checks

class Controller:
	def __init__(self, identifier, robots: list[Robot], strategy=DEFAULT_CONTROLLER_STRATEGY):
		"""Models a Controller with a capacity of 100 operations per round who monitors a list of `Robots`

		Args:
		- `identifier`: a name for the Controller
		- `robots`: list of robots the Controller
		- `strategy`: function applied to accomplish the Controller's task

			The function must take in the object itself, and may return the number of fixed robots (for use in logging)

			The function must make use of the `read_health`, `read_active` and `fix` methods

			Defaults to `two_checks`
		"""
		if strategy is None:
			strategy = DEFAULT_CONTROLLER_STRATEGY
		if not callable(strategy):
			raise ValueError("Parameter strategy is not callable")
		self.ident = identifier
		self.robots = robots
		self.ops = 100
		self._strategy = strategy
		self.history = []

	def __str__(self):
		contents = ""
		if len(self.robots) > 0:
			contents += self.robots[0].serial_number + " .. " + self.robots[-1].serial_number
		return f"Ctrlr [{self.ident:<4}| strategy: {self._strategy.__name__} <monitors {len(self.robots)} robots>({contents})]"

	def strategy(self):
		self.round_log = []
		result = self._strategy(self)
		self.history.append(self.round_log)
		return result if type(result) is int else 0

	def reset_ops(self):
		self.ops = 100

	def read_health(self, r: Robot):
		if self.ops > 0:
			self.ops -= 1
			self.round_log.append(("h", r.serial_number))
			return r.healthy
		else:
			raise OutOfOpsException

	def read_active(self, r: Robot):
		if self.ops > 0:
			self.ops -= 1
			self.round_log.append(("a", r.serial_number))
			return r.active
		else:
			raise OutOfOpsException

	def fix(self, r: Robot):
		if self.ops > 0:
			self.ops -= 1
			r.healthy = True
			self.round_log.append(("f", r.serial_number))
		else:
			raise OutOfOpsException