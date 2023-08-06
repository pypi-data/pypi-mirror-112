import lightkurve as lk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import mundey
from pathlib import Path
ddir = str(Path(__file__).parent.parent.resolve() / 'notebooks/')+'/'

import pytest


def test_sirius():

	tpffile = ddir+'tess2018349182459-s0006-0000000322899250-0126-s_tp.fits'

	tpf = mundey.mundey.mundey_tpf(tpffile)

	tpf.calibrate(ddir=ddir) # do the entire thing

	assert (np.nansum(tpf.flux.value) - 41293316000.0) < 0.01 # very simple checksum! improve this long term