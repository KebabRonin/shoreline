# Task
<details>
<summary>Full text</summary>

Your task will be to create a simulation of a fleet of robots that do some work in order to generate points over a sequence of rounds.


You are managing 10.000 robots. Each robot has a unique serial number, an activation round, a deactivation round, an active state, a health state and a task to generate points.


In the beginning of the simulation each robot will be assigned an activation round as a random number between 1 and 30, and a deactivation round as a random number between 30 and 60. When a robot reaches its activation round it becomes active; when it reaches its deactivation round, it becomes inactive.


Each active robot generates 1 point per round if healthy after performing a workload. A workload consists in generating a number between 1 and 100. If the value is below or equal to 90 the point is generated. If the value is above 90 then the robot becomes unhealthy instead. Until repaired, an active, unhealthy robot generates negative points, -10 per round.


The robots cannot fix themselves. They can only be repaired by a fleet of controllers. A controller can monitor a range of robots and repair the unhealthy ones. A robot doesn’t know about the controller but the controller knows about robots. A controller is limited to 100 robot interactions (read robot active status, read robot health status, repair robot) per round. Each round, a controller also consumes 20 points for its own effort.


The controllers’ fleet has the following characteristics:

- Controllers do not know about each other

- Controllers are not directly reachable but are managed from a command center that contains the list of serial numbers of the robots through which a certain controller can interact with a certain robot.

- The only permitted interactions for the controller are these 3: read robot active status, read robot health status, repair robot


The command center knows:

- Total number of robots, not the robot details

- List of controllers

</details>

Your mission is to generate a minimum of 50.000 points in 60 rounds.


In a language of your choice, implement a solution that simulates the scenario to generate the points. The solution includes: a description of the model, explanations for the design and algorithm choices, a runnable simulation of the 60 rounds that displays at least the final score.

# Solution

-


# Thought Process

I chose python because it allows for fast prototyping and supports both OOP and functional programming.

### Probabilities/Point considerations

##### _Robot performance:_
Average robot livespan is 30 rounds
- Worst case: -3.000.000 (-10 * 30 * 10.000)
- Best case: 300.000 (1 * 30 * 10.000) [5.000 per round]
- Target: 50.000 [834 per round]

##### _Simulation analysis:_
Average robots active: 5.000
Average broken robots per round: 500 (10% of 5.000) [-> -5.000 per round if no repairs]

### Interpretation of constraints

##### Controllers

- The controllers act after all robots have acted on a round
- Since all controllers are the same, they should all have an even range of robots (and together cover all 10.000 robots)

##### Robots

- The -10 point penalty for unhealthy robots is applied at the end, only after the controllers have done their job (?)
- If a robot is activated and deactivated in the same round, it still does its workload (but if it breaks down it doesn't generate -10 points since it isn't active anymore)


# Strategy (ies?)

## Per robot procedure

```py
if c.read_health(r) == False:
	c.fix(r)
```
- Each robot in range uses 1-2 ops. This means each controller can process between 100-50 robots per round
- The active state of robots is never checked, because of added overhead for each robot (worst case 33 robots checked vs. 50 per round).

	It may be more useful to only check health state and risk fixing inactive robots, if it means an overall increase in robot throughtput.

	Plus, since an inactive robot can't break down, this means at most one 'useless' fix per robot.

	Note: I made this decision with the aim of optimising the number of operations. If the 'fixing' operation was more costly, then both checks would be necessary.

## Robot range distribution

### Naive (best)

***Each controller evaluates the range of robots in the order of their ids.***

Best score: 118.257

Best performance achieved with 110 - 125 controllers [penalty 2.200 - 2.500 points per round]

### Other ideas

- Naive with reversing order (not implemented, as other ideas)

	***Each controller evaluates the range of robots in the order of their ids. Each round the order changes (ascending/descending)***

- Since the Naive method evaluates the robots in the same

- Should be the same

### Phases

***Each controller evaluates the range of robots in the order of their ids, alternating between even and odd ids depending on the current round.***

-

### State monitoring