## Work experience @ STFC Rutherford Appleton Laboratory, Harwell

### Some demo output from real data
![](demooutput2.png)

#### Data sourced from https://gist.githubusercontent.com/StewMH/9f75f8c2915e33b4248ed994173ebc53/raw/03a4f4221a424167beb824ad902768c900a08c50/event through Kaggle. The data is currently stored locally in the repo, allowing the code to run offline without pulling the data from the Gist.

## So what does it actually do?
#### This program takes many points from a particle detector around a collision (like that of the ATLAS detector) and aims to trace viable paths between points to reconstruct what particles were produced in the collision. The program does not predict the particles produced, but it plots the possible paths of particles.

## How does it work?
#### The front view works using the fact that any three points have only one circle, or one quadratic polynomial, that passes through them all. The code tries all possible combinations of the data, plots the circle that passes through each combination, and checks whether this goes near the origin, where the collisions would have happened. If it does, then the section of the curve going from the origin to the outmost point is plotted.

#### The side view is a projection of all the possible tracks into the plane. As the magnetic field is along the z-axis only, the tracks in this view are straight lines. Again, we find all the possible combinations of points, and check to see if they make a straight line which passes through the z-axis between -3000 and 3000 (the dimensions of the part where collisions can occur). This is done by finding the road angle between the points - in other words, take the point nearest the z-axis, find the angle from this point to the second point, then from the same point to the third point, then find the difference in these angles. If the road is less than a certain, very small angle, then the points are assumed to be part of the straight track made by the particle, and this line is plotted along with the points. 
