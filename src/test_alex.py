import numpy as np
from scipy.ndimage.interpolation import shift
#dtakes in (xlong,ylat) which is center of square. ef assignLocation:
def assignLocation(x,y,drivers):
    tuple_list = list()
    #1 degree of longitude ~=~ 55.051 miles? assuming latitude is the same
    #l is length of the square in degrees
    l = 10/55.051
    #number of sub-squares
    a = np.sqrt(drivers)

    long_array = np.linspace(start = x-l/2, stop = x+l/2, num = a+1)
    long_array1 = shift(long_array,-1,cval=0)
    long_array = (long_array+long_array1)/2
    long_array = np.resize(long_array,(1,int(a))).flatten()

    lat_array = np.linspace(start = y-l/2, stop = y+l/2, num = a+1)
    lat_array1 = shift(lat_array,-1,cval=0)
    lat_array = (lat_array+lat_array1)/2
    lat_array = np.resize(lat_array,(1,int(a))).flatten()

    for _ in range(drivers):
        random_squarex = np.random.randint(int(a))
        random_squarey = np.random.randint(int(a))
        xc = long_array[random_squarex]
        yc = lat_array[random_squarey]
        driver_tuple = (xc, yc)
        tuple_list.append(driver_tuple)
    return tuple_list

def main():
    cute=assignLocation(-94.5785667, 39.0997265,50)
    for i in cute:
        print(i)

main()