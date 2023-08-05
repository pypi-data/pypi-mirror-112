import numpy as np


def updatedict(updatee, updater, mode="intersect"):
    """
    Updates the values from the updater dictionary --> updatee dictionary

    If mode is "intersect", updates only occur on the keys which exist between both dictionaries.

    If mode is "union", updates missing key-value pairs from updater --> updatee

    """
    if mode == "intersect":
        sharedkeys = [
            dictkey for dictkey in updater.keys() if dictkey in updatee.keys()
        ]
        for key in sharedkeys:
            updatee[key] = updater[key]

    elif mode == "union":
        missingkeys = [
            dictkey for dictkey in updater.keys() if dictkey not in updatee.keys()
        ]
        for key in missingkeys:
            updatee[key] = updater[key]
    else:
        raise Exception("Mode '" + str(mode) + "' not supported.")

    return updatee


def maxshape(*imgs, buff=0, frame="original"):
    """
    Returns the maximum physical shape of a set of images

    Uses either "original" or "current" frame.

    """
    myshape = np.zeros(3, dtype=np.float64)
    for img in imgs:
        if frame == "current":
            physshape = (np.array(img.shape) + buff) * img.affine.scale()
        elif frame == "original":
            physshape = (np.array(img.shape) + buff) * img.affine.decomposition("RS")[
                -1
            ].scale()
        else:
            raise Exception()
        myshape[physshape > myshape] = physshape[physshape > myshape]
    return myshape


def multidot(*arrays):
    result = arrays[0]
    for array in arrays[1:]:
        result = np.dot(result, array)
    return result
