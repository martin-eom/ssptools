import sys, json
from numpy import array

exampleJSON = " {\n\
  \"type\": \"reciprocal\",\n\
  \"straights\": [\n\
    {\n\
     \"endpoint\": [0, 0, 0],\n\
     \"npoints\": 1,\n\
     \"name\": \"gamma\"\n\
    },\n\
    {\n\
     \"endpoint\": [0.5, 0, 0],\n\
     \"npoint\": 40,\n\
     \"name\": \"M\"\n\
    }\n\
   ]\n\
 }"

def read(filename):
    with open(filename, 'r') as kfile:
        data = json.load(kfile)
        try:
            pointList   = [straight["endpoint"] for straight in data["straights"]]
            numList     = [straight["npoints"] for straight in data["straights"]]
            nameList    = [straight["name"] for straight in data["straights"]]
            return pointList, numList, nameList
        except:
            print("Example of json file:\n%s"%exampleJSON)
            raise
        

def makeCoordList(pointList, numList, nameList):
    try:
        if not (len(pointList)==len(numList) and len(numList)==len(nameList)):
            raise IndexError("Supplied lists must have the same lengths.")
    except IndexError as error:
        print(repr(error))
    if len(pointList) == 0:
        raise IndexError("Supplied lists must not be empty.")
    if numList[0] == 0:
        raise Exception("Number of kpoints in a line must be given by the end-point, not the beginning. Therefore the first point in the list must have num = 1. This script fundamentally differs from other existing ones in that regard.")
    coordList = [array(pointList[0])]
    for i in range(1, len(pointList)):
        prev, current = array(pointList[i-1]), array(pointList[i])
        diffStep = (current - prev) / numList[i]
        for j in range(1, numList[i] + 1):
            coordList.append(prev + diffStep * j)
    return coordList
