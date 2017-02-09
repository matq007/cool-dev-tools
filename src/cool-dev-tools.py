#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Authors
# Martin Proks <martin.proks@outlook.com>

from __future__ import absolute_import
from __future__ import print_function

import sys

from src.lib.ArgParser import ArgParser

args = ArgParser(sys.argv)
args.parse()
