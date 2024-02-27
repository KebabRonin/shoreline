from simulation import Simulation
import matplotlib.pyplot as plt


def test(nrounds=1, range_start=95, range_len=10):
	"""Used to create score comparison pictures"""
	heights = []
	for j in range(range_start, range_start + range_len):
		s = 0
		for i in range(nrounds):
			s += Simulation(j).run_sim()
		heights.append(s)
		print("Mean for", j, ":", s/nrounds)
	plt.bar(range(range_start, range_start + range_len), [heights[i] + 20 * 60 * (i+range_start) for i in range(range_len)], label="controller price")
	plt.bar(range(range_start, range_start + range_len), heights, label="points")
	plt.legend()
	plt.show()


if __name__ == "__main__":
	s = Simulation(110)
	print("Score:", s.run_sim())
	# stats: ['round score', 'current step', 'activated', 'deactivated',
	#		   'active', 'inactive', 'broken', 'working', 'broken down']
	s.plot_sim("active", "broken", "fixed", "broken down")
	s.save_hist("hist.txt")