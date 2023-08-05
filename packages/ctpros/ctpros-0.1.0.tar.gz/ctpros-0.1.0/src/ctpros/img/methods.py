"""ctpros image methods
Defines NumPy/SciPy/ITK interfacing methods inherited into the image classes.
These are broken up into Method Groups which act as containers
for themed actions. IO and other methods are defined in the classes themselves.

Method group details can be accessed via help(ctpros.NDArray.*methodgroup*).
See help(ctpros.NDArray) for more details about available method groups.

"""
import copy
import numpy as np
import scipy as sp
import scipy.ndimage
import skimage as sk
import skimage.filters
import skimage.feature
import itk
from mayavi import mlab

from .utils import decorators as dec
from .utils.script import multidot


class MethodGroup:
    def __init__(self, parent):
        self.parent = parent


@dec.for_all_methods(dec.inplace, dec.selfisparent)
class Classification(MethodGroup):
    """
    Defines methods for classification in images. Methods include standard
    multiple global thresholding to local thresholding techniques.

    """

    def threshold(self, val, *vals):
        """
        Performs global thresholding for a set of values. Practically,
        values should be monotonically increasing.

        Support for up to 255 threshold values.

        Values below the first threshold are 0. Values above
        the first value are set to 1, above the second value are
        set to 2, and so on.

        Parameters:
            *vals = threshold values

        Ex:
            instance.classify.threshold(100,1000)
            -         instance < 100   --> 0
            - 100  <= instance < 1000  --> 1
            - 1000 <= instance         --> 2
            - instance.dtype --> np.uint8
        """
        mask = np.zeros_like(self, np.uint8)
        vals = [val, *vals]
        for i, val in enumerate(vals):
            mask[self >= val] = i + 1

        return mask

    def otsu_global(self, n=1, nbins=256):
        """
        Performs multi-otsu thresholding, defaults to defining a single threshold.

        Parameters
            n : number of threshold values
            nbins : number of bins for calculating thresholds

        """
        otsu_vals = skimage.filters.threshold_multiotsu(self, n + 1, nbins)
        if self.verbosity >= 2:  # pragma: no cover
            print(f"Otsu Values:{otsu_vals}")
        mask = self.classify.threshold(*otsu_vals, inplace=False)
        return mask, otsu_vals

    def canny_edge(self, sigma=1, low_threshold=None, high_threshold=None):
        """
        Applies ITK's Canny Edge detection algorithm.

        Parameters:
            sigma = smoothing magnitude on image before gradient estimation
            low_threshold, high_threshold = gradient cutoff values for weak and strong edges

        Returns:
            type(self)(shape=self.shape,dtype="bool")
        """

        if low_threshold is None and high_threshold is None:
            gradient = self.transform.gradient(sigma=sigma, inplace=False)
            gradient.verbosity = 0
            threshed_gradient, (
                _,
                low_threshold,
                high_threshold,
            ) = gradient.classify.otsu_global(3, inplace=False)
            gradient.clear()
            threshed_gradient.clear()

        itkimg, itkimgtype, _ = _data2itkimg(self.astype("single"))

        itk_canny = itk.CannyEdgeDetectionImageFilter[itkimgtype, itkimgtype].New()
        itk_canny.SetInput(itkimg)
        itk_canny.SetVariance(sigma)
        itk_canny.SetLowerThreshold(float(low_threshold))
        itk_canny.SetUpperThreshold(float(high_threshold))

        itk_result = itk_canny.GetOutput()

        array = itk.array_from_image(itk_result).astype("uint8")
        return type(self)(array, self)

    def inv(self):
        return np.logical_not(self).astype(np.uint8)


@dec.for_all_methods(dec.inplace, dec.selfisparent)
class Filters(MethodGroup):
    """
    Defines methods for filtering in images. Methods include gaussian
    smoothing to inversion techniques.

    """

    def gauss(self, sigma=1, cutoff=3, precision=None):
        """
        Returns gaussian-filtered image. Gaussian filter is truncated at
        ceil(sigma*cutoff)
        """
        precision = self.dtype
        array = sp.ndimage.gaussian_filter(
            self, sigma, output=precision, mode="nearest", truncate=cutoff
        )
        return type(self)(array, self)

    def inv(self, alpha, filter, *args, **kwargs):
        """
        Performs an estimated inverse operation to a filter with
        magnitude amplification alpha.

        Besides filter and alpha, input *args and **kwargs as fits
        for the to-be-inversed filter.

        Ex:
            img = NDArray(...)
            img.filter.inv(img.filter.gauss,alpha,sigma)

        """
        filtered = filter(*args, inplace=False, **kwargs)
        inv = self + alpha * (self - filtered)
        return inv

    def mean(
        self,
        size=3,
        precision=np.float64,
    ):
        """
        Returns a mean-filtered image. Size defines the pixel size of
        the mean window taken.

        """
        array = sp.ndimage.uniform_filter(self, size, output=precision, mode="nearest")
        return type(self)(array, self)


@dec.for_all_methods(dec.selfisparent)
class Generic(MethodGroup):
    """
    Currently empty.


    """

    def tra(self, pos=None, *, voi=None, interp=0):
        inputs = self._tra_protocol(pos=pos, voi=voi)
        if inputs is None:
            return None
        else:
            return self.transform.affine(
                *inputs, interp=interp, inplace=False
            ).squeeze()

    def cor(self, pos=None, *, voi=None, interp=0):
        inputs = self._cor_protocol(pos=pos, voi=voi)
        if inputs is None:
            return None
        else:
            return self.transform.affine(
                *inputs, interp=interp, inplace=False
            ).squeeze()

    def sag(self, pos=None, *, voi=None, interp=0):
        inputs = self._sag_protocol(pos=pos, voi=voi)
        if inputs is None:
            return None
        else:
            return self.transform.affine(
                *inputs, interp=interp, inplace=False
            ).squeeze()

    def render_contour(self, *contours, title="Contour Rendering", show=True):
        mlab.figure(bgcolor=(0, 0, 0))
        mlab.contour3d(self, contours=list(contours), color=(1, 1, 1))
        mlab.title(title)
        if show:
            mlab.show()

    def render_cubes(
        self,
        labels=None,
        colors=None,
        opacities=None,
        sizes=None,
        accent_outline=True,
        title="Cube Rendering",
        show=True,
    ):
        """
        This function generates a voxel-based volume rendering of the
        current data of the image volume instance.

        """
        if labels is None:
            labels = np.array([1])
        if colors is None:
            colors = np.array([[1.0, 1.0, 1.0]])
        if opacities is None:
            opacities = np.ones_like(labels, dtype=np.float)
        if sizes is None:
            sizes = np.ones_like(labels, dtype=np.float)

        mlab.figure(bgcolor=(0, 0, 0))
        if accent_outline:
            xyz = np.nonzero(self)
            outline = mlab.points3d(
                *xyz, mode="cube", scale_factor=1, color=(0, 0, 0), opacity=0.25
            )
            outline.glyph.scale_mode = "scale_by_vector"
            outline.mlab_source.dataset.point_data.scalars = np.ones(
                shape=(np.sum(self != 0),), dtype=np.uint8
            )
            sizes = np.array([size * 0.9 for size in sizes])

        colors = colors.astype(np.float)
        opacities = opacities.astype(np.float)
        sizes = sizes.astype(np.float)

        [s0, s1, s2] = self.shape
        point1 = (
            np.array(
                [
                    [0, 0, 0],
                    [0, s1, 0],
                    [0, 0, s2],
                    [0, s1, s2],
                    [0, 0, 0],
                    [s0, 0, 0],
                    [0, 0, s2],
                    [s0, 0, s2],
                    [0, 0, 0],
                    [s0, 0, 0],
                    [0, s1, 0],
                    [s0, s1, 0],
                ]
            )
            - 0.5
        )
        point2 = (
            np.array(
                [
                    [s0, 0, 0],
                    [s0, s1, 0],
                    [s0, 0, s2],
                    [s0, s1, s2],
                    [0, s1, 0],
                    [s0, s1, 0],
                    [0, s1, s2],
                    [s0, s1, s2],
                    [0, 0, s2],
                    [s0, 0, s2],
                    [0, s1, s2],
                    [s0, s1, s2],
                ]
            )
            - 0.5
        )

        for i in range(point1.shape[0]):
            mlab.plot3d(
                [point1[i][0], point2[i][0]],
                [point1[i][1], point2[i][1]],
                [point1[i][2], point2[i][2]],
                color=(1, 1, 1),
                tube_radius=None,
            )

        for label, size, color, opacity in zip(labels, sizes, colors, opacities):
            xyz = np.nonzero(self == label)
            if len(xyz) == 0:
                continue
            voxels = mlab.points3d(
                *xyz,
                mode="cube",
                scale_factor=size,
                color=tuple(color),
                opacity=opacity,
            )
            voxels.glyph.scale_mode = "scale_by_vector"
            voxels.mlab_source.dataset.point_data.scalars = np.ones(
                shape=(np.sum(self == label),), dtype=np.uint8
            )

        # mlab.view(azimuth=150, elevation=210, roll=180)
        mlab.view(azimuth=195, elevation=105, roll=180)
        mlab.title(title)
        if show:
            mlab.show()

        return None

    def render_scalar(self, vmin=None, vmax=None, title="Scalar Field", show=True):
        """
        Opacity is defined linearly between vmin and vmax values of the scalar field.
        vmin = raw value threshold for complete transparence
        vmax = raw value threshold for complete opacity
        """
        if vmax is None:
            if type(vmin) == int:
                vmax = vmin + 1
            elif type(vmin) == float:
                vmax = vmin + 1e-6
            else:
                vmax = self.max()

        if vmin is None:
            vmin = self.min()
        crusts = self.generic._cut_crusts()
        mlab.figure(bgcolor=(0, 0, 0))
        mlab.pipeline.volume(
            mlab.pipeline.scalar_field(self), vmin=vmin, vmax=vmax, color=(1, 1, 1)
        )
        self.generic._put_crusts(*crusts)
        mlab.title(title)
        if show:
            mlab.show()

    def render_triangles(
        self, labels=None, colors=None, title="Triangle Rendering", show=True
    ):
        """
        Performs volume rendering of thresholded image.
        Ex:
        labelvol = np.array, usually of specified labels
            (i.e. composed of 0's, 1's, 2's, 3's)
        labels = np.array, composed of label values to be visualized
        colors = np.array, nx3 defining color of corresponding label


        """
        if labels is None:
            labels = np.array([1])
        if colors is None:
            colors = np.array([[1.0, 1.0, 1.0]])

        colors = colors.astype(np.float)
        crusts = self.generic._cut_crusts()
        mask = self.astype(np.bool_)

        verts, faces = sk.measure.marching_cubes(mask, 0.5)[0:2]
        values = sp.interpolate.interpn(  # average of 4 labels and 4 zeros
            (
                np.arange(self.shape[0]),
                np.arange(self.shape[1]),
                np.arange(self.shape[2]),
            ),
            self,
            verts,
        )
        values *= 2
        self.generic._put_crusts(*crusts)

        facelabels = values[faces[:, 0]]
        uniquefacelabels = np.unique(facelabels)
        for facelabel in uniquefacelabels:
            if facelabel not in labels:
                facelabels[facelabels == facelabel] = 0

        [s0, s1, s2] = self.shape
        point1 = (
            np.array(
                [
                    [0, 0, 0],
                    [0, s1, 0],
                    [0, 0, s2],
                    [0, s1, s2],
                    [0, 0, 0],
                    [s0, 0, 0],
                    [0, 0, s2],
                    [s0, 0, s2],
                    [0, 0, 0],
                    [s0, 0, 0],
                    [0, s1, 0],
                    [s0, s1, 0],
                ]
            )
            - 0.5
        )
        point2 = (
            np.array(
                [
                    [s0, 0, 0],
                    [s0, s1, 0],
                    [s0, 0, s2],
                    [s0, s1, s2],
                    [0, s1, 0],
                    [s0, s1, 0],
                    [0, s1, s2],
                    [s0, s1, s2],
                    [0, 0, s2],
                    [s0, 0, s2],
                    [0, s1, s2],
                    [s0, s1, s2],
                ]
            )
            - 0.5
        )

        mlab.figure(bgcolor=(0, 0, 0))
        for i in range(point1.shape[0]):
            mlab.plot3d(
                [point1[i][0], point2[i][0]],
                [point1[i][1], point2[i][1]],
                [point1[i][2], point2[i][2]],
                color=(1, 1, 1),
                tube_radius=None,
            )

        for i, label in enumerate(labels):
            mlab.triangular_mesh(
                verts[:, 0],
                verts[:, 1],
                verts[:, 2],
                faces[facelabels == label],
                color=tuple(colors[i]),
            )
        mlab.view(azimuth=150, elevation=210, roll=180)
        mlab.title(title)
        if show:
            mlab.show()

    def _cut_crusts(self):
        front = np.array(self[0, :, :])
        back = np.array(self[-1, :, :])
        left = np.array(self[:, 0, :])
        right = np.array(self[:, -1, :])
        top = np.array(self[:, :, 0])
        bottom = np.array(self[:, :, -1])
        self[0, :, :] = 0
        self[-1, :, :] = 0
        self[:, 0, :] = 0
        self[:, -1, :] = 0
        self[:, :, 0] = 0
        self[:, :, -1] = 0
        return front, back, left, right, top, bottom

    def _put_crusts(self, front, back, left, right, top, bottom):
        self[0, :, :] = front
        self[-1, :, :] = back
        self[:, 0, :] = left
        self[:, -1, :] = right
        self[:, :, 0] = top
        self[:, :, -1] = bottom


@dec.for_all_methods(dec.selfisparent)
class Numeric(MethodGroup):
    """
    Currently empty.

    """

    def second_moment(self):
        """
        Calculates the second moment of area tensor of an array interpreted as a boolean mask.

        Returns:
            Isma = [[Ixx,-Ixy],[-Ixy,Iyy]]

        Notes:
            - Voxels are considered as discretized points with an area weight of 1, not squares of area 1
            - The x- and y- axis are considered to be in the vertical and horizontal directions, respectively
            - Measurements are taken in the original coordinate system and scaled, so there is no resampling



        Quick Reference:
        https://mathworld.wolfram.com/AreaMomentofInertia.html

        """
        if np.any(self.affine.rotate()[1:]):
            raise Exception(
                "No implementation of second moment at rotations not about the transaxial (1st) axis."
            )
        # get center of mass of each slice
        labels = np.arange(1, 1 + self.shape[0]).reshape([-1, 1, 1])
        indexedimg = self.astype(bool) * labels
        com = np.array(
            sp.ndimage.measurements.center_of_mass(
                self, labels=indexedimg, index=labels.ravel()
            )
        )

        # calculate x**2, y**2, x*y at each point
        grid = np.ogrid[0 : self.shape[0], 0 : self.shape[1], 0 : self.shape[2]]
        grid = [axis.astype(np.uint64) for axis in grid]
        xx = grid[1] ** 2
        yy = grid[2] ** 2
        xy = grid[1] * grid[2]

        # Calculate Ixx, Iyy, and Ixy for each slice

        Ixx = (
            np.sum(yy * self.astype(bool), axis=(1, 2))
            - np.sum(self.astype(bool), axis=(1, 2)) * com[:, 2] ** 2
        )
        Iyy = (
            np.sum(xx * self.astype(bool), axis=(1, 2))
            - np.sum(self.astype(bool), axis=(1, 2)) * com[:, 1] ** 2
        )
        Ixy = (
            np.sum(xy * self.astype(bool), axis=(1, 2))
            - np.sum(self.astype(bool), axis=(1, 2)) * com[:, 1] * com[:, 2]
        )

        # average I components, then scale
        Ixx, Ixy, Iyy = [float(np.nanmean(array)) for array in [Ixx, Ixy, Iyy]]
        Isma = np.array([[Ixx, -Ixy], [-Ixy, Iyy]]) * self.affine.scale()[1:] ** 4
        from .classes import AffineTensor

        R = AffineTensor(2).rotate(self.affine.rotate()[0])[:-1, :-1]
        rotated_Isma = np.dot(R.copy().inv(), np.dot(Isma, R))
        return rotated_Isma


@dec.for_all_methods(dec.selfisparent)
class Registration(MethodGroup):
    """
    Defines methods for registration in images. Methods mostly utilize ITK's
    registration algorithms.

    """

    def true3D(self, reference, voi=True, **kwargs):
        """
        Performs image registration of self to reference using self's VOI if `voi=True`. If voi is False (not recommended),
        the whole image volume is used for image registration

        Registration is performed up to the reference image resolution.

        Target = moving volume (self)
        Reference = fixed volume to be overlapped
                Tstar
            Ttar ----> Tref

        Keyword Arguments:
        pyrlevels = (int) pyramid structure levels (sets of undersampled registrations)
        pyrsigmas = (list(int)) smoothing factors for each pyramid level
        pyrfactors = (list(int)) downsampling factors for each pyramid level
        minstep = (float) size of gradient step to define convergence of registration
        niterations = (int) number of iteratiosn PER pyramid level

        """
        from .classes import NDArray, AffineTensor, VOI

        if self.verbosity > 1:
            print("Image Registration: Initializing ...")
        defaults = [
            ("pyrlevels", 1),
            ("pyrsigmas", [1]),
            ("pyrfactors", [1]),
            ("minstep", 1e-5),
            ("niterations", 300),
        ]
        for field, value in defaults:
            if field not in kwargs:
                kwargs[field] = value
        if voi is False:
            voi = VOI(
                pos=[0, 0, 0], shape=reference.shape, elsize=reference.affine.scale()
            )
        else:
            voi = copy.deepcopy(self.voi)
        resolution = np.max(
            np.array([reference.affine.scale(), self.affine.scale()]),
            axis=0,
        )
        voi.shape = (
            np.minimum(
                voi.shape * voi.elsize, reference.shape * reference.affine.scale()
            )
            / resolution
        )
        voi.elsize = resolution

        if "complex" in str(reference.dtype):
            reference = np.absolute(reference)
        referencevoi = reference.view(NDArray).transform.affine(
            voi=voi,
            interp=1,
            dtype=np.single,
            inplace=False,
        )
        if "complex" in str(self.dtype):
            target = np.absolute(self)
        else:
            target = self
        targetvoi = target.view(NDArray).transform.affine(
            voi=voi,
            interp=1,
            dtype=np.single,
            inplace=False,
        )

        rimg, rimgtype, _ = _data2itkimg(targetvoi)
        timg, timgtype, _ = _data2itkimg(referencevoi)

        type_transform = itk.Euler3DTransform[itk.D]
        operator_transform = type_transform.New()
        operator_transform.SetIdentity()
        identity = type_transform.New()
        identity.SetIdentity()

        type_metric = itk.MeanSquaresImageToImageMetricv4[rimgtype, timgtype]
        operator_metric = type_metric.New()

        type_optimizer = itk.RegularStepGradientDescentOptimizerv4
        operator_optimizer = type_optimizer.New(
            LearningRate=1,
            MinimumStepLength=kwargs["minstep"],
            RelaxationFactor=0.5,
            NumberOfIterations=kwargs["niterations"],
        )

        type_reg = itk.ImageRegistrationMethodv4[rimgtype, timgtype]
        operator_reg = type_reg.New(
            FixedImage=rimg,
            MovingImage=timg,
            Metric=operator_metric,
            Optimizer=operator_optimizer,
            InitialTransform=operator_transform,  # identity
        )
        operator_reg.SetMovingInitialTransform(identity)
        operator_reg.SetFixedInitialTransform(identity)
        operator_reg.SetNumberOfLevels(kwargs["pyrlevels"])
        operator_reg.SetSmoothingSigmasPerLevel(kwargs["pyrsigmas"])
        operator_reg.SetShrinkFactorsPerLevel(kwargs["pyrfactors"])

        scales = operator_optimizer.GetScales()
        scales.SetSize(6)
        scales[0] = 1.0
        scales[1] = 1.0
        scales[2] = 1.0
        scales[3] = 1e-3
        scales[4] = 1e-3
        scales[5] = 1e-3
        operator_optimizer.SetScales(scales)

        def watcher(counter=[0]):
            """
            Defines the function which runs at each iteration of registration.

            Adds 1 to counter.

            """
            counter[0] += 1
            total = kwargs["niterations"] * kwargs["pyrlevels"]
            print("Progress: " + str(counter[0]) + "/" + str(total), end="\r")

        if self.verbosity > 1:
            operator_optimizer.AddObserver(
                itk.IterationEvent(),
                watcher,
            )
        operator_reg.Update()

        finalparameters = operator_reg.GetTransform().GetParameters()
        extractedparameters = np.array(
            [
                finalparameters.GetElement(i)
                for i in range(finalparameters.GetNumberOfElements())
            ]
        )
        T = (
            AffineTensor(self.ndim)
            .rotate(*extractedparameters[2::-1])
            .translate(*extractedparameters[3:])
        )
        npT2itkT = AffineTensor(self.ndim).swap(0, 2)

        voiT = (
            AffineTensor(self.ndim)
            .translate(*(-voi.pos))
            .scale(*(resolution / self.affine.scale()))
        )
        scaling = AffineTensor(self.ndim).scale(*resolution)
        Tstar = multidot(
            voiT.copy().inv(),
            scaling.copy(),
            npT2itkT.copy(),
            T,
            npT2itkT.copy().inv(),
            scaling.copy().inv(),
            voiT.copy(),
        )

        if self.verbosity > 1:
            print(operator_optimizer.GetStopConditionDescription())
        self.affine.affine(Tstar)
        # import ctpros

        # ctpros.GUI(self, reference).mainloop()
        return self, Tstar


@dec.for_all_methods(dec.inplace, dec.selfisparent)
class Transform(MethodGroup):
    def affine(
        self,
        affine=None,
        voi=None,
        *,
        interp=1,
        dtype=None,
        outofbounds="grid-constant",
        constantval=0.0,
    ):
        """
        Generates a new image from an affine transform of an image.

        Parameters:
            affine: img.AffineTensor (defaults to doing nothing)
                Affine tensor to be applied to image for affine transformation.
                This does not update the affine object of the image, it only informs the output.
            voi: img.VOI (defaults to using image's VOI)
                Volume of interest to sample of affine transformation.
                Overrides image's VOI for sampling if inputted.
            interp: string or int
                Defines interpolation degree.
                0 == nearest
                1 == linear
                etc.
            dtype: NumPy datatype (i.e. np.single)
                dtype of the returned array
            outofbounds: string (default: "constant")
                Defines behavior of out of bounds sampling. See
                scipy.ndimage.affine for more detail.
            constantval: numeric (default: 0.)
                Defines the constant value out of bounds if out of bounds type is "constant"
        """
        if affine is None:
            affine = self.affine.copy()
        else:
            affine = self.affine.copy().affine(affine)
        if voi is None:
            voi = self.voi.copy()

        isbool = False
        if dtype == np.bool_:
            isbool = True
            dtype = np.single
        elif dtype is None:
            dtype = self.dtype
        else:  # default behavior: just use dtype in scipy's call
            pass

        transform, newshape = affine.voi(voi)
        newdata = type(self)(np.empty(newshape, dtype), self)

        sp.ndimage.affine_transform(
            self,
            np.linalg.inv(transform),
            output_shape=tuple(newshape),
            output=newdata,
            order=interp,
            prefilter=False,
            mode=outofbounds,
            cval=constantval,
        )
        if isbool:
            return newdata > 0.5
        else:
            return newdata

    def distance(self):
        _, S = self.affine.copy().decomposition("RS")
        return sp.ndimage.distance_transform_edt(self, S.scale())

    def gradient(self, sigma=1):
        array = sp.ndimage.gaussian_gradient_magnitude(self, sigma)
        return type(self)(array, self)

    def resample(self, *samplerate):
        samplerate = np.array(samplerate)
        affine = self.affine.copy().scale(*(1 / samplerate))
        voi = self.voi.copy()
        voi.shape[:] = voi.shape * self.affine.scale() / samplerate
        self.transform.affine(affine, voi)


def _data2itkimg(ndarray):
    """
    Returns an image view and blank image template of an n-dimensional array
    for processing through ITK functions.

    """
    img = itk.GetImageViewFromArray(ndarray)
    itktypeinfo = itk.template(img)[1]
    imgtype = itk.Image[itktypeinfo]
    return img, imgtype, itktypeinfo
