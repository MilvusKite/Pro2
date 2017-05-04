
# Additional functions used in "ActualPolarPlotter"
import numpy as np


def meiScale(InputValues, axisMin, axisMax, plotRange): # Simple shift and scale function
   if not np.issubdtype(InputValues.dtype, float):
       raise Exception('Input WrOnGG!')
   return np.multiply(np.divide(np.subtract(InputValues,axisMin),axisMax-axisMin),plotRange)

def getX(InputValvs,numberOfAxises):
    if len(InputValvs) != numberOfAxises:
        raise ValueError('InputS WrOnGG!')
    rotationVec = np.array([], dtype='float64')
    for K in range(0,numberOfAxises):
        rotationVec = np.append(rotationVec,np.cos(np.pi/2 + K*2*np.pi/numberOfAxises))
    outi = InputValvs * rotationVec
    return(outi)

def getY(InputValvs,numberOfAxises):
    if len(InputValvs) != numberOfAxises:
        raise ValueError('InputS WrOnGG!')
    rotationVec = np.array([], dtype='float64')
    for K in range(0,numberOfAxises):
        rotationVec = np.append(rotationVec,np.sin(np.pi/2 + K*2*np.pi/numberOfAxises))
    outi = InputValvs * rotationVec
    return(outi)

def makePolarBG(PlotRange,NumOfCircles,NumberOfAxises,BackGroundColor,BackGroundWidth,ZeroWidth,ZeroPosition):
    def makeSingleCircle(plotPos,COLOR,WIDTH):
        ToRtrn =  {
            'type': 'circle',
            'xref': 'x',
            'yref': 'y',
            'x0': -plotPos,
            'y0': -plotPos,
            'x1': plotPos,
            'y1': plotPos,
            'line': {
                'color': COLOR,
                'width': WIDTH,
            },
        }
        return(ToRtrn)
    def makePolarAxis(PlotRange, N, NumberOfAxises, COLOR, WIDTH):
        ToRtrn = {
            'type': 'line',
            'x0': 0,
            'y0': 0,
            'x1': PlotRange*np.cos(np.pi/2 + N*2*np.pi/NumberOfAxises),
            'y1': PlotRange*np.sin(np.pi/2 + N*2*np.pi/NumberOfAxises),
            'line': {
                'color': COLOR,
                'width': WIDTH,
                # 'dash': 'dot',
            },
        }
        return(ToRtrn)
    bgShapes = []
    posStep = float(PlotRange)/float(NumOfCircles)
    for K in range(1,NumOfCircles+1):
        bgShapes.append(makeSingleCircle(posStep*K,BackGroundColor,BackGroundWidth))
    bgShapes.append(makeSingleCircle(ZeroPosition,BackGroundColor,ZeroWidth)) # Adding zero circle
    for K in range(1,NumberOfAxises+1):
        bgShapes.append(makePolarAxis(PlotRange, K, NumberOfAxises,BackGroundColor,BackGroundWidth))
    return(bgShapes)

def makeCloud(ValuesScaledX,ValuesScaledY,COLOR):

    PATH = 'M ' + np.array_str(ValuesScaledX[0]) + ',' + np.array_str(ValuesScaledY[0])
    for K in range(1,len(ValuesScaledX)):
        PATH = PATH + ' L ' + np.array_str(ValuesScaledX[K]) + ',' + np.array_str(ValuesScaledY[K])
    PATH = PATH + ' L ' + np.array_str(ValuesScaledX[0]) + ',' + np.array_str(ValuesScaledY[0])
    for K in range(len(ValuesScaledX)):
        PATH = PATH + ' L ' + np.array_str(ValuesScaledX[K]) + ',' + np.array_str(ValuesScaledY[K])
    PATH = PATH + ' L ' + np.array_str(ValuesScaledX[0]) + ',' + np.array_str(ValuesScaledY[0])
    PATH = PATH + 'Z'
    ToRtrn = [{
            'type': 'path',
            'path': PATH,
            'fillcolor': COLOR,
            'line': {
                'color': COLOR,
                'width': 0,
            },
        }]
    return(ToRtrn)