
# easy-trilateration
Trilateration example using least squares method in scipy (Graphing tools included).

![](https://github.com/agusalex/easy-trilateration/blob/master/images/img2.png?raw=true)

Trilateration enables the unknown point to be found. However a since there are a number of samples a non linear least squares method needs to be used to find the solution that has the least error. 

It is distinct from triangulation which has a series of angles to an unknown point. Trilateration uses a series of distances to an unkown point.

## How to install

    pip install easy_trilateration


## How to use

    from easy_trilateration.model import *  
    from easy_trilateration.least_squares import easy_least_squares  
    from easy_trilateration.graph import *  
      
    if __name__ == '__main__':  
        arr = [Circle(Point(100, 100), 50),  
      Circle(Point(100, 50), 50),  
      Circle(Point(50, 50), 50),  
      Circle(Point(50, 100), 50)]  
        result, meta = easy_least_squares(arr)  
        create_circle(result, target=True)  
        draw(arr)
	
    
## Method
This code uses the [scipy.optimize.least_squares](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html) method.
