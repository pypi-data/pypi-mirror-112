import sys, math
def minCubes( boxVolume:int, noCubes:list ):
    '''
    This function will return the minimum number of cubes that can fill the box
    params:
        boxVolume: Volume of the bigger box
        noCubes: The number of cubes that we can use to fill the box
    return:
        -1, if we cant fill box
        minCubeCount, in all other scenarios 
    '''
    if boxVolume == 0: #if volume of the box is 0, we can't fill the box, thus return -1
        return -1

    minCubeCount = 0
    for idx in range(len(noCubes)-1, -1, -1): #start filling with the larger cube
        sideSize = pow(2,idx)#get the size of the side based on the index
        cubeVolume = pow(sideSize,3)#calculate volume of cube

        while(boxVolume >= 0  and noCubes[idx] > 0 and noCubes[idx] != 0 and cubeVolume <= boxVolume):
            boxVolume = boxVolume - cubeVolume
            noCubes[idx] = noCubes[idx] - 1
            minCubeCount = minCubeCount + 1

    if boxVolume > 0: #even after filling all the cubes in the box, if the volume left is not 0, return -1
        return -1

    return minCubeCount

def boxVolume( record ):
    '''
    This function will caluclate the volume of the bigger box and also extract the
    number of smaller cubes
    '''
    volume = record[0] * record[1] * record[2]
    return volume, record[3:]

def main():
    pass

if __name__ == "__main__": main()