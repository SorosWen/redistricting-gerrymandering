# redistricting-gerrymandering
In development. This repo is purely for fun at this point and is not heading in any particular direction. 

This repo is meant to explore several algorithm that are related gerrymandering and redistricting, through hypothetical scenarios. 

This repo will also explore several extreme cases and test the limit of the algorithms. In the long term I wish to develop some sort of application that simulate political polling. Hopefully the end product can bring awareness of partisian gerrymandering. 

### Modeling 
So first we need to model this problem. We are going to consider the premise similar to how real life political groups approach a district/constituency redraw problem. 

Premise: 
- There are different types of objects 
- We want to divide objects in a map into a defined amount of partitions. 
- The partition has to be physically continuous and has equal amount of population. 
- Each object has a property. There are two or more enumeration of this property a object can take one. Each object can take on exactly one enumeration at once. 
- DominentPartition: one cluster such that 50% of the population has the same property. 

Objective: 
- Find a physcially continuous partition such that the number of DominentPartition of a particular enum is maximized. 
