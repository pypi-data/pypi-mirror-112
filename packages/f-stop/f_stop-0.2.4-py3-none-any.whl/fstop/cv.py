from typing import Callable

import cv2 as cv
import numpy as np
from PIL import Image

from .parser import parser, get_var
from .objects import *

def _fromarray(arr: np.ndarray) -> Image.Image:
    return Image.fromarray(
        cv.cvtColor(
            arr, cv.COLOR_BGR2RGB
        )
    )

def cv_process(state: ParserState, img: str, operation: Callable, *args, **kwargs) -> np.ndarray:
    img = get_var(state, img)
    arr = operation(img.array, *args, **kwargs)
    if isinstance(arr, tuple):
        arr = arr[-1]
    img.array = arr
    img.image = _fromarray(arr)
    return arr

 
@parser.production('expr : CANNY variable number COMMA number')
@evaluate
def canny_st(state: ParserState, p: list) -> np.ndarray:
    return cv_process(state, p[1], cv.Canny, p[2](), p[4]())

 
@parser.production('expr : CVTCOLOR variable string')
@evaluate
def colorspace_convert(state: ParserState, p: list) -> np.ndarray:
    val = p[2]()
    mapping = getattr(cv, 
        (val if val.startswith('COLOR_') else 'COLOR_' + val).upper()
    )
    return cv_process(state, p[1], cv.cvtColor, mapping)

 
@parser.production('expr : NOT variable')
@evaluate
def bitwise_not(state: ParserState, p: list) -> np.ndarray:
    return cv_process(state, p[1], cv.bitwise_not)

 
@parser.production('expr : THRESHOLD variable number COMMA number string')
@evaluate
def threshold_st(state: ParserState, p: list) -> np.ndarray:
    return cv_process(state, p[1], cv.threshold, p[2](), p[4](), getattr(cv, p[5]().upper()))

 
@parser.production('expr : COLORMAP variable string')
@evaluate
def apply_color_map(state: ParserState, p: list) -> np.ndarray:
    val = p[2]()
    mapping = getattr(cv, 
        (val if val.startswith('COLORMAP_') else 'COLORMAP_' + val).upper()
    )
    return cv_process(state, p[1], cv.applyColorMap, mapping)

 
@parser.production('expr : variable INRANGE ntuple COMMA ntuple AS variable')
@evaluate
def inrange_st(state: ParserState, p: list) -> ImageRepr:
    img = get_var(state, p[0])
    arr = cv.inRange(
        img.array, 
        np.uint8(p[2]()), 
        np.uint8(p[4]()),
    )
    img = ImageRepr(_fromarray(arr))
    state.env[p[-1]] = img
    return img

 
@parser.production('expr : variable AND variable AS variable')
@evaluate
def bitwise_and(state: ParserState, p: list) -> ImageRepr:
    img, img2 = get_var(state, p[0]), get_var(state, p[2])
    arr = cv.bitwise_and(img.array, img2.array)
    img = ImageRepr(_fromarray(arr))
    state.env[p[-1]] = img
    return img

 
@parser.production('expr : variable OR variable AS variable')
@evaluate
def bitwise_or(state: ParserState, p: list) -> ImageRepr:
    img, img2 = get_var(state, p[0]), get_var(state, p[2])
    arr = cv.bitwise_or(img.array, img2.array)
    img = ImageRepr(_fromarray(arr))
    state.env[p[-1]] = img
    return img

 
@parser.production('expr : variable XOR variable AS variable')
@evaluate
def bitwise_xor(state: ParserState, p: list) -> ImageRepr:
    img, img2 = get_var(state, p[0]), get_var(state, p[2])
    arr = cv.bitwise_xor(img.array, img2.array)
    img = ImageRepr(_fromarray(arr))
    state.env[p[-1]] = img
    return img