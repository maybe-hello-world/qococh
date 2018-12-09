# qococh project
## General Description
This is Junction 2018 project. The task was to implement schedule changes management system for delivery company using available API data.
This system will listen to the schedule of flights and trucks and will replan delivering of shipments using another available flights and trucks. Or at least will try to do it.

Being based on math, graph algorithms and our understanding of logistic company everyday work, this solution try to react to delays and cancellations of flights and ship everything-that-needed with aware of the available volume and weight in different trucks and planes.
Backpack task solver not included, but in v0.2 we hope it will be.

On top of the algo, there's a pretty visualization for an operator to be aware of different events like reroutings of shipments and flight/truck movements.  Also, there's a dashboard for undeliverable shipments to help operators to react to them in proper time.

The project is divided into three parts - data gathering system (API pinger :D), great-and-awful-graph-algorithm-part and visualization part. Of course, all parts are rather isolated so the can be used with another software or in another project, though we ask you to remember that's it hackathon and we didn't have much time.

The software is complete and working right now, maybe not (far-far not) production ready, but it can be used right now and do not depends on presented data - you can change input data and see how it react to it.
## API Description
API with data about transports, including truck and aircraft schedules and shipment details. 
API generates disruptions to schedules, which your solution should deal with.
## Implementation Description
The main logic of system is a slightlly modified version of Dijkstra's algorithm. 
We  used python networkx library for graph representation and dash for it's visualisation.
