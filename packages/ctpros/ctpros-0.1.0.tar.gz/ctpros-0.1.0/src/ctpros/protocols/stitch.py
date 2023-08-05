import numpy as np
import tkinter.filedialog
import copy, sys, glob, os
import tqdm
import ctpros as ct
import itertools


def reorient(*imgs, tfm="average"):
    """
    Re-orients transformations to set all images to be (1) relative to the
    frame of the unmatched transformation matrix OR (2) relative to an
    average orientation of all of the matches transformations.

    Parameters:
        ctpros.ImgTemplate[] imgs = list of images to be considered for stitching
        ctpros.AffineTensor tfm = transform to re-orient to, defaults to the average orientation

    """
    if tfm is None:
        return ct.AffineTensor(3)
    elif type(tfm) is str and tfm == "average":  # calculate tfm as average transform
        prod = ct.AffineTensor(3)
        affines = [img.affine.copy() for img in imgs]
        orientations = [
            ct.AffineTensor(affine.pdim).align(affine) for affine in affines
        ]
        [prod.affine(orientation) for orientation in orientations]
        avg_rot = prod.rotate() / len(imgs)
        avg_trans = prod.translate() / len(imgs)
        tfm = ct.AffineTensor(3).rotate(*avg_rot).translate(*avg_trans)

    # calculates difference from the image transforms to the reference transform
    affine_diff = tfm.copy().inv()

    return affine_diff


def define_voi(imgs, tfm=None):
    """
    Identifies the volume of interest to be sampled.

    - Calculates the minimum and maximum physical coordinates of an image
    - Sets the minimum value as the sampling origin and difference as the size to be sampled
      at a rate of the affine scaling of the first image in the list

    """
    if tfm is not None:
        modified_tfms = [img.affine.copy().affine(tfm) for img in imgs]
    else:
        modified_tfms = [img.affine for img in imgs]
    shapes = [img._fileshape() for img in imgs]

    for i, (shape, modified_tfm) in enumerate(zip(shapes, modified_tfms)):
        index_bounds = np.array(
            [
                [0, 0, 0],
                [shape[0] - 1, 0, 0],
                [0, shape[1] - 1, 0],
                [0, 0, shape[2] - 1],
                [shape[0] - 1, shape[1] - 1, 0],
                [shape[0] - 1, 0, shape[2] - 1],
                [0, shape[1] - 1, shape[2] - 1],
                [shape[0] - 1, shape[1] - 1, shape[2] - 1],
            ]
        ).T
        physical_bounds = modified_tfm.dot(index_bounds)

        if not i:  # on first iteration assign
            minpos = physical_bounds.min(1)
            maxpos = physical_bounds.max(1)
        else:  # otherwise update
            minpos[:] = np.minimum(minpos, physical_bounds.min(1))
            maxpos[:] = np.maximum(maxpos, physical_bounds.max(1))

    pos = minpos
    elsize = imgs[0].affine.scale()
    shape = (maxpos - minpos + 1) // elsize + ((maxpos - minpos + 1) % elsize).astype(
        bool
    )
    voi = ct.VOI(pos=pos, shape=shape, elsize=elsize)

    return voi


def resampler(imgs, affine_diff, voi, *, precision="single"):
    """
    Resamples the images within their physical bounds with a given image resolution.

    """
    # loaded_imgs = [img for img in imgs if img.nbytes]  # to be re-loaded after stitching
    # [img.clear() for img in imgs[1:]]

    stitched_img = type(imgs[0])(tuple(voi.shape), dtype=precision)
    stitched_img.__array_finalize__(imgs[0])
    stitched_img[:] = 0

    coeff_img = type(imgs[0])(tuple(voi.shape), dtype=np.half)
    coeff_img[:] = 0

    for img in imgs:
        try:
            img.load()
            loaded = True
        except:
            loaded = False
        np.add(
            img.transform.affine(affine_diff, voi, inplace=False),
            stitched_img,
            out=stitched_img,
        )
        if loaded:
            img.clear()
            shape = img._fileshape()
        else:
            shape = img.shape
        ones = ct.NDArray(shape, dtype="single", verbosity=False)
        ones.affine.affine(img.affine)
        ones[:] = 1
        np.add(
            ones.transform.affine(affine_diff, voi, inplace=False),
            coeff_img,
            out=coeff_img,
        )
        ones.clear()

    stitched_img[coeff_img > 1] /= coeff_img[coeff_img > 1]
    return stitched_img


def stitcher(*imgs, tfm="average", precision="single"):
    """
    Stitches images together based on their affine relationships.

    Parameters:
        ctpros.ImgTemplate[] imgs = list of images to be considered for stitching
        tfm ctpros.AffineTensor tfm = transform to be resampled onto

    """
    affine_diff = reorient(*imgs, tfm=tfm)
    voi = define_voi(imgs, affine_diff)
    stitched_img = resampler(imgs, affine_diff, voi, precision=precision)
    return stitched_img


def align(*imgs, reference=None):
    dirs = {}
    for img in imgs:
        if img.fileloc not in dirs:
            dirs[img.fileloc] = []
        dirs[img.fileloc].append(img)

    for dir, imgs in dirs.items():
        tfms = [ct.AffineTensor(filename) for filename in glob.glob(f"{dir}*.tfm")]
        imgnames = [os.path.splitext(img.filename)[0] for img in imgs]
        tfmnames = [os.path.splitext(tfm.filename)[0] for tfm in tfms]
        array = np.array(
            [[tfmname.find(imgname) for imgname in imgnames] for tfmname in tfmnames],
            float,
        )
        array[array == -1] = np.nan
        isrelevant = np.logical_not(np.all(np.isnan(array), 1))
        tfms = [tfm for tfm, flag in zip(tfms, isrelevant) if flag]
        array = array[isrelevant]
        array[np.arange(array.shape[0]), np.nanargmin(array, 1)] = 1
        array[np.arange(array.shape[0]), np.nanargmax(array, 1)] = 2

        for i, row in enumerate(array):
            minind = np.nanargmin(row)
            maxind = np.nanargmax(row)
            if minind > maxind:
                row[[minind, maxind]] = row[[maxind, minind]]
                tfms[i].inv()
        for j, col in enumerate(array.transpose()[:-1]):
            start = np.nonzero(col == 1)[0][0]
            end = np.nonzero(col == 2)[0]
            for ind in end:
                col[ind] = np.nan
                array[ind, np.nonzero(array[start] == 2)[0][0]] = 2
                tfms[ind].affine(tfms[start])

        if reference is not None:
            ref_ind = imgs.index(reference)
        else:
            ref_ind = -1
        ref_tfm = imgs[ref_ind].affine.copy()

        for img in imgs:
            img.reset_affine()
        for img, tfm in zip(imgs[:-1], tfms):
            img.affine.affine(tfm)

        ref_tfm_diff = (
            ct.AffineTensor(ref_tfm.pdim)
            .affine(imgs[ref_ind].affine.copy().inv())
            .affine(ref_tfm)
        )
        for img in imgs:
            img.affine.affine(ref_tfm_diff)


def main(*argv):  # pragma: no cover
    imgfiles = argv
    imgs = [ct.ImgTemplate(imgfile) for imgfile in imgfiles]

    align(imgs)

    stitcher(imgs)


if __name__ == "__main__":  # pragma: no cover
    main(*sys.argv[1:])
