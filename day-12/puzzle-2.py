import numpy as np
from scipy.ndimage import correlate
from skimage.measure import label, regionprops
from skimage.segmentation import find_boundaries

inputfile = open("./day-12/input.txt", "r")

"""
We read the input into a numpy array, where we replaced each letter with their Unicode code, for easier processing.
We then use `skimage.measure.label` to separate regions that have the same letter, but are not contiguous. This function just assigns a unique number to all regions.
"""
gardenMap = np.array(list(map(lambda x: list(map(ord, x)), map(str.strip, inputfile.readlines()))))
labeledMap = label(gardenMap, connectivity=1)

"""
We set the `kernel` array such that only neighbouring plots are considered, but the horizontal and vertical directions are distinguished. More on this in the next comment block.
"""
kernel = np.array([[0, 2, 0], [3, 0, 3], [0, 2, 0]])

"""
The `fencePrice` function takes a region's mask as an input and returns the price of the fencing for the region.
A region's mask is a numpy array with a shape of the region's bounding box, with each value within the region being `True`, and all others being `False`.
We convert this mask to ints (ones and zeros in this case) so that we can process it, and pad it with 0s in a width of 1 for the next step.
We obtain its boundaries using `skimage.segmentation.find_boundaries`, specifically in "subpixel" mode. The result is an array of size 2*N-1: each boundary between two cells of the original array has a cell itself in the new one, with a value of 1 if that boundary was between two different regions, and 0 otherwise. The original values of the cells are discarded. What we get is the outline of the region mask.
We correlate this with a kernel slightly different from the previous solution's: we assigned different values to vertical and horizontal neighbours. The result will be the outline, where all vertical and horizontal sides have values of 4 and 6, respectively; but much more of our interest are the corners, which have values of 5. We also have residual elements that do not correspond to any of the outline: we get rid of them by multiplying the array element-wise by the outline, like we did in the solution for the first part.
We count the number of corners, paying attention to situations where a point is actually a corner of 4 sides: we count these twice.
......
...OOO
...OOO
.OO..O
.OO..O
.OOOOO

All simple polygons have an Euler characteristic of 1. This means that the number of sides they have equal the number of corners. For polygons that have holes, the Euler characteristic will change, but the equality will hold in our case, since even if our regions have holes, their corners will not be connected to the corners of the outline.
Since the number of points in the region is finite, each hole is either a simple polygon (in which case it has the same number of sides as corners), or it has holes that are simple polygons (in which case it still has the same number of sides as corners), etc. We proved by induction that every hole has the same number of sides as corners, and therefore the region will have the same number of sides as corners.
This way, if we count the corners, and multiply the sum by the area of the region, we get the price of the fencing.
"""
def fencePrice(regionmask):
    regionmaskInt = np.pad(np.array(regionmask, dtype=int), 1)
    boundary = np.array(find_boundaries(regionmaskInt, mode="subpixel"), dtype=int)
    corners = np.multiply(boundary, correlate(boundary, kernel, mode="constant"))
    return np.sum(regionmask)*np.sum(corners[(corners == 5) | (corners == 10)])//5

"""
We use `skimage.measure.regionprops` to apply the `fencePrice` function to all regions on the labeled map.
"""
regProps = regionprops(labeledMap, cache=True, extra_properties=(fencePrice,))

"""
The result is the sum of the fence prices for all regions.
"""
print(sum([regProp["fencePrice"] for regProp in regProps]))


inputfile.close()