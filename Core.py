import numpy as np

def get_quaternion(lst1,lst2,matchlist=None):
    """
    Function copied from Paul J. Besl and Neil D. McKay "Method for registration of 3-D shapes", Sensor Fusion IV: Control Paradigms and Data Structures, 586 (April 30, 1992).
    Takes 2 lists of (3 perpendicular (3x1 numpy.array) a.k.a. two sets of perpendicular axes) and finds the quaternion that best rotates from the axis in lst1 to the axis in lst 2
    returns the quaternion as a list in [w,x,y,z] form
    """
    if not matchlist:
        matchlist=range(len(lst1))
    M=np.matrix([[0,0,0],[0,0,0],[0,0,0]])

    for i,coord1 in enumerate(lst1):
        x=np.matrix(np.outer(coord1,lst2[matchlist[i]]))
        M=M+x

    N11=float(M[0][:,0]+M[1][:,1]+M[2][:,2])
    N22=float(M[0][:,0]-M[1][:,1]-M[2][:,2])
    N33=float(-M[0][:,0]+M[1][:,1]-M[2][:,2])
    N44=float(-M[0][:,0]-M[1][:,1]+M[2][:,2])
    N12=float(M[1][:,2]-M[2][:,1])
    N13=float(M[2][:,0]-M[0][:,2])
    N14=float(M[0][:,1]-M[1][:,0])
    N21=float(N12)
    N23=float(M[0][:,1]+M[1][:,0])
    N24=float(M[2][:,0]+M[0][:,2])
    N31=float(N13)
    N32=float(N23)
    N34=float(M[1][:,2]+M[2][:,1])
    N41=float(N14)
    N42=float(N24)
    N43=float(N34)

    N=np.matrix([[N11,N12,N13,N14],\
        [N21,N22,N23,N24],\
        [N31,N32,N33,N34],\
        [N41,N42,N43,N44]])


    values,vectors=np.linalg.eig(N)
    w=list(values)
    mw=max(w)
    quat= vectors[:,w.index(mw)]
    quat=np.array(quat).reshape(-1,).tolist()
    return quat

def CalculateBlockProperties(pointList):
    """
    Finds the rectangle's size, center, and rotation base on its 8 points.
    """

    #Rectangle center is the average of its 8 points
    center = np.sum(pointList,axis = 0)/8.0

    #Find the axis vectors of the rectangle, starting with a arbitrary "origin" point
    originCornerPosition = pointList[0]

    #Find the first point closest to the origin corner, label it as the "x" point
    vectorList        = pointList[1:,:] - np.repeat([originCornerPosition],7,axis = 0)
    pointDistanceList = np.linalg.norm(vectorList, axis = 1)
    originXIndex      = np.where(pointDistanceList == min(pointDistanceList))[0][0]
    originXVector     = vectorList[originXIndex]
    originXUnitVector = originXVector/np.linalg.norm(originXVector)
    originXLength     = np.linalg.norm(originXVector)

    #Find the other 3 vectors which are perpendicular to the x vector
    unitVectorList         = np.divide(vectorList,np.linalg.norm(vectorList, axis = 1)[:, np.newaxis])
    crossProductList       = np.cross(np.repeat([originXUnitVector],7,axis = 0),unitVectorList)
    perpendicularIndexList = np.where(np.linalg.norm(crossProductList, axis = 1)>.999999)[0]#.999999 is for roundoff errors
    if len(perpendicularIndexList) != 3:
        raise StandardError('Found ' + str(len(perpendicularIndexList)) + ' instead of 3 perpendicular vectors, probably due to roundoff error in python or the .obj file.')

    #The longest vector of those three vectors is not the y or z vector
    possibleVectorList    = vectorList[perpendicularIndexList]
    possibleVectorLength  = np.linalg.norm(possibleVectorList, axis = 1)
    possibleYZVectorIndex = np.where(possibleVectorLength != max(possibleVectorLength))[0]
    possibleYZVectorIndex = perpendicularIndexList[possibleYZVectorIndex]

    #Determine which of these vectors is the y and z vector
    if np.dot(np.cross(originXUnitVector,unitVectorList[possibleYZVectorIndex[0]]),unitVectorList[possibleYZVectorIndex[1]])>0:
        originYIndex      = possibleYZVectorIndex[0]
        originZIndex      = possibleYZVectorIndex[1]
    else:
        originYIndex      = possibleYZVectorIndex[1]
        originZIndex      = possibleYZVectorIndex[0]

    originYVector     = vectorList[originYIndex]
    originYUnitVector = unitVectorList[originYIndex]
    originYLength     = np.linalg.norm(originYVector)
    originZVector     = vectorList[originZIndex]
    originZUnitVector = unitVectorList[originZIndex]
    originZLength     = np.linalg.norm(originZVector)

    rotation = get_quaternion([np.array([1,0,0]),np.array([0,1,0]),np.array([0,0,1])],[originXUnitVector, originYUnitVector, originZUnitVector])

    size = np.array([originXLength,originYLength,originZLength])

    return size, center, rotation