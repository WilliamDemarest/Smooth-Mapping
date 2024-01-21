### Our program, mapping.py helps people explore nature efficiently and prevent trailblazing. 
### It uses the grayscale shade of pixels to map the least steep, quickest path to a certain destination, which will prevent people from getting lost.
### It will also help prevent the destruction of natural areas by trailblazing, whether intended or inadvertent.
import sys
import numpy as np
from matplotlib.pyplot import imread, imsave
import random


# read png file (topographical image)
path = 'map1.png'
image = imread(path)

print(image.shape)

# keeps track of pixels that are already on the path
used_pix = {}

# distance between points
def dist(ax, ay, bx, by):
    da = (ax-bx)**2
    db = (ay-by)**2
    d = (da+db)**0.5
    return d

# checks to make sure path isn't going out of image
def out_of_bounds_check(x, y):
    return x<0 or y<0 or x>=image.shape[0] or y>=image.shape[1]

# find closest boundary region to the end point when a certain region has been fully explored
def search_for_closest_boundary(px, py, dest_x, dest_y):
    min_distance = 1e10
    while (px, py) in used_pix:
        neighbours = [
            (px-1, py-1), (px-1, py), (px-1, py+1),
            (px, py-1), (px, py+1), (px+1, py-1),
            (px+1, py), (px+1, py+1)
        ]
        for neighbor in neighbours:
            if out_of_bounds_check(neighbor[0], neighbor[1]):
                continue
            distance = dist(neighbor[0], neighbor[1], dest_x, dest_y)
            if distance < min_distance:
                px = neighbor[0]
                py = neighbor[1]
                min_distance = distance
    return [px, py]

# avoids edges, points that have already been used in used_pix
def find_clean(px, py, dest_x, dest_y):
    edges = (
        px-1 > 0,
        py-1 > 0,
        px+1 < image.shape[0],
        py+1 < image.shape[1],
    )
    points = []
    # creates route based on which pixels aren't already in used_pix
    if(edges[0]):
        if((px-1, py) not in used_pix):
            points.append([px-1, py])
    if(edges[1]):
        if((px, py-1) not in used_pix):
            points.append([px, py-1])
    if(edges[2]):
        if((px+1, py) not in used_pix):
            points.append([px+1, py])
    if(edges[3]):
        if((px, py+1) not in used_pix):
            points.append([px, py+1])
    if (not out_of_bounds_check(px-1, py-1)) and ((px-1, py-1) not in used_pix):
        points.append([px-1, py-1])
    if (not out_of_bounds_check(px-1, py+1)) and ((px-1, py+1) not in used_pix):
        points.append([px-1, py+1])
    if (not out_of_bounds_check(px+1, py-1)) and ((px+1, py-1) not in used_pix):
        points.append([px+1, py-1])
    if (not out_of_bounds_check(px+1, py+1)) and ((px+1, py+1) not in used_pix):
        points.append([px+1, py+1])
    
    if len(points)==0:
        pt = search_for_closest_boundary(px, py, dest_x, dest_y)
        points.append(pt)
        
    return points

# function to find the closest pixel to the current one that is the same shade (similar shade = similar topography)
def find_next_william(im, px, py, ex, ey):
    base_d = dist(px, py, ex, ey)
    gravity = 0.015 # Bias for moving in direction of goal
    backtrack = -0.01 # Bias for avoiding backtracking (lower value is higher avoidance)

    points = find_clean(px, py, ex, ey)
    if((ex, ey) in points):
        return (ex, ey)
    
    # assign a default that isnt already used (checks how many available points surround the current one)
    new_p = random.choice(points)
    d = dist(new_p[0], new_p[1], ex, ey)-base_d
    
    new_gradient = abs(im[new_p[0], new_p[1], 0] - im[px, py, 0])
    new_score = new_gradient+d*gravity+len(find_clean(new_p[0], new_p[1], ex, ey))*backtrack

    # chooses best point to continue the path
    for p in points:
        gradient = abs(im[p[0], p[1], 0] - im[px, py, 0])
        d = dist(p[0], p[1], ex, ey)-base_d
        score = gradient+d*gravity+len(find_clean(p[0], p[1], ex, ey))*backtrack
        if(score < new_score): 
            if(tuple(p) not in used_pix):
                new_p = p
                new_gradient = abs(im[new_p[0], new_p[1], 0] - im[px, py, 0])
                d = dist(new_p[0], new_p[1], ex, ey)-base_d
                new_score = new_gradient+(d*gravity)+len(find_clean(new_p[0], new_p[1], ex, ey))*backtrack
    used_pix[tuple(new_p)] = True
    return new_p
    
    
# function to draw line using x and y coordinates of start and end points
def route(im, sx, sy, ex, ey):
    base_d = dist(sx, sy, ex, ey)
    p = [sx, sy]

    i = 0
    color_up = True
    while(True):
        if(i>5000):
            break
        p = find_next_william(im, p[0], p[1], ex, ey)
        if(np.isclose(p[0], ex) and np.isclose(p[1], ey)):
            break
        im[p[0], p[1], 0] = (i)*0.001
        im[p[0], p[1], 1] = 0
        im[p[0], p[1], 2] = 1-(i)*0.001
        #imsave("trail_" + path, im)
        if(i == 1000):
            color_up = False
        elif(i == 0):
            color_up = True
        if(color_up):
            i += 1
        else:
            i -= 1
    im[sx, sy, 0] = 0
    im[sx, sy, 1] = 1 
    im[sx, sy, 2] = 0

    im[ex, ey, 0] = 0
    im[ex, ey, 1] = 0 
    im[ex, ey, 2] = 1
    imsave("trail_" + path, im)

# maps the route 

# From top left to another corner:
route(image, 0, 0, image.shape[0]-1, image.shape[1]-1)
#route(image, 0, 0, 0, image.shape[1]-1)
#route(image, 0, 0, image.shape[0]-1, 0)
    
# Random points:
#route(image, random.randrange(image.shape[0]), 
#      random.randrange(image.shape[1]), 
#      random.randrange(image.shape[0]), 
#      random.randrange(image.shape[1]))

# displays the finished route
imsave("trail_" + path, image)