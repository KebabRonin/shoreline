from simulation import Simulation
import matplotlib.pyplot as plt
# tot = 0
# NRUNS = 1
# for _ in range(NRUNS):
# 	c = Simulation(110).run_sim()
# 	tot += c
# 	print(c)
# print("Mean:", tot / NRUNS)
# rd.seed(10)
s = Simulation(125, seed=10)
print("Score:", s.run_sim())

plt.plot(list(map(lambda x: x[0], s.log)), label="active")
plt.plot(list(map(lambda x: x[1], s.log)), label="broken")
plt.plot(list(map(lambda x: x[2], s.log)), label="fixed")
plt.legend()
plt.show()