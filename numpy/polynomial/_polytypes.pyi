import decimal
import numbers
import sys
from collections.abc import Callable, Sequence
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Protocol,
    SupportsIndex,
    SupportsInt,
    TypeAlias,
    TypeVar,
    final,
    overload,
)

import numpy as np
import numpy.typing as npt
from numpy._typing import (
    # array-likes
    _ArrayLikeFloat_co,
    _ArrayLikeComplex_co,
    _ArrayLikeNumber_co,
    _ArrayLikeObject_co,
    _NestedSequence,

    # scalar-likes
    _IntLike_co,
    _FloatLike_co,
    _ComplexLike_co,
    _NumberLike_co,
)

if sys.version_info >= (3, 11):
    from typing import LiteralString
elif TYPE_CHECKING:
    from typing_extensions import LiteralString
else:
    LiteralString: TypeAlias = str

_T = TypeVar("_T", bound=object)
_Tuple2: TypeAlias = tuple[_T, _T]

_V = TypeVar("_V")
_V_co = TypeVar("_V_co", covariant=True)
_Self = TypeVar("_Self", bound=object)

_SCT = TypeVar("_SCT", bound=np.number[Any] | np.bool | np.object_)
_SCT_co = TypeVar(
    "_SCT_co",
    bound=np.number[Any] | np.bool | np.object_,
    covariant=True,
)

class _SupportsArray(Protocol[_SCT_co]):
    def __array__(self ,) -> npt.NDArray[_SCT_co]: ...

_Series: TypeAlias = np.ndarray[tuple[int], np.dtype[_SCT]]

_FloatSeries: TypeAlias = _Series[np.floating[Any]]
_ComplexSeries: TypeAlias = _Series[np.complexfloating[Any, Any]]
_NumberSeries: TypeAlias = _Series[np.number[Any]]
_ObjectSeries: TypeAlias = _Series[np.object_]
_CoefSeries: TypeAlias = _Series[np.inexact[Any] | np.object_]

_FloatArray: TypeAlias = npt.NDArray[np.floating[Any]]
_ComplexArray: TypeAlias = npt.NDArray[np.complexfloating[Any, Any]]
_ObjectArray: TypeAlias = npt.NDArray[np.object_]
_CoefArray: TypeAlias = npt.NDArray[np.inexact[Any] | np.object_]

_Array1: TypeAlias = np.ndarray[tuple[Literal[1]], np.dtype[_SCT]]
_Array2: TypeAlias = np.ndarray[tuple[Literal[2]], np.dtype[_SCT]]


_AnyInt: TypeAlias = SupportsInt | SupportsIndex

# NOTE: `decimal.Decimal` isn't compatible with `numbers.Real`, but e.g.
# `fractions.Fraction` is.
_NumberObjectLike_co: TypeAlias = (
    np.object_
    | numbers.Complex
    | decimal.Decimal
)
_CoefLike_co: TypeAlias = _NumberLike_co | _NumberObjectLike_co

# The term "series" is used here to refer to 1-d arrays of numeric scalars.
_SeriesLikeInt_co: TypeAlias = (
    _SupportsArray[np.integer[Any] | np.bool]
    | Sequence[_IntLike_co]
)
_SeriesLikeFloat_co: TypeAlias = (
    _SupportsArray[np.floating[Any] | np.integer[Any] | np.bool]
    | Sequence[_FloatLike_co]
)
_SeriesLikeComplex_co: TypeAlias = (
    _SupportsArray[np.integer[Any] | np.inexact[Any] | np.bool]
    | Sequence[_ComplexLike_co]
)
_SeriesLikeNumberObject_co: TypeAlias = (
    _SupportsArray[np.object_]
    | Sequence[_NumberObjectLike_co]
)
_SeriesLikeCoef_co: TypeAlias = (
    # npt.NDArray[np.number[Any] | np.bool | np.object_]
    _SupportsArray[np.number[Any] | np.bool | np.object_]
    | Sequence[_CoefLike_co]
)

_ArrayLikeNumberObject_co: TypeAlias = (
    _NumberObjectLike_co
    | _ArrayLikeComplex_co
    | _SeriesLikeNumberObject_co
    | _NestedSequence[_SeriesLikeNumberObject_co]
)
_ArrayLikeCoef_co: TypeAlias = (
    npt.NDArray[np.number[Any] | np.bool | np.object_]
    | _ArrayLikeNumber_co
    | _ArrayLikeNumberObject_co
)

_Name_co = TypeVar("_Name_co", bound=LiteralString, covariant=True)

class _Named(Protocol[_Name_co]):
    @property
    def __name__(self, /) -> _Name_co: ...

_Line: TypeAlias = np.ndarray[tuple[Literal[1, 2]], np.dtype[_SCT]]

@final
class _FuncLine(_Named[_Name_co], Protocol[_Name_co]):
    @overload
    def __call__(self, /, off: _SCT, scl: _SCT) -> _Line[_SCT]: ...  # type: ignore[overload-overlap]
    @overload
    def __call__(self, /, off: int, scl: int) -> _Line[np.int_] : ...  # type: ignore[overload-overlap]
    @overload
    def __call__(self, /, off: float, scl: float) -> _Line[np.float64]: ...
    @overload
    def __call__(
        self, /,
        off: complex,
        scl: complex,
    ) -> _Line[np.complex128]: ...
    @overload
    def __call__(self, /, off: object, scl: object) -> _Line[np.object_]: ...

@final
class _FuncFromRoots(_Named[_Name_co], Protocol[_Name_co]):
    @overload
    def __call__(self, /, roots: _SeriesLikeFloat_co) -> _FloatSeries: ...  # type: ignore[overload-overlap]
    @overload
    def __call__(self, /, roots: _SeriesLikeComplex_co) -> _ComplexSeries: ...
    @overload
    def __call__(self, /, roots: _SeriesLikeCoef_co) -> _ObjectSeries: ...

@final
class _FuncBinOp(_Named[_Name_co], Protocol[_Name_co]):
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        c1: _SeriesLikeFloat_co,
        c2: _SeriesLikeFloat_co,
    ) -> _FloatSeries: ...
    @overload
    def __call__(
        self, /,
        c1: _SeriesLikeComplex_co,
        c2: _SeriesLikeComplex_co,
    ) -> _ComplexSeries: ...
    @overload
    def __call__(
        self, /,
        c1: _SeriesLikeCoef_co,
        c2: _SeriesLikeCoef_co,
    ) -> _ObjectSeries: ...

@final
class _FuncUnOp(_Named[_Name_co], Protocol[_Name_co]):
    @overload
    def __call__(self, /, c: _SeriesLikeFloat_co) -> _FloatSeries: ...  # type: ignore[overload-overlap]
    @overload
    def __call__(self, /, c: _SeriesLikeComplex_co) -> _ComplexSeries: ...
    @overload
    def __call__(self, /, c: _SeriesLikeCoef_co) -> _ObjectSeries: ...

@final
class _FuncPoly2Ortho(_Named[_Name_co], Protocol[_Name_co]):
    @overload
    def __call__(self, /, pol: _SeriesLikeFloat_co) -> _FloatSeries: ...  # type: ignore[overload-overlap]
    @overload
    def __call__(self, /, pol: _SeriesLikeComplex_co) -> _ComplexSeries: ...
    @overload
    def __call__(self, /, pol: _SeriesLikeCoef_co) -> _ObjectSeries: ...

@final
class _FuncPow(_Named[_Name_co], Protocol[_Name_co]):
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        c: _SeriesLikeFloat_co,
        pow: _AnyInt,
        maxpower: None | _AnyInt = ...,
    ) -> _FloatSeries: ...
    @overload
    def __call__(
        self, /,
        c: _SeriesLikeComplex_co,
        pow: _AnyInt,
        maxpower: None | _AnyInt = ...,
    ) -> _ComplexSeries: ...
    @overload
    def __call__(
        self, /,
        c: _SeriesLikeCoef_co,
        pow: _AnyInt,
        maxpower: None | _AnyInt = ...,
    ) -> _ObjectSeries: ...

@final
class _FuncDer(_Named[_Name_co], Protocol[_Name_co]):
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        c: _ArrayLikeFloat_co,
        m: SupportsIndex = ...,
        scl: _NumberLike_co = ...,
        axis: SupportsIndex = ...,
    ) -> _FloatArray: ...
    @overload
    def __call__(
        self, /,
        c: _ArrayLikeComplex_co,
        m: SupportsIndex = ...,
        scl: _NumberLike_co = ...,
        axis: SupportsIndex = ...,
    ) -> _ComplexArray: ...
    @overload
    def __call__(
        self, /,
        c: _ArrayLikeNumberObject_co,
        m: SupportsIndex = ...,
        scl: _NumberLike_co = ...,
        axis: SupportsIndex = ...,
    ) -> _ObjectArray: ...

@final
class _FuncInteg(_Named[_Name_co], Protocol[_Name_co]):
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        c: _ArrayLikeFloat_co,
        m: SupportsIndex = ...,
        k: _NumberLike_co | Sequence[_NumberLike_co] = ...,
        lbnd: _NumberLike_co = ...,
        scl: _NumberLike_co = ...,
        axis: SupportsIndex = ...,
    ) -> _FloatArray: ...
    @overload
    def __call__(
        self, /,
        c: _ArrayLikeComplex_co,
        m: SupportsIndex = ...,
        k: _NumberLike_co | Sequence[_NumberLike_co] = ...,
        lbnd: _NumberLike_co = ...,
        scl: _NumberLike_co = ...,
        axis: SupportsIndex = ...,
    ) -> _ComplexArray: ...
    @overload
    def __call__(
        self, /,
        c: _ArrayLikeNumberObject_co,
        m: SupportsIndex = ...,
        k: _NumberLike_co | Sequence[_CoefLike_co] = ...,
        lbnd: _NumberLike_co = ...,
        scl: _NumberLike_co = ...,
        axis: SupportsIndex = ...,
    ) -> _ObjectArray: ...

_AnyRealRoots: TypeAlias = (
    _Series[np.floating[Any] | np.integer[Any]]
    | Sequence[_FloatLike_co]
)
_AnyComplexRoots: TypeAlias = (
    _Series[np.number[Any]]
    | Sequence[_NumberLike_co]
)
_AnyObjectRoots: TypeAlias = _ObjectSeries | Sequence[_NumberObjectLike_co]
_AnyRoots: TypeAlias = _CoefSeries | Sequence[_CoefLike_co]

_AnyRealPoints: TypeAlias = (
    npt.NDArray[np.floating[Any] | np.integer[Any]]
    | tuple[_ArrayLikeFloat_co, ...]
    | list[_ArrayLikeFloat_co]
)
_AnyComplexPoints: TypeAlias = (
    npt.NDArray[np.number[Any]]
    | tuple[_ArrayLikeComplex_co, ...]
    | list[_ArrayLikeComplex_co]
)
_AnyObjectPoints: TypeAlias = (
    _ObjectArray
    | tuple[_ArrayLikeNumberObject_co, ...]
    | list[_ArrayLikeNumberObject_co]
)
_AnyPoints: TypeAlias = (
    npt.NDArray[np.number[Any] | np.object_]
    | tuple[_ArrayLikeCoef_co, ...]
    | list[_ArrayLikeCoef_co]
)

@final
class _FuncValFromRoots(_Named[_Name_co], Protocol[_Name_co]):
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        x: _FloatLike_co,
        r: _FloatLike_co,
        tensor: bool = ...,
    ) -> np.floating[Any]: ...
    @overload
    def __call__(
        self, /,
        x: _NumberLike_co,
        r: _NumberLike_co,
        tensor: bool = ...,
    ) -> np.complexfloating[Any, Any]: ...
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        x: _CoefLike_co,
        r: _CoefLike_co,
        tensor: bool = ...,
    ) -> object: ...
    @overload
    def __call__(
        self, /,
        x: _FloatLike_co | _AnyRealPoints,
        r: _ArrayLikeFloat_co,
        tensor: bool = ...,
    ) -> _FloatArray: ...
    @overload
    def __call__(
        self, /,
        x: _NumberLike_co | _AnyComplexPoints,
        r: _ArrayLikeComplex_co,
        tensor: bool = ...,
    ) -> _ComplexArray: ...
    @overload
    def __call__(
        self, /,
        x: _CoefLike_co | _AnyPoints,
        r: _ArrayLikeCoef_co,
        tensor: bool = ...,
    ) -> _ObjectArray: ...

@final
class _FuncVal(_Named[_Name_co], Protocol[_Name_co]):
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        x: _FloatLike_co,
        c: _AnyRealRoots,
        tensor: bool = ...,
    ) -> np.floating[Any]: ...
    @overload
    def __call__(
        self, /,
        x: _NumberLike_co,
        c: _AnyComplexRoots,
        tensor: bool = ...,
    ) -> np.complexfloating[Any, Any]: ...
    @overload
    def __call__(
        self, /,
        x: _CoefLike_co,
        c: _AnyObjectRoots,
        tensor: bool = ...,
    ) -> object: ...
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        x: _AnyRealPoints,
        c: _ArrayLikeFloat_co,
        tensor: bool = ...,
    ) -> _FloatArray: ...
    @overload
    def __call__(
        self, /,
        x: _AnyComplexPoints,
        c: _ArrayLikeComplex_co,
        tensor: bool = ...,
    ) -> _ComplexArray: ...
    @overload
    def __call__(
        self, /,
        x: _AnyPoints,
        c: _ArrayLikeCoef_co,
        tensor: bool = ...,
    ) -> _ObjectArray: ...

@final
class _FuncVal2D(_Named[_Name_co], Protocol[_Name_co]):
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        x: _FloatLike_co,
        y: _FloatLike_co,
        c: _AnyRealRoots,
    ) -> np.floating[Any]: ...
    @overload
    def __call__(
        self, /,
        x: _NumberLike_co,
        y: _NumberLike_co,
        c: _AnyComplexRoots,
    ) -> np.complexfloating[Any, Any]: ...
    @overload
    def __call__(
        self, /,
        x: _CoefLike_co,
        y: _CoefLike_co,
        c: _AnyRoots,
    ) -> object: ...
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        x: _AnyRealPoints,
        y: _AnyRealPoints,
        c: _ArrayLikeFloat_co,
    ) -> _FloatArray: ...
    @overload
    def __call__(
        self, /,
        x: _AnyComplexPoints,
        y: _AnyComplexPoints,
        c: _ArrayLikeComplex_co,
    ) -> _ComplexArray: ...
    @overload
    def __call__(
        self, /,
        x: _AnyPoints,
        y: _AnyPoints,
        c: _ArrayLikeCoef_co,
    ) -> _ObjectArray: ...

@final
class _FuncVal3D(_Named[_Name_co], Protocol[_Name_co]):
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        x: _FloatLike_co,
        y: _FloatLike_co,
        z: _FloatLike_co,
        c: _AnyRealRoots
    ) -> np.floating[Any]: ...
    @overload
    def __call__(
        self, /,
        x: _NumberLike_co,
        y: _NumberLike_co,
        z: _NumberLike_co,
        c: _AnyComplexRoots,
    ) -> np.complexfloating[Any, Any]: ...
    @overload
    def __call__(
        self, /,
        x: _CoefLike_co,
        y: _CoefLike_co,
        z: _CoefLike_co,
        c: _AnyRoots,
    ) -> object: ...
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        x: _AnyRealPoints,
        y: _AnyRealPoints,
        z: _AnyRealPoints,
        c: _ArrayLikeFloat_co,
    ) -> _FloatArray: ...
    @overload
    def __call__(
        self, /,
        x: _AnyComplexPoints,
        y: _AnyComplexPoints,
        z: _AnyComplexPoints,
        c: _ArrayLikeComplex_co,
    ) -> _ComplexArray: ...
    @overload
    def __call__(
        self, /,
        x: _AnyPoints,
        y: _AnyPoints,
        z: _AnyPoints,
        c: _ArrayLikeCoef_co,
    ) -> _ObjectArray: ...

_AnyValF: TypeAlias = Callable[
    [npt.ArrayLike, npt.ArrayLike, bool],
    _CoefArray,
]

@final
class _FuncValND(_Named[_Name_co], Protocol[_Name_co]):
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self,
        val_f: _AnyValF,
        c: _AnyRealRoots,
        /,
        *args: _FloatLike_co,
    ) -> np.floating[Any]: ...
    @overload
    def __call__(
        self,
        val_f: _AnyValF,
        c: _AnyComplexRoots,
        /,
        *args: _NumberLike_co,
    ) -> np.complexfloating[Any, Any]: ...
    @overload
    def __call__(
        self,
        val_f: _AnyValF,
        c: _AnyObjectRoots,
        /,
        *args: _NumberObjectLike_co,
    ) -> object: ...
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self,
        val_f: _AnyValF,
        c: _ArrayLikeFloat_co,
        /,
        *args: _AnyRealPoints,
    ) -> _FloatArray: ...
    @overload
    def __call__(
        self,
        val_f: _AnyValF,
        c: _ArrayLikeComplex_co,
        /,
        *args: _AnyComplexPoints,
    ) -> _ComplexArray: ...
    @overload
    def __call__(
        self,
        val_f: _AnyValF,
        c: _ArrayLikeCoef_co,
        /,
        *args: _AnyObjectPoints,
    ) -> _ObjectArray: ...

@final
class _FuncVander(_Named[_Name_co], Protocol[_Name_co]):
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        x: _ArrayLikeFloat_co,
        deg: SupportsIndex,
    ) -> _FloatArray: ...
    @overload
    def __call__(
        self, /,
        x: _ArrayLikeComplex_co,
        deg: SupportsIndex,
    ) -> _ComplexArray: ...
    @overload
    def __call__(
        self, /,
        x: _ArrayLikeCoef_co,
        deg: SupportsIndex,
    ) -> _ObjectArray: ...
    @overload
    def __call__(
        self, /,
        x: npt.ArrayLike,
        deg: SupportsIndex,
    ) -> _CoefArray: ...

_AnyDegrees: TypeAlias = Sequence[SupportsIndex]

@final
class _FuncVander2D(_Named[_Name_co], Protocol[_Name_co]):
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        x: _ArrayLikeFloat_co,
        y: _ArrayLikeFloat_co,
        deg: _AnyDegrees,
    ) -> _FloatArray: ...
    @overload
    def __call__(
        self, /,
        x: _ArrayLikeComplex_co,
        y: _ArrayLikeComplex_co,
        deg: _AnyDegrees,
    ) -> _ComplexArray: ...
    @overload
    def __call__(
        self, /,
        x: _ArrayLikeCoef_co,
        y: _ArrayLikeCoef_co,
        deg: _AnyDegrees,
    ) -> _ObjectArray: ...
    @overload
    def __call__(
        self, /,
        x: npt.ArrayLike,
        y: npt.ArrayLike,
        deg: _AnyDegrees,
    ) -> _CoefArray: ...

@final
class _FuncVander3D(_Named[_Name_co], Protocol[_Name_co]):
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        x: _ArrayLikeFloat_co,
        y: _ArrayLikeFloat_co,
        z: _ArrayLikeFloat_co,
        deg: _AnyDegrees,
    ) -> _FloatArray: ...
    @overload
    def __call__(
        self, /,
        x: _ArrayLikeComplex_co,
        y: _ArrayLikeComplex_co,
        z: _ArrayLikeComplex_co,
        deg: _AnyDegrees,
    ) -> _ComplexArray: ...
    @overload
    def __call__(
        self, /,
        x: _ArrayLikeCoef_co,
        y: _ArrayLikeCoef_co,
        z: _ArrayLikeCoef_co,
        deg: _AnyDegrees,
    ) -> _ObjectArray: ...
    @overload
    def __call__(
        self, /,
        x: npt.ArrayLike,
        y: npt.ArrayLike,
        z: npt.ArrayLike,
        deg: _AnyDegrees,
    ) -> _CoefArray: ...

# keep in sync with the broadest overload of `._FuncVander`
_AnyFuncVander: TypeAlias = Callable[
    [npt.ArrayLike, SupportsIndex],
    _CoefArray,
]

@final
class _FuncVanderND(_Named[_Name_co], Protocol[_Name_co]):
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        vander_fs: Sequence[_AnyFuncVander],
        points: Sequence[_ArrayLikeFloat_co],
        degrees: Sequence[SupportsIndex],
    ) -> _FloatArray: ...
    @overload
    def __call__(
        self, /,
        vander_fs: Sequence[_AnyFuncVander],
        points: Sequence[_ArrayLikeComplex_co],
        degrees: Sequence[SupportsIndex],
    ) -> _ComplexArray: ...
    @overload
    def __call__(
        self, /,
        vander_fs: Sequence[_AnyFuncVander],
        points: Sequence[
            _ArrayLikeObject_co | _ArrayLikeComplex_co,
        ],
        degrees: Sequence[SupportsIndex],
    ) -> _ObjectArray: ...
    @overload
    def __call__(
        self, /,
        vander_fs: Sequence[_AnyFuncVander],
        points: Sequence[npt.ArrayLike],
        degrees: Sequence[SupportsIndex],
    ) -> _CoefArray: ...

@final
class _FuncFit(_Named[_Name_co], Protocol[_Name_co]):
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        x: _SeriesLikeFloat_co,
        y: _ArrayLikeFloat_co,
        deg: int | _SeriesLikeInt_co,
        rcond: None | float = ...,
        full: Literal[False] = ...,
        w: None | _SeriesLikeFloat_co = ...,
    ) -> _FloatArray: ...
    @overload
    def __call__(
        self, /,
        x: _SeriesLikeComplex_co,
        y: _ArrayLikeComplex_co,
        deg: int | _SeriesLikeInt_co,
        rcond: None | float = ...,
        full: Literal[False] = ...,
        w: None | _SeriesLikeFloat_co = ...,
    ) -> _ComplexArray: ...
    @overload
    def __call__(
        self, /,
        x: _SeriesLikeComplex_co,
        y: _ArrayLikeCoef_co,
        deg: int | _SeriesLikeInt_co,
        rcond: None | float = ...,
        full: Literal[False] = ...,
        w: None | _SeriesLikeFloat_co = ...,
    ) -> _ObjectArray: ...
    @overload
    def __call__(
        self,
        x: _SeriesLikeComplex_co,
        y: _ArrayLikeCoef_co,
        deg: int | _SeriesLikeInt_co,
        rcond: None | float,
        full: Literal[True],
        /,
        w: None | _SeriesLikeFloat_co = ...,
    ) -> tuple[_CoefArray, Sequence[np.inexact[Any] | np.int32]]: ...
    @overload
    def __call__(
        self, /,
        x: _SeriesLikeComplex_co,
        y: _ArrayLikeCoef_co,
        deg: int | _SeriesLikeInt_co,
        rcond: None | float = ...,
        *,
        full: Literal[True],
        w: None | _SeriesLikeFloat_co = ...,
    ) -> tuple[_CoefArray, Sequence[np.inexact[Any] | np.int32]]: ...

@final
class _FuncRoots(_Named[_Name_co], Protocol[_Name_co]):
    @property
    def __name__(self, /) -> _Name_co: ...

    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        c: _SeriesLikeFloat_co,
    ) -> _Series[np.float64]: ...
    @overload
    def __call__(
        self, /,
        c: _SeriesLikeComplex_co,
    ) -> _Series[np.complex128]: ...
    @overload
    def __call__(self, /, c: _SeriesLikeCoef_co) -> _ObjectSeries: ...


_Companion: TypeAlias = np.ndarray[tuple[int, int], np.dtype[_SCT]]

@final
class _FuncCompanion(_Named[_Name_co], Protocol[_Name_co]):
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        c: _SeriesLikeFloat_co,
    ) -> _Companion[np.float64]: ...
    @overload
    def __call__(
        self, /,
        c: _SeriesLikeComplex_co,
    ) -> _Companion[np.complex128]: ...
    @overload
    def __call__(self, /, c: _SeriesLikeCoef_co) -> _Companion[np.object_]: ...

@final
class _FuncGauss(_Named[_Name_co], Protocol[_Name_co]):
    def __call__(
        self, /,
        deg: SupportsIndex,
    ) -> _Tuple2[_Series[np.float64]]: ...

@final
class _FuncWeight(_Named[_Name_co], Protocol[_Name_co]):
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        c: _ArrayLikeFloat_co,
    ) -> npt.NDArray[np.float64]: ...
    @overload
    def __call__(
        self, /,
        c: _ArrayLikeComplex_co,
    ) -> npt.NDArray[np.complex128]: ...
    @overload
    def __call__(self, /, c: _ArrayLikeCoef_co) -> _ObjectArray: ...

_N_pts = TypeVar("_N_pts", bound=int)

@final
class _FuncPts(_Named[_Name_co], Protocol[_Name_co]):
    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        npts: _N_pts,
    ) -> np.ndarray[tuple[_N_pts], np.dtype[np.float64]]: ...
    @overload
    def __call__(self, /, npts: _AnyInt) -> _Series[np.float64]: ...
