from setuptools import setup

README = '''
# coordinate_geometry

## Features

- Helps to perform various operations on points like calculate distance between them, write equation formed by them   
- Perform various tasks in equation of lines like calculate distance between point and line , find image of point in a line etc  
- find area of triangle formed by three points , incentre , circumcentre, orthocentre etc  

## Important things to know about equations

- equation_type1(slope , y_intercept) --> Creates a line object with slope and y_intercept    
- equation_type2(a, b, c) --> Creates a line object in form ax + by + c = 0  
- equation_type3(x_intercept , y_intercept) --> Creates a line object with x_intercept and y_intercept  
- equation_type4(pt:point , slope) --> Creates a line object with pt ( a point object ) and slope  
- equation_type5(pt:point , pt2:point) --> Creates a line object with given two point objects , throws error if both points are same  

- These types can not be used to make lines parallel to y-axis  

## IMPORTS

from coordinate_geometry.point import *
from coordinate_geometry.equations import *
from coordinate_geometry.triangle import *

## Examples

## Point

#### Distance Formula

p1=point(3,0)  
p2=point(0,4)  
print(p1.distance(p2)) # --> 5.0  

#### Section Formula

Internal division  

p1=point(4,4)  
p2=point(8,8)  
print(p1.section(p2,m=1,n=3)) # --> ( 5.0 , 5.0 )  

External division  

p1=point(4,4)  
p2=point(8,8)  
print(p1.section(p2,m=1,n=3,external=True)) # --> ( 2.0 , 2.0 )  

#### Slope
p1=point(1,1)  
p2=point(3,3)  
print(p1.slope(p2)) # --> 1.0  


## Triangles

A=point(0,0)  
B=point(5,0)  
C=point(5*math.cos(math.pi/3),5*math.sin(math.pi/3))  
t1=Triangle(A,B,C) # NOTE : THIS IS A EQUILATERAL TRIANGLE , SO IT MUST HAVE SAME INCENTRE, ORHTOCENTRE , CENTROID and CIRCUMCENTRE   
print(t1.area()) # --> 10.82532  
print(t1.incenter()) --> ( 2.5 , 1.4433757 )   
print(t1.centroid()) --> ( 2.5 , 1.4433757 )  
print(t1.circumcenter()) --> ( 2.5 , 1.4433757 )  
print(t1.orthocenter()) --> ( 2.5 , 1.4433757 )  


## Line 


#### Solving Two Lines
l1=equation_type2(a=3,b=4,c=-5)  
l2=equation_type2(a=3,b=-4,c=-7)  
print(l1.solve(l2)) # --> ( 2.0 , -0.25   )  

#### Angle Between two lines

l1=equation_type5(point(1,1),point(2,2))  
l2=equation_type5(point(-1,1),point(-3,3))  
print(l1.slope) # --> 1.0  
print(l2.slope) # --> -1.0  
print(l1.angle(l2)) # --> 1.5707963267948966 (PI/2)  
print(l1.is_perpendicular(l2)) # --> True  
print(l1.is_parallel(l2)) # --> False  


#### Distance Between point and line

l1=equation_type4(point(0,0),0) # X axis  
pt=point(3,0)  
pt1=point(0,3)  
print(l1.distance(pt)) # --> 0.0  
print(l1.distance(pt1)) # --> 3.0  

#### Image of a point and foot of perpendicular in a line

l1=equation_type4(point(0,0),1)  
pt=point(1,2)  
print(l1.foot_of_perpendicular(pt)) # --> ( 1.5 , 1.5 )  
print(l1.image_of_point(pt)) # --> ( 2.0 , 1.0 )  

## LICENSE

© 2021 Deepak Kumar Dash  

This repository is licensed under MIT license.  
See LICENSE for details

'''


# This call to setup() does all the work
setup(
    name="coordinate_geometry",
    version="1.0.0.1",
    description="A package that simplifies most of the operation performed on point and line in 2D geometry",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Deepak Kumar Dash",
    author_email="dipudash.2003@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["coordinate_geometry"],
    include_package_data=True,
    install_requires=[],
)