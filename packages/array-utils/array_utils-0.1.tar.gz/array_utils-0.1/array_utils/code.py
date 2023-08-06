class ArrayUtils:
    @staticmethod
    def amin(array, axis=None):
        if axis is None:
            return min([min(r) for r in array])
        if axis == 0:
            return [min(c) for c in zip(*array)]
        if axis == 1:
            return [min(r) for r in array]

    @staticmethod
    def amax(array, axis=None):
        if axis is None:
            return max([max(r) for r in array])
        if axis == 0:
            return [max(c) for c in zip(*array)]
        if axis == 1:
            return [max(r) for r in array]
	    
    @staticmethod
    def linspace(start, stop, num=50, endpoint=True):
  	if endpoint:
    	    return [start + x*(stop-start)/(num-1) for x in range(num)]
  	return [start + x*(stop-start)/(num-1) for x in range(num-1)]