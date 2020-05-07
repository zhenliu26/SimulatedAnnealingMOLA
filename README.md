# Simulated Annealing (Metropolis Algorithm) in Multi-Objective Land Allocation #

## Introduction ##
It is often the case that we need to make site selection or land allocation decisions that satisfy multiple objectives, each expressed in its own suitability map. These objectives may be complementary in terms of land use or they may be conflicting. There are several methods to solve such allocation problems with multiple objectives. 

## Objectives ##
We will use Simulated Annealing (Metropolis Algorithm) to allocate land for two competing objectives -- residential development and industrial development. The areas of both regions are 200 hectares, which equals 5000 pixels on the map. The contiguity and compactness are not required in this application.

## Study Area ##
Westborough, a town in Worcester County, Massachusetts, United States.

## Data ##
The suitability maps for residential development and industrial development in Westborough.

## Methodology ##
1.	allocate land uses randomly to start
Randomly allocate the residential area and the industrial area whose areas are both 5000 pixels on the map. Assign residential areas as 1 and industrial areas as 2. The rest of the areas on the map are assigned as 0.
2.	randomly swap two pixels from different land uses
The difficulty of this algorithm in this application is how to swap the pixels. All possibilities should be considered in the process: the swaps between residential pixels and industrial pixels; residential pixels and non-value pixels, and industrial pixels and non-value pixels. So, in this project, randomly select two pixels, swap them if there are in different classes.
3.	if aggregate suitability is better, keep the swap.
4.	if not, keep the swap anyways if exp(DSS/c)>random(0,1). (DSS is the difference between the present suitability and the previous suitability; c is the present temperature.)
5.	if iterations=n then adjust cooling factor: c = c * rate_of_decline. (Rate_of_decline is the annealing rate)
6.	if adjustments<m and temperature > T_end, then go to 2.
The parameters in the algorithm are:
The start temperature (T_start) is 2000; the end temperature (T_end) is 1e-20; the rate of decline (a) is 0.995; the number of inner iterations (n) is 50.
After we get the results, we use the Crosstab in Terrset to find the difference between two allocation maps (MOLA and Simulated Annealing).

## Results ##
The total suitability in MOLA is 1,115,257, and the total suitability in the simulated annealing is 1,048,880.5.

## Analysis ##
Compared with the algorithms in Terrset, the total suitability of the simulated annealing algorithm is less and the time it takes is much longer. Also, we can tell the relationship between iteration number and total suitability is still increasing, which means the total suitability doesn’t reach to the maximum suitability. As for the two result allocation maps, they are similar. However, the distribution of sites in the allocation map by MOLA is more clustered than the one by Simulated Annealing. We can find that there are a majority of pixel choices are different in two maps, and both total suitabilities of two classes (Residential and Industrial) are higher in MOLA in Terrset.

## Conclusions ##
Due to randomly swapping pixels on the map, the uncertainty of the results and time increases in the simulated annealing algorithm. Allocation analysis by using the simulated algorithm is time-consuming, which means that it is not realistic to apply it to some daily used software. So, accelerating the process of simulated annealing is important for future applications in MOLA. Also, for the simulated annealing algorithm, from the curve which shows the relationship between the total suitability and the number of iterations, we can see the total suitability of the map is still increasing. The restriction in the algorithm is the end temperature. If the end temperature is less, the total suitability will be higher. Considered the time, the simulated annealing algorithm is not a great algorithm, However, given enough time, it will find out the best allocation map for the project.
