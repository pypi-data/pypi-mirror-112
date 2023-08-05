from . import utils
from . import methods

import os, copy, struct, datetime, fnmatch, itertools
import PIL

import numpy as np
import scipy as sp
import tqdm
import sys


class AffineTensor(np.ndarray):
    """
    Affine tensors describe a linear mapping from one space to another.

    For images, the mapping describes:
     - matrix index space --> physical coordinate space
       Ex: [0,0,0]px --> [offset_x,offset_y,offset_z] um
    """

    def __new__(thisclass, *args, **kwargs):
        if type(args[0]) == int:
            pdim = args[0]
        else:
            pdim = 1
        instance = super().__new__(thisclass, (pdim + 1, pdim + 1))
        instance[:] = np.eye(pdim + 1)
        if type(args[0]) == str:
            if os.path.isfile(args[0]):
                if os.path.splitext(args[0])[-1].lower() == ".tfm":
                    instance.fileloc = (
                        os.path.dirname(os.path.abspath(args[0])) + os.path.sep
                    )
                    instance.filename = os.path.basename(args[0])
                    instance.load()
                else:
                    raise Exception(
                        "Expected filetype *.tfm, received *{}".format(
                            os.path.splitext(args[0])[-1].lower()
                        )
                    )
            else:
                raise Exception("Could not find file {}".format(args[0]))

        return instance

    def __init__(self, pdim=3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pdim = self.shape[0] - 1

    def __array_finalize__(self, parent):
        self.pdim = getattr(parent, "pdim", 3)

    def _snap(self, eps_angle=1e-3, eps_stretch=1e-8):
        """Snaps the tensor to 0 rotation if rotations are extremely small"""
        angles = self.rotate()
        snapflags = np.array(
            [abs(angle) < eps_angle and angle != 0 for angle in angles]
        )
        if np.any(snapflags):
            snapped = np.array(
                [angle if abs(angle) >= eps_angle else 0 for angle in angles]
            )
            _, V, T = self.decomposition("RVT")
            V[V - np.eye(V.pdim + 1) < eps_stretch] = np.eye(V.pdim + 1)[
                V - np.eye(V.pdim + 1) < eps_stretch
            ]
            self[:] = (
                AffineTensor(self.pdim).affine(T).affine(V).rotate(*snapped, snap=False)
            )

    def decomposition(self, labels):
        """
        Labels in affine multiplication order. Labels define components to output
        and the order in which they are computed.

        V or stretch is the Left Stretch Tensor or the stretch in the un-decomposed coordinate system.
        To acquire u, the Right Stretch Tensor, pass V after R
        Example w/ Left Stretch:
        S,V,R,T,A = affine.decomposition("SVRTA")
            S = Scaling relative to new coordinate system
            V = Stretch between old and new coordinate system axes
            R = Rotation "   "
            T = Translation "   "
            A = Affine remainder of decomposition (in this case I)

        A common usage for this is to acquire the scaling or stretch
        of the elements in the original coordinate system:
            _, S = affine.decomposition("RS")
            original_scaling = S.scale()
        """
        affine = self.copy()  # matrix being modified
        components = []
        for label in labels:
            base = AffineTensor(affine.pdim)  # container for composite step
            if label.lower() == "r":
                base.rotate(*affine.rotate(snap=False), snap=False)
            elif label.lower() == "t":
                base.translate(*affine.translate())
            elif label.lower() == "s":
                base.scale(*affine.scale())
            elif label.lower() == "a":
                base.affine(affine)
            elif label.lower() == "v":
                base.stretch(*affine.stretch())
            else:
                raise Exception(
                    "Decomposition labels must be of the following:\nR: Rotation\nT: Translation\nS: Scaling\nA: Affine (remainder)"
                )
            affine.affine(base.copy().inv())
            components += [base]
        return components

    def load(self):
        """
        Loads n filename into the affine tensor, reshaping as necessary.

        """
        with open(self.fileloc + self.filename, "rb") as f:
            data = np.fromfile(f, np.float64)

        i = 0
        while 1:
            if len(data) == i * (i + 1):
                self.pdim = i
                break
            else:
                i += 1

        self.resize((self.pdim + 1, self.pdim + 1), refcheck=False)
        self[: self.pdim, : self.pdim + 1].ravel()[:] = data
        self.ravel()[-1] = 1
        return self

    def save(self):  # pragma: no cover
        self.saveas(self.fileloc + self.filename)

    def saveas(self, filename):
        """
        Saves the affine tensor to a file defined by the input filename.

        """
        self.fileloc = os.path.abspath(os.path.dirname(filename)) + os.path.sep
        self.filename = os.path.basename(filename)
        with open(self.fileloc + self.filename, "wb") as f:
            self[: self.pdim, : self.pdim + 1].tofile(f)

    def copy(self):
        return copy.deepcopy(self)

    def inv(self):
        self[:] = np.linalg.inv(self)
        return self

    def root(self):
        self[:] = sp.linalg.sqrtm(self)
        return self

    def flip(self, *axes, physshape):
        for axis in axes:
            self[axis, : self.pdim] = -self[axis, : self.pdim]
            self[axis, -1] += physshape[axis]
            self[axis, -1] -= self.scale()[axis]
        return self

    def swap(self, m, n):
        """
        Performs an axis swapping operation.
        """
        affine = AffineTensor(self.pdim)
        affine[m, m] = 0
        affine[n, n] = 0
        affine[m, n] = 1
        affine[n, m] = 1
        return self.affine(affine)

    def scale(self, *scales):
        if len(scales) == 0:
            return self._get_scaling()
        elif len(scales) == 1:
            scales = np.array([*([scales[0]] * self.pdim), 1]).astype(np.float64)
        else:
            scales = np.array([*scales, 1]).astype(np.float64)
        affine = np.eye(self.pdim + 1)
        affine *= scales
        self[:] = np.dot(affine, self)
        return self

    def _get_scaling(self):
        return np.linalg.norm(self[: self.pdim, : self.pdim], 2, 1)

    def translate(self, *translates):
        translates = np.array(translates, dtype=np.float64).ravel()
        if not translates.size:
            return self._get_translation()
        if translates.size != self.pdim:
            raise Exception
        self.ravel()[self._get_trans_inds()] += translates.ravel()
        return self

    def _get_translation(self):
        translation = np.empty(self.pdim, dtype=np.float64)
        translation[:] = self.ravel()[self._get_trans_inds()]
        return translation

    def _get_trans_inds(self):
        return np.arange(self.pdim, (self.pdim + 1) ** 2, self.pdim + 1)[:-1]

    def rotate(self, *angles, snap=True):
        """
        Angles are related by axis pairs generated via itertools.
        Ex:
            R = AffineTensor(3).rotate(a,b,c)
            (0,1) --> a (rotation from 0 towards 1)
            (0,2) --> b
            (1,2) --> c

        """
        if not angles:
            return self._get_rotation()
        expectedangles = sum(range(self.pdim))
        if len(angles) != expectedangles:
            raise Exception(
                "Expected {} angles for {}-dimensional Affine Tensor, but got {}.".format(
                    expectedangles, self.pdim, len(angles)
                )
            )

        result = np.eye(self.pdim + 1)
        for (x, y), angle in zip(itertools.combinations(range(self.pdim), 2), angles):
            R = np.eye(self.pdim + 1)
            R[[x, x, y, y], [x, y, x, y]] = (
                np.cos(angle),
                -np.sin(angle),
                np.sin(angle),
                np.cos(angle),
            )
            result[:] = np.dot(result, R)

        self[:] = np.dot(result, self)
        if snap:
            self._snap()
        return self

    def _get_rotation(self):
        """
        Returns the angles associated to the left rotation matrix
        via polar decomposition where F is self:

        F = RU
        F.T*F = U^2
        F = R*root(F.T*F)
        R = F*root(F.T*F)^-1

        Angles are extracted as follows:
            For rotation from axis x to y:
            1. Extract rotation matrix (R) from affine tensor.
            2. Multiply unit vector along x (r = R*e_x)
            3. Project r onto 2D plane x-y (e_x --> p_x, r --> p)
            4. angle = arctan2(cross(p_x,p),dot(p_x,p))

        """

        if self.pdim == 1:
            raise Exception(
                "Attempted to rotate a 1D affine tensor, where rotation does not exist in 1D."
            )
        else:
            angles = []
            F = self[: self.pdim, : self.pdim]
            R = AffineTensor(self.pdim)
            R[: self.pdim, : self.pdim] = F.copy().affine(F.T).root().inv().affine(F)
            for i, (x, y) in enumerate(itertools.combinations(range(self.pdim), 2)):
                e_x = [[0] for _ in range(self.pdim)]
                e_x[x][0] = 1
                r = np.dot(R[:-1, :-1], e_x)

                p_x = [0] * 2
                p_x[0] = 1
                p = [r[x][0], r[y][0]]
                angle = np.arctan2(np.cross(p_x, p), np.dot(p_x, p))
                angles += [angle]

                unrotate_angles = [0] * sum(range(self.pdim))
                unrotate_angles[i] = -angle
                R.rotate(*unrotate_angles, snap=False)

            return np.array([angle if angle != 0.0 else 0.0 for angle in angles])

    def stretch(self, *stretches):
        """
        Stretches are scaling relations between all axes in a coordinate system.
        This will pass the

        For a coordinate system F:
        F = VR = RU

        R is an orthogonal tensor and V/U are positive definite symmetric tensors.

        F*F^T = V^2
        V = sqrt(F*F^T)

        Stretches are defined in the orter of itertools combinations with replacement:

        affine.stretch(a,b,c) # 2D tensor --> 3 stretches
        a = stretch between old axis 0 and new axis 0
        b = stretch between old axis 0 and new axis 1 (by symmetry, the inverse relation is identical)
        c = stretch between old axis 1 and new axis 1
        """
        if not stretches:
            return self._get_stretch()
        expectedstretches = sum(range(self.pdim + 1))
        if len(stretches) != expectedstretches:
            raise Exception(
                "Expected {} stretches for {}-dimensional Affine Tensor, but got {}.".format(
                    expectedstretches, self.pdim, len(stretches)
                )
            )
        else:
            V = np.dot(self, self.T).root()
            self.affine(V.inv())

            indices = np.array(
                list(itertools.combinations_with_replacement(range(self.pdim), 2))
            )
            V[indices[:, 0], indices[:, 1]] = stretches
            stretches = [
                stretch
                for i, stretch in enumerate(stretches)
                if indices[i][0] != indices[i][1]
            ]
            indices = np.array([(y, x) for (x, y) in indices if x != y])
            V[indices[:, 0], indices[:, 1]] = stretches
            np.linalg.cholesky(V)  # asserts positive definite matrix
            self.affine(V)
            return self

    def _get_stretch(self):
        V = np.dot(
            self[: self.pdim, : self.pdim], self[: self.pdim, : self.pdim].T
        ).root()
        indices = np.array(
            list(itertools.combinations_with_replacement(range(self.pdim), 2))
        )
        return V[indices[:, 0], indices[:, 1]]

    def affine(self, myaffine):
        self[:] = np.dot(myaffine, self)
        return self

    def dot(self, vector):
        if not issubclass(type(vector), np.ndarray):
            vector = np.array(vector)
        if vector.shape[0] + 1 == self.shape[-1]:
            if vector.ndim == 1:
                return np.dot(self.view(np.ndarray), np.array([*vector, 1]))[:-1]
            else:
                padsize = vector.shape[1]
            return np.dot(self.view(np.ndarray), np.array([*vector, [1] * padsize]))[
                :-1
            ]
        else:
            return np.dot(self.view(np.ndarray), vector)

    def voi(self, myvoi):
        self.translate(-myvoi.pos)
        self.scale(*(1 / myvoi.elsize))
        return self, myvoi.shape.astype(int)

    def align(self, affine):
        """
        Alignment of two coordinate systems refers to the application of identical affine transformations over the base
        scale factor into physical coordinates.

        If affine A = RTS where "R","T","S" are composites of rotation, translation, and scaling, all but scaling are applied to the original affine

        affine.align(aligner) --> A.align(B) --> RaTaSa.align(RbTbSb) = RbTbSa

        """
        _, _, S = self.decomposition("RTS")
        R, T, _ = affine.decomposition("RTS")
        self[:] = S.affine(T).affine(R)
        return self


class VOI:
    """Volume Of Interest. Descriptor of volume grid of interest to be sampled.

    Has the following attributes of interest:
    - pos (um) = offset corner where sampling begins relative to physical space
    - shape (pix) = number of samples to take (pixels to draw)
    - elsize (um) = density for samples to be taken relative to physical space
    """

    def __repr__(self):
        return "position:\n{}\nshape:\n{}\nelsize:\n{}".format(
            self.pos, self.shape, self.elsize
        )

    def __init__(self, filename=None, *, pos=None, shape=None, elsize=None):
        """
        Instantiates the dimensionality of the VOI

        """
        if pos is None:
            self.pos = np.zeros((3, 1))
        else:
            self.pos = np.array(pos, dtype=np.float64).reshape((-1, 1))

        if shape is None:
            self.shape = np.zeros(3, dtype=np.uint64)
        else:
            self.shape = np.array(shape, dtype=np.uint64).reshape(-1)

        if elsize is None:
            self.elsize = np.ones(3)
        else:
            self.elsize = np.array(elsize, dtype=np.float64).reshape(-1)

        if filename is None:
            self.filename = filename
            self.fileloc = "." + os.path.sep
        elif type(filename) is str:
            if os.path.isfile(filename):
                if os.path.splitext(filename)[-1].lower() == ".voi":
                    self.filename = os.path.basename(filename)
                    self.fileloc = (
                        os.path.abspath(os.path.dirname(filename)) + os.path.sep
                    )
                    self.load()
                else:
                    raise Exception("VOI attempted to read non *.voi filetype.")
            else:
                raise Exception("VOI file {} not found.".format(filename))
        else:
            raise Exception("Unknown input when initializing class VOI.")

    def load(self):
        """
        Loads a binary file with VOI position and shape defined as doubles.

        """
        with open(self.fileloc + self.filename, "rb") as f:
            dtypes = (np.float64, np.uint64, np.float64)
            shapes = ((3, 1), (3), (3))
            self.pos, self.shape, self.elsize = [
                np.fromfile(f, dtype=dtype, count=3).reshape(shape)
                for dtype, shape in zip(dtypes, shapes)
            ]

        return self

    def saveas(self, filename):
        """
        Saves a binary file with VOI position and shape defined as doubles.

        """
        fileloc = os.path.abspath(os.path.dirname(filename)) + os.path.sep
        filename = os.path.basename(filename)
        if not os.path.isdir(fileloc):
            raise Exception(
                "Attempted to write file {} to path {} but path was not found.".format(
                    filename, fileloc
                )
            )
        else:
            self.filename = filename
            self.fileloc = fileloc
            with open(fileloc + filename, "wb") as f:
                self.pos.tofile(f)
                self.shape.tofile(f)
                self.elsize.tofile(f)

    def copy(self):
        return copy.deepcopy(self)


class ImgTemplate(np.ndarray):
    """
    Integrating a new subclass:

    1. Define the new subclass as a subclass of ImgTemplate
        `class NewClass(ImgTemplate)`
    2. Add the class name into the subclasses list under:
        - ImgTemplate._getsubclass method
    3. Add the extension `*.ext` to the supported_types in:
        module .__init__
    4. Define the following in your new class:
        Attributes:
            dict _base_header: default metadata in the header to be used for IO of an image generated by data
            dict defaults: default NumPy kwargs for generated images with partial information or placeholders until data is read
            str ext: file extension string
            dict reqs: key-value pairs which are required for a sensible IO pipeline (e.g. volumetric images must have 3 dimensions to save to disc)
        Methods:
            _read_protocol: how to read the metadata
            _load_protocol: how to read the raw data
            _save_protocol: how to save the metadata and raw data to the disc
            _tra_protocol: how to interpret the data as a tra slice
            _cor_protocol: how to interpret the data as a cor slice
            _sag_protocol: how to interpret the data as a sag slice

    """

    classify = methods.Classification
    filter = methods.Filters
    generic = methods.Generic
    numeric = methods.Numeric
    register = methods.Registration
    transform = methods.Transform

    @classmethod
    def _getsubclass(thisclass, filename):
        subclasses = [NDArray, AIM, JPEG, MDA]
        ext = [
            i
            for i, subclass in enumerate(subclasses)
            if len(
                fnmatch.filter([os.path.splitext(filename)[-1].lower()], subclass.ext)
            )
        ]
        if not ext:
            subclass = None
        else:
            subclass = subclasses[ext[0]]

        return subclass

    def _read_protocol(self):
        raise Exception(
            "Expected overwrite of _read_protocol method from ImgTemplate subclass."
        )

    def _load_protocol(self):
        raise Exception(
            "Expected overwrite of _load_protocol method from ImgTemplate subclass."
        )

    def _save_protocol(self):
        raise Exception(
            "Expected overwrite of _save_protocol method from ImgTemplate subclass."
        )

    def _tra_protocol(self):
        raise Exception(
            "Expected overwrite of _tra_protocol method from ImgTemplate subclass."
        )

    def _cor_protocol(self):
        raise Exception(
            "Expected overwrite of _cor_protocol method from ImgTemplate subclass."
        )

    def _sag_protocol(self):
        raise Exception(
            "Expected overwrite of _sag_protocol method from ImgTemplate subclass."
        )

    def __new__(thisclass, *args, verbosity=None, **kwargs):
        """
        Instance construction from super() methods goes here.

        Inputs are processed to define how instantiation proceeds:
            1) File-based: reads metadata and prepares for loading
                - `myimg = ImgClass(fullfilename)`
            2) Cast-based: converts the initial input array to the specified class
                - `myimg = ImgClass(myarray)`
            3) Numpy-based: creates empty array using NumPy's approach, but in type ImgClass
                - `myimg = ImgClass(shape=(x,y,z), dtype=np.uint8)`

        ImgClass changes the behavior related to IO. Subclasses of this template should
        contain the following methods:
            `_read_protocol` = reads metadata and otherwise prepare for data-loading protocol
            `_load_protocol` = fills in the array with the image data
            `_save_protocol` = runs validation protocol then proceeds to write to disk
            `_val_protocol` = validates that the data is compatible with known IO protocols
                - return True if valid, otherwise return False
                i.e. no known format for 64-bit 6-D AIM file, or 4-D JPEGs.
                Validation is tested only on save so as to permit flexibility in image processing
                transforms which may lead to temporary loss of, albeit unrequired, IO compatibility.

        ImgClass also defines how the subclass transforms to be displayed in 2-D:
            `_tra_protocol`,`_sag_protocol`,`_cor_protocol` return child instances of the transformed data
            for transaxial, sagittal, and coronal slices. These should be scaled and converted to uint8 and 2-D.
        """
        fileloc, filename, array, ndimg, args, kwargs = thisclass._update_defaults(
            *args, **kwargs
        )

        # file behavior
        if filename is not None:
            if not os.path.isfile(fileloc + filename):
                raise Exception("Cannot find file: \n" + fileloc + filename)

            if (
                thisclass == ImgTemplate
            ):  # try to assign more specific class for IO protocols
                subclass = thisclass._getsubclass(filename)
            else:  # if already specified subclass, validate extension
                subclass = thisclass
                subclass._assert_validfileext(filename)
            instance = ImgTemplate.__new__(subclass, *args, **kwargs)
            instance.fileloc = fileloc
            instance.filename = filename
            instance._read_protocol()

        # cast behavior
        elif array is not None:
            if ndimg is not None:
                instance = copy.deepcopy(array.view(thisclass))
                instance.__array_finalize__(ndimg)
            else:
                instance = array.view(thisclass)
                instance.__array_finalize__(array)

        # basic ndarray behavior
        else:
            instance = super().__new__(thisclass, *args, **kwargs)
            # instance.validforIO(raiseit=True)
        if verbosity is not None:
            instance.verbosity = verbosity
        return instance

    def __str__(self):
        return f"{type(self).__name__}(shape = {self.shape}, dtype = {self.dtype}, filename = '{self.filename}')"

    def __repr__(self):
        return self.__str__()

    def __array_finalize__(self, parent):
        """
        This is where object-creation house-keeping goes as view-casting is also calling
        this, but does not call __new__ or __init__.

        Thus, all instance inheritance of parent images belongs here.

        """
        self.verbosity = copy.deepcopy(getattr(parent, "verbosity", 2))
        self.fileloc = getattr(parent, "fileloc", os.getcwd() + os.path.sep)
        self.filename = getattr(parent, "filename", None)
        if type(self) == type(parent):
            self.header = copy.deepcopy(getattr(parent, "header", self._base_header))
        elif not getattr(self, "header", {}):
            self.header = copy.deepcopy(self._base_header)
        self.affine = copy.deepcopy(getattr(parent, "affine", AffineTensor(self.ndim)))
        self.position = copy.deepcopy(
            getattr(parent, "position", (np.array([self.shape]).T - 1) / 2)
        )
        self.voi = copy.deepcopy(getattr(parent, "voi", VOI(**self._init_voi_params())))
        self.classify = type(self).classify(self)
        self.filter = type(self).filter(self)
        self.generic = type(self).generic(self)
        self.numeric = type(self).numeric(self)
        self.register = type(self).register(self)
        self.transform = type(self).transform(self)

    def __array_ufunc__(self, ufunc, method, *args, out=None, **kwargs):
        args = [
            arg.view(np.ndarray) if issubclass(type(arg), np.ndarray) else arg
            for arg in args
        ]
        if out is not None:
            out = tuple(
                [o.view() if issubclass(type(o), ImgTemplate) else o for o in out]
            )
        result = super().__array_ufunc__(
            ufunc,
            method,
            *args,
            out=out,
            **kwargs,
        )

        if type(result) in [list, tuple]:
            result = [o.base if o.base is not None else o for o in result]
        elif type(result) == np.ndarray and result.base is not None:
            result = result.base

        if type(result) in [list, tuple]:
            result = [
                type(self)(o, self) if type(o) == np.ndarray else o for o in result
            ]
        elif type(result) == np.ndarray:
            result = type(self)(result, self)
        return result

    @classmethod
    def _update_defaults(thisclass, *args, **kwargs):
        if not args and not kwargs:
            raise Exception("See `help({})` for usage.".format(thisclass.__name__))
        if len(args) and type(args[0]) == str:
            fullfilename = args[0]
            filename = os.path.basename(fullfilename)
            fileloc = os.path.abspath(os.path.dirname(fullfilename)) + os.path.sep
            args = args[1:]
            if thisclass is ImgTemplate:
                thisclass = thisclass._getsubclass(filename)
        else:
            filename = None
            fileloc = os.getcwd() + os.path.sep

        for arg, key in zip(args, thisclass.defaults.keys()):
            if key in kwargs.keys():
                raise Exception("NDArray received multiple inputs in args and kwargs.")
            else:
                kwargs[key] = arg
                args = args[1:]
        utils.script.updatedict(kwargs, thisclass.defaults, mode="union")

        array = kwargs["shape"]  # first input
        ndimg = kwargs["dtype"]  # second input
        if not issubclass(type(array), np.ndarray) and not issubclass(
            type(array), ImgTemplate
        ):
            array = None
            ndimg = None
        if not issubclass(type(ndimg), ImgTemplate):
            ndimg = None

        return fileloc, filename, array, ndimg, args, kwargs

    @classmethod
    def _assert_validfileext(thisclass, filename):
        if thisclass != thisclass._getsubclass(filename):
            raise Exception(
                'Expected filetype "{}" for class {} IO protocol, but got {}'.format(
                    thisclass.ext, thisclass.__name__, os.path.splitext(filename)[-1]
                )
            )

    @classmethod
    def _assert_validdata(thisclass, ndim, dtype):
        if not (ndim in thisclass.reqs["ndims"] and dtype in thisclass.reqs["dtypes"]):
            raise Exception(
                "Expected dimensionality to be of {} and dtype to be of {}. Received {}-D {} array.".format(
                    thisclass.reqs["ndims"], thisclass.reqs["dtypes"], ndim, dtype
                )
            )

    def __str__header(self):  # pragma: no cover
        return "".join(
            [
                f"\n{label}: {value}"
                if "S" not in value.dtype.__str__()
                else f"\n{label}: \"{bytes(value).decode('ASCII')}\""
                for label, value in self.header.items()
            ]
        )

    def _init_voi_params(self):
        return {
            "pos": np.zeros_like(self.position),
            "shape": self.shape,
            "elsize": self.affine.scale(),
        }

    def reset_affine(self):
        self.affine = AffineTensor(self.ndim)

    def validforIO(self, raiseit=False):
        glossary = {
            "dtype": (self.dtype, self.reqs["dtypes"]),
            "ndim": (self.ndim, self.reqs["ndims"]),
        }

        msg = "".join(
            [
                f"\nExpected {label} to be: {[dtype for dtype in expected]}, but received {actual}"
                for label, (actual, expected) in glossary.items()
                if actual not in expected
            ]
        )
        if msg:
            if raiseit:
                raise Exception(msg)
            elif self.verbosity >= 2:  # pragma: no cover
                print(msg)
        return not bool(msg)

    def view(self, classtype=np.ndarray):
        return super().view(classtype)

    def print(self):  # pragma: no cover
        return print(self)

    def reload(self):
        self.clear()
        self.load()
        return self

    def load(self):
        if self.size:
            raise Exception(
                "Expected image to be empty, but has data loaded. Instead use .reload() which clears then loads the data from disc."
            )
        self._assert_validfileext(self.filename)
        self._load_protocol()
        self.position = ((np.array([self.shape]) - 1) // 2 * self.affine.scale()).T
        self.voi = VOI(**self._init_voi_params())

        return self

    def save(self):
        self._assert_validdata(self.ndim, self.dtype)
        self._save_protocol()
        return self

    def saveas(self, filename):
        self._assert_validfileext(filename)
        self.set_filename(filename)
        self.save()
        return self

    def set_filename(self, filename):
        self.filename = os.path.basename(filename)
        self.fileloc = os.path.abspath(os.path.dirname(filename)) + os.path.sep

    def clear(self, verbosity=None):
        if verbosity is None:
            verbosity = self.verbosity
        if verbosity >= 2:  # pragma: no cover
            print("Clearing {}".format(self.filename))
        self.resize((0,))

    def print_metadata(self):  # pragma: no cover
        return print(self.__str__header())

    def resize(self, new_shape, refcheck=False):
        super().resize(new_shape, refcheck=refcheck)

    def fill(self, filler):
        if issubclass(type(filler), np.ndarray):
            self.resize(filler.shape)
            self[:] = filler
        else:
            super().fill(filler)

    def squeeze(self, *, inplace=True):
        if inplace:
            self.shape = tuple(length for length in self.shape if length != 1)
            return self
        else:
            return super().squeeze()


class NDArray(ImgTemplate):
    """
    Subclass of NumPy array which permits use of package while maintaing as close to standard array behavior as possible
    """

    _base_header = {"descr": "<i2", "fortran_order": False, "shape": (0,)}

    defaults = {
        "shape": 0,
        "dtype": np.float64,
        "buffer": None,
        "offset": 0,
        "strides": None,
        "order": None,
    }
    ext = ".npy"
    reqs = {
        "dtypes": (
            np.bool_,
            np.uint8,
            np.int8,
            np.uint16,
            np.int16,
            np.float16,
            np.uint32,
            np.int32,
            np.float32,
            np.uint64,
            np.int64,
            np.float64,
        ),
        "ndims": np.arange(1000),
    }

    def _read_protocol(self):
        if self.filename is None:
            return
        with open(f"{self.fileloc}{self.filename}", "rb") as f:
            fbytes = f.read(10)
            mstring = fbytes[:6]
            v_maj = fbytes[6]
            v_min = fbytes[7]
            header_len = fbytes[8] + fbytes[9] * 256
            header_bytes = f.read(header_len)
            self.header = eval(header_bytes)
        return self

    def _fileshape(self):
        if self.filename is None:
            return self.shape
        else:
            return tuple(self.header["shape"])

    def _load_protocol(self):
        npy = np.load(self.fileloc + self.filename)
        self.dtype = npy.dtype
        self.fill(npy)
        self.affine = AffineTensor(self.ndim)

    def _save_protocol(self):
        np.save(self.fileloc + self.filename, self)

    def _tra_protocol(self, *, pos=None, voi=False):
        """
        Returns the affine matrix and VOI associated
        to acquiring a transaxial slice of the image.

        For an image with affine relation A:
                          A
            image space ----> physical space

        This returns a new transform B while transforming a
        VOI's position to be of the new space to be sampled:
                             B
            physical space ----> screen/new image space
        while transforming

        """
        shape = list(self.shape)
        voipos = np.zeros(3)
        elsize = self.affine.scale()
        default_voi = VOI(shape=shape, pos=voipos, elsize=elsize)
        if not voi:  # don't crop
            tra_voi = default_voi
        else:  # crop
            if issubclass(type(voi), VOI):  # use VOI if passed in
                tra_voi = voi.copy()
            else:  # use own VOI if non-voi passed
                tra_voi = self.voi.copy()

        tra_voi.shape[0] = 1
        if pos is None:
            tra_voi.pos[0] = self.position[0]
        else:
            tra_voi.pos[0] = pos

        tra_transform = AffineTensor(3)

        return tra_transform, tra_voi

    def _cor_protocol(self, *, pos=None, voi=False):
        if not voi:  # don't crop
            shape = list(self.shape)
            shape[1] = 1
            voipos = np.zeros(3)
            elsize = self.affine.scale()
            cor_voi = VOI(shape=shape, pos=voipos, elsize=elsize)
        else:  # crop
            if issubclass(type(voi), VOI):  # use VOI if passed in
                cor_voi = voi.copy()
            else:  # use own VOI if non-voi passed
                cor_voi = self.voi.copy()
            cor_voi.shape[1] = 1
        if pos is None:
            cor_voi.pos[1] = self.position[1]
        else:
            cor_voi.pos[1] = pos
        cor_transform = self.affine.copy().flip(
            0, physshape=utils.script.maxshape(self)
        )
        cor_transform = np.dot(cor_transform, self.affine.copy().inv())
        cor_voi.pos[:] = cor_transform.dot(cor_voi.pos)
        cor_voi.pos[0] -= cor_voi.elsize[0] * (cor_voi.shape[0] - 1)

        return cor_transform, cor_voi

    def _sag_protocol(self, *, pos=None, voi=False):
        if not voi:  # don't crop
            shape = list(self.shape)
            voipos = np.zeros(3)
            elsize = self.affine.scale()
            sag_voi = VOI(shape=shape, pos=voipos, elsize=elsize)
        else:  # crop
            if issubclass(type(voi), VOI):  # use VOI if passed in
                sag_voi = voi.copy()
            else:  # use own VOI if non-voi passed
                sag_voi = self.voi.copy()
        sag_voi.shape[2] = 1
        if pos is None:
            sag_voi.pos[2] = self.position[2]
        else:
            sag_voi.pos[2] = pos

        sag_transform = AffineTensor(3).swap(0, 1)
        sag_voi.shape[:] = sag_transform.dot(sag_voi.shape)
        sag_voi.elsize[:] = sag_transform.dot(sag_voi.elsize)
        sag_voi.pos[:] = sag_transform.dot(sag_voi.pos)

        return sag_transform, sag_voi


class AIM(ImgTemplate):
    """
    Help for AIM.
    """

    _template_headers = {
        2: {
            "version": np.array([], dtype=np.uint32),
            "blocksize": np.array([20, 140, 1, 0, 0], dtype=np.uint32),
            "hidden #1": np.array([16, 0, 0, 0, 0, 131074], dtype=np.uint32),
            "dim": np.array([0] * 3, dtype=np.uint32),
            "pos": np.array([0] * 3, dtype=np.uint32),
            "off": np.array([0] * 3, dtype=np.uint32),
            "supdim": np.array([0] * 3, dtype=np.uint32),
            "suppos": np.array([0] * 3, dtype=np.uint32),
            "subdim": np.array([0] * 3, dtype=np.uint32),
            "testoff": np.array([0] * 3, dtype=np.uint32),
            "elsize": np.array([0] * 12, dtype=np.uint8),
            "hidden #2": np.array([0] * 5, dtype=np.uint32),
            "process log": np.array(b"", dtype="S1"),
            "hidden #3": np.array([], dtype=np.uint32),
        },
        3: {
            "version": np.array("AIMDATA_V030   \x00", dtype="S16"),
            "blocksize": np.array([40, 224, 1, 0, 0], dtype=np.uint64),
            "hidden #1": np.array([24, 0, 0, 131074], dtype=np.uint32),
            "dim": np.array([0] * 3, dtype=np.uint64),
            "pos": np.array([0] * 3, dtype=np.uint64),
            "off": np.array([0] * 3, dtype=np.uint64),
            "supdim": np.array([0] * 3, dtype=np.uint64),
            "suppos": np.array([0] * 3, dtype=np.uint64),
            "subdim": np.array([0] * 3, dtype=np.uint64),
            "testoff": np.array([0] * 3, dtype=np.uint64),
            "elsize": np.array([0] * 3, dtype=np.uint64),
            "hidden #2": np.array([0] * 4, dtype=np.uint32),
            "process log": np.array(b"", dtype="S1"),
            "hidden #3": np.array([], dtype=np.uint32),
        },
    }

    _base_header = _template_headers[3]

    defaults = {
        "shape": (0, 0, 0),
        "dtype": np.int16,
        "buffer": None,
        "offset": 0,
        "strides": None,
        "order": None,
    }
    ext = ".aim*"
    reqs = {"dtypes": (np.int8, np.int16), "ndims": (3,)}

    def __array_finalize__(self, *args, **kwargs):
        super().__array_finalize__(*args, **kwargs)
        self._header_update()

    def _fileshape(self):
        if self.filename is None:
            return self.shape
        else:
            return tuple(np.flip(self.header["dim"]))

    def _read_protocol(self):
        if self.filename is None:
            return self

        with open(self.fileloc + self.filename, "rb") as f:
            if f.read(16) == b"AIMDATA_V030   \x00":
                version = 3
            else:
                version = 2
            f.seek(0)

            if version == 2:
                headerstruct = {
                    "version": ([], np.uint32),
                    "blocksize": (struct.unpack("5I", f.read(5 * 4)), np.uint32),
                    "hidden #1": (struct.unpack("6I", f.read(6 * 4)), np.uint32),
                    "pos": (struct.unpack("3I", f.read(3 * 4)), np.uint32),
                    "dim": (struct.unpack("3I", f.read(3 * 4)), np.uint32),
                    "off": (struct.unpack("3I", f.read(3 * 4)), np.uint32),
                    "supdim": (struct.unpack("3I", f.read(3 * 4)), np.uint32),
                    "suppos": (struct.unpack("3I", f.read(3 * 4)), np.uint32),
                    "subdim": (struct.unpack("3I", f.read(3 * 4)), np.uint32),
                    "testoff": (struct.unpack("3I", f.read(3 * 4)), np.uint32),
                    "elsize": (struct.unpack("12B", f.read(3 * 4)), np.uint8),
                    "hidden #2": (struct.unpack("5I", f.read(5 * 4)), np.uint32),
                }
            elif version == 3:
                headerstruct = {
                    "version": (f.read(16), None),
                    "blocksize": (struct.unpack("5Q", f.read(5 * 8)), np.uint64),
                    "hidden #1": (struct.unpack("4I", f.read(4 * 4)), np.uint32),
                    "pos": (struct.unpack("3Q", f.read(3 * 8)), np.uint64),
                    "dim": (struct.unpack("3Q", f.read(3 * 8)), np.uint64),
                    "off": (struct.unpack("3Q", f.read(3 * 8)), np.uint64),
                    "supdim": (struct.unpack("3Q", f.read(3 * 8)), np.uint64),
                    "suppos": (struct.unpack("3Q", f.read(3 * 8)), np.uint64),
                    "subdim": (struct.unpack("3Q", f.read(3 * 8)), np.uint64),
                    "testoff": (struct.unpack("3Q", f.read(3 * 8)), np.uint64),
                    "elsize": (struct.unpack("3Q", f.read(3 * 8)), np.uint64),
                    "hidden #2": (struct.unpack("4I", f.read(4 * 4)), np.uint32),
                }
            else:  # pragma: no cover
                raise Exception(f"No defined structure for AIM version: {version}.")
            loglen = headerstruct["blocksize"][0][2]
            headerstruct["process log"] = (f.read(loglen), None)
            f.seek(headerstruct["blocksize"][0][3], 1)
            headerstruct["hidden #3"] = (f.read(self.header["blocksize"][4]), None)

        for field, (data, dtype) in headerstruct.items():
            self.header[field] = np.array(data, dtype)
        if not self.header["blocksize"][
            4
        ]:  # pragma: no cover # no example of footer data interpretation
            self.header["hidden #3"] = AIM._template_headers[version]["hidden #3"]

        if self._version() == 2:
            ind_dtype = 5
        else:  # self._version() == 3:
            ind_dtype = 3

        if self.header["hidden #1"][ind_dtype] == 65537:
            self.dtype = np.int8
        else:  # self.header["hidden #1"][ind_dtype] == 131074:
            self.dtype = np.int16

        self.affine = self._elsize2affine()
        self.voi = VOI(**self._init_voi_params())
        return self

    def _load_protocol(self, *, iterator=None):
        self.resize(np.flip(self.header["dim"]))
        with open(self.fileloc + self.filename, "rb") as f:
            f.seek(np.sum(self.header["blocksize"][:3]))
            if self._version() == 3:  # version 3 has the 16-byte version string
                f.seek(16, 1)
            if iterator is None:
                iterator = self.get_load_iterator()
            for i in iterator:
                self[i].ravel()[:] = np.fromfile(
                    f, dtype=self.dtype, count=np.prod(self.shape[1:])
                )
        self.position.ravel()[:] = (np.array(self.shape) - 1) // 2 * self.affine.scale()

        return self

    def _save_protocol(self):
        self._header_update()
        headerstruct = [
            "version",
            "blocksize",
            "hidden #1",
            "pos",
            "dim",
            "off",
            "supdim",
            "suppos",
            "subdim",
            "testoff",
            "elsize",
            "hidden #2",
            "process log",
        ]
        with open(self.fileloc + self.filename, "wb") as f:
            for head in headerstruct:
                self.header[head].tofile(f)

            iterator = range(self.shape[0])
            for i in iterator:
                self[i].tofile(f)

            self.header["hidden #3"].tofile(f)
        return None

    def _tra_protocol(self, *, pos=None, voi=False):
        """
        Returns the affine matrix and VOI associated
        to acquiring a transaxial slice of the image.

        For an image with affine relation A:
                          A
            image space ----> physical space

        This returns a new transform B while transforming a
        VOI's position to be of the new space to be sampled:
                             B
            physical space ----> screen/new image space
        while transforming

        """
        shape = list(self.shape)
        voipos = np.zeros(3)
        elsize = self.affine.scale()
        default_voi = VOI(shape=shape, pos=voipos, elsize=elsize)
        if not voi:  # don't crop
            tra_voi = default_voi
        else:  # crop
            if issubclass(type(voi), VOI):  # use VOI if passed in
                tra_voi = voi.copy()
            else:  # use own VOI if non-voi passed
                tra_voi = self.voi.copy()

        tra_voi.shape[0] = 1
        if pos is None:
            tra_voi.pos[0] = self.position[0]
        else:
            tra_voi.pos[0] = pos

        tra_transform = AffineTensor(3)

        return tra_transform, tra_voi

    def _cor_protocol(self, *, pos=None, voi=False):
        if not voi:  # don't crop
            shape = list(self.shape)
            shape[1] = 1
            voipos = np.zeros(3)
            elsize = self.affine.scale()
            cor_voi = VOI(shape=shape, pos=voipos, elsize=elsize)
        else:  # crop
            if issubclass(type(voi), VOI):  # use VOI if passed in
                cor_voi = voi.copy()
            else:  # use own VOI if non-voi passed
                cor_voi = self.voi.copy()
            cor_voi.shape[1] = 1
        if pos is None:
            cor_voi.pos[1] = self.position[1]
        else:
            cor_voi.pos[1] = pos
        cor_transform = self.affine.copy().flip(
            0, physshape=utils.script.maxshape(self)
        )
        cor_transform = np.dot(cor_transform, self.affine.copy().inv())
        cor_voi.pos[:] = cor_transform.dot(cor_voi.pos)
        cor_voi.pos[0] -= cor_voi.elsize[0] * (cor_voi.shape[0] - 1)

        return cor_transform, cor_voi

    def _sag_protocol(self, *, pos=None, voi=False):
        if not voi:  # don't crop
            shape = list(self.shape)
            voipos = np.zeros(3)
            elsize = self.affine.scale()
            sag_voi = VOI(shape=shape, pos=voipos, elsize=elsize)
        else:  # crop
            if issubclass(type(voi), VOI):  # use VOI if passed in
                sag_voi = voi.copy()
            else:  # use own VOI if non-voi passed
                sag_voi = self.voi.copy()
        sag_voi.shape[2] = 1
        if pos is None:
            sag_voi.pos[2] = self.position[2]
        else:
            sag_voi.pos[2] = pos

        sag_transform = AffineTensor(3).swap(0, 1)
        sag_voi.shape[:] = sag_transform.dot(sag_voi.shape)
        sag_voi.elsize[:] = sag_transform.dot(sag_voi.elsize)
        sag_voi.pos[:] = sag_transform.dot(sag_voi.pos)

        return sag_transform, sag_voi

    def _header_update(self, **kwargs):
        """
        Enforces header to be appropriate to data for proper IO

        """
        if self.dtype == np.int16:
            self.header["hidden #1"][-1] = 131074
        elif self.dtype == np.int8:
            self.header["hidden #1"][-1] = 65537

        if self.nbytes > 2 ** 32 and self._version() == 2:  # pragma: no cover
            self._versionchange(3)

        self.header["blocksize"][2] = self.header["process log"].nbytes
        self.header["blocksize"][3] = self.nbytes
        self.header["blocksize"][4] = self.header["hidden #3"].nbytes

        if self.ndim == 3:
            self.header["dim"][:] = tuple(reversed(self.shape))
            self.header["elsize"][:] = self._affine2elsize()

    def _version(self):
        vstring = self.header["version"]
        if not vstring.size:
            return 2
        elif vstring == b"AIMDATA_V030   \x00":
            return 3
        else:  # pragma: no cover
            raise Exception(
                f"Version string '{vstring}' has no identified interpretation."
            )

    def _elsize2affine(self):
        """
        AIM v2:
            Converts the non-sensical header elsize ordering of AIM v2 into sensical order
            for proper value interpretation. The elsize should be in dtype uint8 to reorder.
            Tries to cast to uint8 just in case it's not.

        AIM v3:
            Simple casting and scaling.

        All:
            Flips the output since the NumPy and Scanco indices are inverted.

        Parameters:
            - self (post-_reading for a sensical calling)

        Returns:
            - elsize (ndarray,dtype=np.float32 (v2) or np.float64 (v3))


        """
        if self._version() == 2:
            nonsensical = self.header["elsize"]
            nonsensical.dtype = np.uint8
            sensical = nonsensical[[2, 3, 0, 1, 6, 7, 4, 5, 10, 11, 8, 9]]
            sensical.dtype = np.float32
            elsize = sensical / 4e-3
        elif self._version() == 3:
            elsize = self.header["elsize"].astype(np.float64) / 10000
        else:  # pragma: no cover
            raise Exception(
                f"Identified version {self._version()} has no interpretation."
            )

        return AffineTensor(len(elsize)).scale(*np.flip(elsize))

    def _affine2elsize(self):
        """
        Returns an array of elsizes from the current affine
        transformed coordinate system.

        """
        phys = np.flip(self.affine.scale())
        if self._version() == 2:
            phys = phys.astype(np.float32)
            phys *= 4e-3
            phys.dtype = np.uint8
            nonsensical = phys[[2, 3, 0, 1, 6, 7, 4, 5, 10, 11, 8, 9]]
            elsize = nonsensical
        elif self._version() == 3:
            elsize = np.round(phys * 10000).astype(np.uint64)
        else:  # pragma: no cover
            raise Exception(
                f"Version type {self._version()} has no identified affine elsize conversion."
            )

        return elsize

    def _versionchange(self, version, *, inplace=True):
        """
        Transforms aim version to inputted version #.

        Ex:
            Given an AIM `filename` corresponds to a version 2 (32-bit) AIM,
            AIM(filename)._versionchange(3) converts the aim into version 3 with proper IO header data.

            This should only be used internally to enforce larger files are translated to v3
            when size does not permit v2 (32-bit) size compatibility.

        """
        if self._version() == version:
            return self
        if not inplace:
            self = type(self)(self)

        oldheader = copy.deepcopy(self.header)
        if version == 2:  # pragma: no cover
            if self.nbytes > 2 ** 32:
                raise Exception("AIM too large for version 2 format.")

        self.header = copy.deepcopy(AIM._template_headers[version])
        self.header["process log"] = oldheader["process log"]
        self._header_update()
        return self

    def _init_voi_params(self):
        pixelsize = np.flip(self.header["dim"])
        return {
            "pos": [0, 0, 0],
            "shape": pixelsize,
            "elsize": self.affine.scale(),
        }

    def reset_affine(self):
        self.affine = self._elsize2affine()

    def get_load_iterator(self, verbosity=None):
        slices = np.flip(self.header["dim"])[0]
        if verbosity is None:
            verbosity = self.verbosity
        iterator = range(slices)
        return iterator


class JPEG(ImgTemplate):
    _base_header = {}
    defaults = {
        "shape": (0, 0),
        "dtype": np.uint8,
        "buffer": None,
        "offset": 0,
        "strides": None,
        "order": None,
    }
    ext = ".jpg"
    reqs = {
        "dtypes": (
            np.bool_,
            np.uint8,
            np.int8,
            np.uint16,
            np.int16,
            np.float16,
            np.uint32,
            np.int32,
            np.float32,
            np.uint64,
            np.int64,
            np.float64,
        ),
        "ndims": (2,),
    }

    def _read_protocol(self):
        if self.filename is None:
            return self
        self.header = PIL.Image.open(self.fileloc + self.filename)

    def _load_protocol(self, *, iterator=None):
        self.resize(tuple(reversed(self.header.size)))
        self[:] = np.array(self.header.convert("L"))
        self.header.close()
        self.position.ravel()[:] = (np.array(self.shape) - 1) // 2 * self.affine.scale()
        return self

    def _save_protocol(self):
        headerstruct = [
            "version",
            "blocksize",
            "hidden #1",
            "pos",
            "dim",
            "off",
            "supdim",
            "suppos",
            "subdim",
            "testoff",
            "elsize",
            "hidden #2",
            "process log",
        ]
        with open(self.fileloc + self.filename, "wb") as f:
            for head in headerstruct:
                self.header[head].tofile(f)

            iterator = range(self.shape[0])
            for i in iterator:
                self[i].tofile(f)

            self.header["hidden #3"].tofile(f)
        return None

    def _tra_protocol(self, *, pos=None, voi=False):
        """
        Returns the affine matrix and VOI associated
        to acquiring a transaxial slice of the image.

        For an image with affine relation A:
                          A
            image space ----> physical space

        This returns a new transform B while transforming a
        VOI's position to be of the new space to be sampled:
                             B
            physical space ----> screen/new image space
        while transforming

        """
        shape = list(self.shape)
        voipos = np.zeros(3)
        elsize = self.affine.scale()
        default_voi = VOI(shape=shape, pos=voipos, elsize=elsize)
        if not voi:  # don't crop
            tra_voi = default_voi
        else:  # crop
            if issubclass(type(voi), VOI):  # use VOI if passed in
                tra_voi = voi.copy()
            else:  # use own VOI if non-voi passed
                tra_voi = self.voi.copy()

        tra_voi.shape[0] = 1
        if pos is None:
            tra_voi.pos[0] = self.position[0]
        else:
            tra_voi.pos[0] = pos

        tra_transform = AffineTensor(3)

        return tra_transform, tra_voi

    def _cor_protocol(self, *args, **kwargs):
        return None

    def _sag_protocol(self, *args, **kwargs):
        return None


class MDA(ImgTemplate):
    _base_header = {}
    defaults = {
        "shape": (0, 0, 0),
        "dtype": np.complex64,
        "buffer": None,
        "offset": 0,
        "strides": None,
        "order": None,
    }
    ext = ".mda"
    reqs = {
        "dtypes": (
            np.float32,
            np.complex64,
        ),
        "ndims": (1, 2, 3, 4, 5),
    }

    def _read_protocol(self):
        """
        Struct:

        int32[1] = (ndim) number of dimensions, or flag (when val<0)
        if first byte is a flag:
            int32[1] = total number of bytes of image
            int32[1] = (ndim) number of dimensions
        int32[ndim] = (shape) shape of each dimension

        if flag==-1:
            complex64[prod(shape)] = data as complex numbers: (float32) + i*(float32)
        elif flag ==-2:
            byte[prod(shape)] = data as bytestring
        elif flag ==-3:
            float32[prod(shape)] = data as real number


        """
        if self.filename is None:
            return self
        with open(self.fileloc + self.filename, "rb") as f:
            ndims = np.fromfile(f, "int32", 1)[0]
            if ndims < 0:  # ndims is flag
                dtype = ["float", "uchar", "complex64"][ndims]
                f.read(1)
                ndims = f.read(1)[0]
            else:
                dtype = "complex64"
            shape = np.fromfile(f, "int32", 3)
            offset = f.tell()
            datasize = np.prod(shape)

        self.header = {
            "shape": shape,
            "dtype": dtype,
            "headersize": offset,
            "datasize": datasize,
        }

    def _load_protocol(self, *, iterator=None):
        self.resize(self.header["shape"])
        with open(self.fileloc + self.filename, "rb") as f:
            f.seek(self.header["headersize"])
            self.ravel()[:] = np.fromfile(
                f, self.header["dtype"], self.header["datasize"]
            )
        self.position.ravel()[:] = (np.array(self.shape) - 1) // 2 * self.affine.scale()
        return self

    def _save_protocol(self):
        self._update_header()
        with open(self.fileloc + self.filename, "wb") as f:
            if not self.dtype == np.complex64:  # write flag
                if self.dtype == np.float32:  # flag == -3
                    np.array([-3], np.int32).tofile(f)

                np.array([self.size], np.int32).tofile(f)
                # more flags to add after clarification of different dtype structures
            np.array(self.ndim, np.int32).tofile(f)
            np.array(self.shape, np.int32).tofile(f)

            self.tofile(f)
        return None

    def _update_header(self):
        self.header["shape"] = np.array(self.shape, dtype=np.int32)
        self.header["dtype"] = str(self.dtype)
        self.header["datasize"] = self.size

    def _tra_protocol(self, *, pos=None, voi=False):
        """
        Returns the affine matrix and VOI associated
        to acquiring a transaxial slice of the image.

        For an image with affine relation A:
                          A
            image space ----> physical space

        This returns a new transform B while transforming a
        VOI's position to be of the new space to be sampled:
                             B
            physical space ----> screen/new image space
        while transforming

        """
        shape = list(self.shape)
        voipos = np.zeros(3)
        elsize = self.affine.scale()
        default_voi = VOI(shape=shape, pos=voipos, elsize=elsize)
        if not voi:  # don't crop
            tra_voi = default_voi
        else:  # crop
            if issubclass(type(voi), VOI):  # use VOI if passed in
                tra_voi = voi.copy()
            else:  # use own VOI if non-voi passed
                tra_voi = self.voi.copy()

        tra_voi.shape[0] = 1
        if pos is None:
            tra_voi.pos[0] = self.position[0]
        else:
            tra_voi.pos[0] = pos

        tra_transform = AffineTensor(3)

        return tra_transform, tra_voi

    def _cor_protocol(self, *, pos=None, voi=False):
        if not voi:  # don't crop
            shape = list(self.shape)
            shape[1] = 1
            voipos = np.zeros(3)
            elsize = self.affine.scale()
            cor_voi = VOI(shape=shape, pos=voipos, elsize=elsize)
        else:  # crop
            if issubclass(type(voi), VOI):  # use VOI if passed in
                cor_voi = voi.copy()
            else:  # use own VOI if non-voi passed
                cor_voi = self.voi.copy()
            cor_voi.shape[1] = 1
        if pos is None:
            cor_voi.pos[1] = self.position[1]
        else:
            cor_voi.pos[1] = pos
        cor_transform = self.affine.copy().flip(
            0, physshape=utils.script.maxshape(self)
        )
        cor_transform = np.dot(cor_transform, self.affine.copy().inv())
        cor_voi.pos[:] = cor_transform.dot(cor_voi.pos)
        cor_voi.pos[0] -= cor_voi.elsize[0] * (cor_voi.shape[0] - 1)

        return cor_transform, cor_voi

    def _sag_protocol(self, *, pos=None, voi=False):
        if not voi:  # don't crop
            shape = list(self.shape)
            voipos = np.zeros(3)
            elsize = self.affine.scale()
            sag_voi = VOI(shape=shape, pos=voipos, elsize=elsize)
        else:  # crop
            if issubclass(type(voi), VOI):  # use VOI if passed in
                sag_voi = voi.copy()
            else:  # use own VOI if non-voi passed
                sag_voi = self.voi.copy()
        sag_voi.shape[2] = 1
        if pos is None:
            sag_voi.pos[2] = self.position[2]
        else:
            sag_voi.pos[2] = pos

        sag_transform = AffineTensor(3).swap(0, 1)
        sag_voi.shape[:] = sag_transform.dot(sag_voi.shape)
        sag_voi.elsize[:] = sag_transform.dot(sag_voi.elsize)
        sag_voi.pos[:] = sag_transform.dot(sag_voi.pos)

        return sag_transform, sag_voi
