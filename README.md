# redistricting-gerrymandering
In development. This package development is aimed to bring more transparency in the redictricting process. 

This repo is meant to explore several algorithm that are related gerrymandering and redistricting, through hypothetical scenarios. 

This repo will also explore several extreme cases and test the limit of the algorithms. In the long term I wish to develop some sort of application that simulate political polling. Hopefully the end product can bring awareness of partisian gerrymandering. 

### Modeling 
So first we need to model this problem. We are going to consider the premise similar to how real life political groups approach a district/constituency redraw problem. 

Premise: 
- There are a numbers of precints in a map, each with different or identical populations.
- We want to divide precints in a map into a defined amount of partitions. 
- The partition has to be physically continuous and has equal amount of population. 
- Each precinct has a property indicating the voting preference of this precinct. This propery has a set of possible values. Each precinct can take on exactly one value at a time. 
- DominentPartition: meaning a partition such that > 50% of the population in the partition has the same property. 

Objective: 
- Find a physcially continuous partition such that the number of DominentPartition of a particular enum is maximized. 

### Development Tool
Most of the code will be done in Jupiter Notebook using Python and matplotlib. 



https://user-images.githubusercontent.com/29587421/193418060-c4c3d10a-dbca-4e4f-ad56-eed66a0b138f.mp4

