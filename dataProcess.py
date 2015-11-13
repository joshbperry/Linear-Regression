__author__ = 'haotian'

from sklearn.linear_model.base import LinearRegression


'''
    parse input file into a 1D array of descriptor name and a 2D array of Data
    inputFormat: (each value is separated with tab, each line is separated with \n)
    Host/Impurity(DataName)   Dsc1    Dsc2    ... DscN    Ea(Data)
    Al-Ag                     1       2       ... x       1.0267
    Al-Au                     m       n       ... y       0.5166
    ...                       ...     ...     ... ...     ...

    OutputFormat:
    splitTitle = ['Dsc1','Dsc2', ..., 'DscN', 'Ea(Data)']
    file = [[1,2,...,x,1.0267],
            [m,n,...,y,0.5166],
            ...
            ]
'''
def parseInput(fileName):
    file = open(fileName,'r').read().splitlines()
    title = file[0]
    file = file[1:]
    i = 0
    for line in file:
        line = line.split('\t')
        line = line[1:]
        for j in xrange(len(line)):
            line[j] = float(line[j])
        file[i] = line
        i = i+1
    splitTitle = title.split('\t')
    splitTitle = splitTitle[1:]
    return splitTitle, file


'''
    given a 2D array f, return another 2D array with columes not in indexList removed
'''
def writeDescripter(f, indexList):
    descripter = []
    for line in f:
        descripter.append([line[i] for i in indexList])
    return descripter


'''
    calculated the rms error of the given two lists
'''
def rmsErr(pre, act):
    size = len(pre)
    rms = 0.0
    avg = 0.0
    for i in range(0,size):
        rms += (act[i]-pre[i])**2
    rms = rms/size
    rms = rms**0.5

    return round(rms,5)
