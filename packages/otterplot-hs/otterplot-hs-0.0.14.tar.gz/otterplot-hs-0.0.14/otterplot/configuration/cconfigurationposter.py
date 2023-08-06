# -*- coding: utf-8 -*-
r"""
This module contains the configuration class for the settings concerning figures in A0 posters.
"""
from matplotlib.pyplot import figure, axis
import otterplot.configuration.constants.keywords as keys
from typing import Union, Dict, Any, List
from otterplot.configuration.iconfiguration import IConfiguration
from otterplot.algorithm.converters import string_to_slice
from matplotlib.gridspec import GridSpec
import otterplot.configuration.constants.constants_poster as POSTER
from mpl_toolkits.mplot3d import Axes3D


class CConfigPoster(IConfiguration):
    r"""
    Configuration class for the settings concerning figures in A0 posters.
    """

    def __init__(self, options: Union[Dict[str, Any], None]) -> None:
        r"""
        Initializes the configuration and therefore the settings for the plot

        Args: options: A dictionary with key value pairs. These are options the user is allowed to configure within
        the API. The allowed keys are defined in configuration.constants.keywords.py.
        """
        super().__init__()
        self._options = options
        self._setupbasics()
        self._applytickoptions()

    def _setupbasics(self) -> None:
        r"""
        Calls the initialization of the figure, the gridspec and the axes in the correct order.
        """
        self._figure = self._initialize_figure()
        self._gs = self._initialize_gridspec()
        self._axes = self._initialize_axes()

    def _initialize_gridspec(self) -> GridSpec:
        r"""
        Initializes the GridSpec. The default subplot-grid has 1 column and 1 row.

        Returns:
            the gridspec
        """
        l_grid = self._options.get(keys.GRID, (1, 1))
        return GridSpec(ncols=l_grid[0], nrows=l_grid[1])

    def _initialize_axes(self) -> List[axis]:
        r"""
        Initializes the axis of the figure. The default is just one axis. Used for defining the axes-property, which is
        a list of axis. It is required to initialize the gridspec first. This method uses a lot of options:

        - If the parameter nonuniformax is not provided as matrix of axes of the same size is created for the grid
        defined. The parameter axes3D defines the index of the axes those shall be in 3d -projection mode.

        - If the parameter nonuniformax is provided (A list of tuples T for each tuple T =(stringslice,stringslice) repr.
        a string which can be converted into a slice for the row or column, respectively. If the parameter axes3D is
        provided some axis are presented in 3d projection mode

        Returns:
            A list of axis.
        """
        l_cols, l_rows = self._gs.get_geometry()
        axes3D = self._options.get(keys.AXES3D, None)
        nonuniformax = self._options.get(keys.NONUNIFORMAX, None)
        if nonuniformax is None:
            if axes3D is None:
                return [self._figure.add_subplot(self._gs[c, r]) for c in range(l_cols) for r in range(l_rows)]
            else:
                if isinstance(axes3D, list):
                    return [self._figure.add_subplot(self._gs[c, r],
                                                     projection='3d') if r + c in axes3D else self._figure.add_subplot(
                        self._gs[c, r]) for c in range(l_cols) for r in range(l_rows)]
                else:
                    raise ValueError("the 3d axis have to be provided as list of indices")
        else:
            if isinstance(nonuniformax, list):
                if axes3D is None:
                    return [self._figure.add_subplot(
                        self._gs[string_to_slice(slicetuple[0]), string_to_slice(slicetuple[1])]) for slicetuple in
                        nonuniformax]
                else:
                    l_axs = []
                    for (idx, slicetuple) in enumerate(nonuniformax):
                        if idx in axes3D:
                            print(slicetuple[0])
                            print(slicetuple[1])
                            l_axs.append(self._figure.add_subplot(
                                self._gs[string_to_slice(slicetuple[0]), string_to_slice(slicetuple[1])],
                                projection='3d'))
                        else:
                            l_axs.append(self._figure.add_subplot(
                                self._gs[string_to_slice(slicetuple[0]), string_to_slice(slicetuple[1])]))
                    return l_axs
            else:
                raise ValueError("the nonuniformax parameter has to be a list of tuples. Each tuple has to be"
                                 "a pair of strings representing a slice")

    def _initialize_figure(self) -> figure:
        r"""
        Initializes the figure. The effective width of a A0 poster, which can be used for content is 32.111 inch. If no
        further options are provided the figure will be of (8.02775,8.02775). If the option keys.FIGUREHEIGHT is given
        the figure will be of (8.02775,fig_height). If keys.EXTENTYPE is equal to keys.BROAD the output figure will have
        size (8.02775 * 2, fig_height) as a broad representation.
        """
        if self._options is None:
            return figure(figsize=(POSTER.FIGUREWIDTH_NARROW, POSTER.FIGUREWIDTH_NARROW))
        l_fig_width_fraction = self._options.get(keys.FRACTION, 4)
        # the height can be adjusted
        l_fig_height = self._options.get(keys.FIGUREHEIGHT, POSTER.FIGUREWIDTH_NARROW)
        l_extend = self._options.get(keys.EXTENTTYPE, keys.FULL)
        if l_extend == keys.FULL:
            return figure(figsize=(POSTER.MAXWIDTH / l_fig_width_fraction, l_fig_height))
        elif l_extend == keys.NARROW:
            return figure(figsize=(POSTER.FIGUREWIDTH_NARROW / l_fig_width_fraction, l_fig_height))
        elif l_extend == keys.BROAD:
            return figure(figsize=(POSTER.FIGUREWIDTH_BROAD / l_fig_width_fraction, l_fig_height))
        else:
            raise ValueError('not a valid key for extent')

    def _applytickoptions(self) -> None:
        r"""
        Applies options to the axis, including tick labelsize, tick length and width, the direction of the ticks.
        Per Default all axis are enabled
        """
        for ax in self._axes:
            ax.tick_params(axis='both',
                           which='major',
                           labelsize=POSTER.FONTSIZEMAJORTICKS,
                           length=POSTER.TICKLENGTH_MAJOR,
                           width=POSTER.TICKWIDTH_MAJOR,
                           direction=POSTER.TICKDIRECTION,
                           bottom=True,
                           top=True,
                           left=True,
                           right=True,
                           labelbottom=True,
                           labeltop=False,
                           labelleft=True,
                           labelright=False)

            ax.tick_params(axis='both',
                           which='minor',
                           direction=POSTER.TICKDIRECTION,
                           length=POSTER.TICKLENGTH_MINOR,
                           width=POSTER.TICKWIDTH_MINOR,
                           bottom=True,
                           top=True,
                           left=True,
                           right=True)

    @property
    def fontsize_labels(self) -> int:
        r"""
        Returns:
            The fontsize of the labels
        """
        return POSTER.FONTSIZEXYLABEL

    @property
    def axes(self) -> List[axis]:
        r"""
        Returns:
            A list of axis
        """
        return self._axes

    @property
    def figure(self) -> figure:
        r"""
        Returns:
             The figure for the plot.
        """
        return self._figure

    def __str__(self) -> str:
        r"""
        Returns:
             The string representation of the configuration object
        """
        return f"plotmode {keys.POSTER}"
