import numpy as np
from scipy.ndimage import correlate
from skimage.measure import label, regionprops

inputfile = open("./day-12/input.txt", "r")

"""
We read the input into a numpy array, where we replaced each letter with their Unicode code, for easier processing.
We then use `skimage.measure.label` to separate regions that have the same letter, but are not contiguous. This function just assigns a unique number to all regions.
"""
gardenMap = np.array(list(map(lambda x: list(map(ord, x)), map(str.strip, inputfile.readlines()))))
labeledMap = label(gardenMap, connectivity=1)

"""
We set the `kernel` array such that only neighbouring plots are considered. More on this in the next comment block.
"""
kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])

"""
The `fencePrice` function takes a region's mask as an input and returns the price of the fencing for the region.
A region's mask is a numpy array with a shape of the region's bounding box, with each value within the region being `True`, and all others being `False`.
We convert this mask to ints (ones and zeros in this case) so that we can process it.
The price of the fencing for a region is calculated by multiplying its area by its perimeter.
    The region's area is easily calculated by summing all the values within the region mask: `np.sum(regionmask)`.
    The region's perimeter is a bit more tricky:
        1. We know that all plots have 4 sides, so the overall number of sides for all the plots is `4*np.sum(regionmask)`.
        2. We use `scipy.ndimage.correlate` to calculate the number of sides that touch plots of the same region.
           This function iterates through all the elements of its first parameter and multiplies its neighbourhood element-wise by the second parameter (the so-called kernel). We set the mode to "constant" to pad the first parameter with 0s.
           For instance for the following region and kernel:
               01000    
               11011    010
               11101    101
               01011    010
               01110
           For element (1,1), the elementwise multiplication:
                010     010     010
                110  *  101  =  100  --> sum: 3
                111     010     010
           Therefore the correlation matrix will have 3 in position (1,1).
           In our application, this calculates the number of plots of this region adjacent to each location. Since this is calculated for locations outside of the region, we multiply the correlation matrix element-wise by the region mask, resulting in a matrix that contains for all the plots of this region the number of plots of the region it is adjacent to, i.e. the number of sides that touch plots of the region. By summing this matrix, we get the number of all the sides that touch plots of the same region (with each side counted twice, once for each plot its a side of).
        3. We subtract the previous number from the overall number of sides to arrive at the overall number of sides _not_ adjacent to plots of the same region, i.e. the region's perimeter.
"""
def fencePrice(regionmask):
    regionmaskInt = np.array(regionmask, dtype=int)
    return np.sum(regionmask)*(4*np.sum(regionmask) - np.sum(np.multiply(regionmaskInt, correlate(regionmaskInt, kernel, mode="constant"))))

"""
We use `skimage.measure.regionprops` to apply the `fencePrice` function to all regions on the labeled map.
"""
regProps = regionprops(labeledMap, cache=True, extra_properties=(fencePrice,))

"""
The result is the sum of the fence prices for all regions.
"""
print(sum([regProp["fencePrice"] for regProp in regProps]))


inputfile.close()