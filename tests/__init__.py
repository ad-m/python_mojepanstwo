# -*- coding: utf-8 -*-
from vcr import VCR
import os

my_vcr = VCR(cassette_library_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),"cassette"),
             path_transformer=VCR.ensure_suffix('.yaml'))
