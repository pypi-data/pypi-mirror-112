# -*- coding: utf-8 -*-
r"""
This module contains the keywords for the factory pattern classes used in this project.
"""
# =======================Creating Plotmode===========================
PAPERPRB = 'paperPRB'
DEFAULTLATEX = 'defaultLatex'
PRESENTATION = 'presentation'
YAML = 'yaml'
POSTER = 'poster'
# =======================Specific Options for Plotmode===============

# Options for defining the Figure. The inputs are designed in a way that only figures within the allowed rules depending
# on the format can be created.
# -------------------------------------------------------------------
EXTENTTYPE = 'extent'
NARROW = 'narrow'
BROAD = 'broad'
TINY = 'tiny'
FULL = 'full'
# if this keyword is selected the figurewidth is a fraction of the defined maximum width. This is so far only imple-
# mented for poster class
FRACTION = 'fraction'
# figure height in inches, input type has to be float
FIGUREHEIGHT = 'figheight'
# -------------------------------------------------------------------
# Gridspec defines number of subplots with number of rows and number of columns data is provided as Tuple
GRID = 'grid'
# -------------------------------------------------------------------
# List of specific axes which shall be in 3D projection mode
AXES3D = 'axes3D'
# In default mode a grid of uniform axes will be created. Sometimes one wants to have one axis bigger than another.
# E.g. a plot and a colorbar
NONUNIFORMAX = 'nonuniformax'
