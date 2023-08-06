# easy-trilateration
Trilateration example using least squares method in scipy.

![](https://raw.githubusercontent.com/agusalex/Least-Squares-Trilateration/master/img.png)

Trilateration enables the unknown point to be found. However a since there are a number of samples a non linear least squares method needs to be used to find the solution that has the least error. 

It is distinct from triangulation which has a series of angles to an unknown point. Trilateration uses a series of distances to an unkown point.


## Method
This code uses the [scipy.optimize.least_squares](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html) method.






