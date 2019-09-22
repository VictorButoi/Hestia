import numpy as np
#dtakes in (xlong,ylat) which is center of square. ef assignLocation:
def assignLocation(x,y,drivers):
    tuple_list = list()
    #1 degree of longitude ~=~ 55.051 miles? assuming latitude is the same
    #l is length of the square in degrees
    l = 25/55.051
    #number of sub-squares
    a = np.sqrt(drivers)
    long_array = np.linspace(start = x-l/2, stop = x+l/2, num = a+1)
    print(long_array)
    lat_array = np.linspace(start = y-l/2, stop = y+l/2, num = a+1)
    print(lat_array)
    for _ in range(drivers):
        random_squarex = np.random.randint(a)
        print(random_squarex)
        random_squarey = np.random.randint(a)
        xc = (long_array[random_squarex]+long_array[random_squarex+1])/2
        yc = (lat_array[random_squarey]+lat_array[random_squarey+1])/2
        driver_tuple = (xc, yc)
        tuple_list.append(driver_tuple)
    return tuple_list

def main():
    cute=assignLocation(-94.5785667, 39.0997265,5)
    for i in cute:
        print(i)

main()