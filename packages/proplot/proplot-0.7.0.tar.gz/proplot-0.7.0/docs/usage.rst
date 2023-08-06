.. _cartopy: https://scitools.org.uk/cartopy/docs/latest/

.. _basemap: https://matplotlib.org/basemap/index.html

.. _seaborn: https://seaborn.pydata.org

.. _pandas: https://pandas.pydata.org

.. _xarray: http://xarray.pydata.org/en/stable/

.. _usage:

=============
Using ProPlot
=============

This page offers a condensed overview of ProPlot's features. It is populated
with links to the :ref:`API reference` and :ref:`User Guide <ug_basics>`.
For a more in-depth discussion, see :ref:`Why ProPlot?`

.. _usage_background:

Background
==========

ProPlot is an object-oriented matplotlib wrapper. The "wrapper" part means
that ProPlot's features are largely a *superset* of matplotlib.  You can use
plotting commands like `~matplotlib.axes.Axes.plot`, `~matplotlib.axes.Axes.scatter`,
`~matplotlib.axes.Axes.contour`, and `~matplotlib.axes.Axes.pcolor` like you always
have. The "object-oriented" part means that ProPlot's features are implemented with
*subclasses* of the `~matplotlib.figure.Figure` and `~matplotlib.axes.Axes` classes.

If you tend to use `~matplotlib.pyplot` and are not familiar with figure and
axes *classes*, check out `this guide
<https://matplotlib.org/stable/api/index.html>`__
Directly working with objects tends to be more clear and concise than
`~matplotlib.pyplot`, makes things easier when working with multiple figures and axes,
and is certainly more "`pythonic <https://www.python.org/dev/peps/pep-0020/>`__".
Therefore, although some ProPlot features may still work, we do not officially support
the `~matplotlib.pyplot` interface.

.. _usage_import:

Importing proplot
=================

Importing ProPlot immediately adds several
new :ref:`colormaps <ug_cmaps>`, :ref:`property cycles <ug_cycles>`,
:ref:`color names <ug_colors>`, and :ref:`fonts <ug_fonts>` to matplotlib.
If you are only interested in these features, you may want to
import ProPlot at the top of your script and do nothing else!
We recommend importing ProPlot as follows:

.. code-block:: python

   import proplot as pplt

This differentiates ProPlot from the usual ``plt`` abbreviation reserved for
the `~matplotlib.pyplot` module. The abbreviation ``pplt`` is a popular
and less generic alternative.

.. _usage_classes:

Figure and axes classes
=======================

Creating plots with ProPlot always begins with a call to the
`~proplot.ui.subplots` command:

.. code-block:: python

   fig, axs = pplt.subplots(...)

The `~proplot.ui.subplots` command is modeled after
matplotlib's native `matplotlib.pyplot.subplots` command
and is :ref:`packed with new features <ug_subplots>`.

Instead of instances of the native `matplotlib.figure.Figure` and
`matplotlib.axes.Axes` classes, `~proplot.ui.subplots` :ref:`returns <ug_basics>`
a `proplot.figure.Figure` instance populated with `proplot.axes.Axes` instances.
ProPlot figures are saved with `~proplot.figure.Figure.save` (or, equivalently,
`~matplotlib.figure.Figure.savefig`). All ProPlot axes also belong
to one of the following three child classes:

* `proplot.axes.CartesianAxes`: For ordinary plots with *x* and *y*
  coordinates.
* `proplot.axes.GeoAxes`: For geographic plots with *longitude* and
  *latitude* coordinates.
* `proplot.axes.PolarAxes`: For polar plots with *radius* and *azimuth*
  coordinates.

Most of ProPlot's features are added via the `proplot.figure.Figure`
and `proplot.axes.Axes` classes. They include several brand new methods
and add new functionality to the *existing* methods.

* The new `~proplot.axes.Axes.format` method is used to fine-tune various
  axes settings.  Think of this as a dedicated
  `~matplotlib.artist.Artist.update` method for axes. See
  :ref:`formatting subplots <ug_format>` for a broad overview, along with the
  individual sections on formatting :ref:`Cartesian plots <ug_cartesian>`,
  :ref:`geographic plots <ug_geoformat>`, and :ref:`polar plots <ug_polar>`.
* The `proplot.axes.Axes.colorbar` and `proplot.axes.Axes.legend` commands
  draw colorbars and legends inside of subplots or along the outside edges of
  subplots. The `proplot.figure.Figure.colorbar` and `proplot.figure.Figure.legend`
  commands draw colorbars or legends along the edges of figures (aligned by
  subplot boundaries). These commands :ref:`simplify <ug_cbars_legends>`
  the process of drawing colorbars and legends.
* ProPlot adds a variety of useful features to the
  `~matplotlib.axes.Axes.plot`, `~matplotlib.axes.Axes.bar`,
  `~proplot.axes.Axes.area`, `~matplotlib.axes.Axes.contour`,
  `~matplotlib.axes.Axes.contourf`, `~matplotlib.axes.Axes.pcolormesh`,
  `~proplot.axes.Axes.heatmap`, and `~proplot.axes.Axes.parametric` plotting
  commands by "wrapping" them. See the :ref:`1D plotting <ug_1dplots>` and
  :ref:`2D plotting <ug_2dplots>` sections for details.

.. _usage_integration:

Integration features
====================

ProPlot includes *optional* integration features with four external
packages: the `pandas`_ and `xarray`_ packages, used for working with annotated
tables and arrays, and the `cartopy`_ and `basemap`_ geographic
plotting packages.

* If you pass a `pandas.Series`, `pandas.DataFrame`, or `xarray.DataArray`
  to any plotting command, the axis labels, tick labels, titles, colorbar
  labels, and legend labels are automatically applied from the metadata. If
  you did not supply the *x* and *y* coordinates, they are also inferred from
  the metadata. This works just like the native `xarray.DataArray.plot` and
  `pandas.DataFrame.plot` methods. A demonstration of this feature is given
  in the sections on :ref:`1D plotting <ug_1dintegration>` and
  :ref:`2D plotting <ug_2dintegration>`. This feature can be disabled by
  setting :rcraw:`autoformat` to ``False``.
* The `~proplot.axes.GeoAxes` class uses the `cartopy`_ or
  `basemap`_ packages to :ref:`plot geophysical data <ug_geoplot>`,
  :ref:`add geographic features <ug_geoformat>`, and
  :ref:`format projections <ug_geoformat>`. `~proplot.axes.GeoAxes` provides
  provides a simpler, cleaner interface than the original `cartopy`_ and `basemap`_
  interfaces. Figures can be filled with `~proplot.axes.GeoAxes` by passing the
  `proj` keyword to `~proplot.ui.subplots`.

Since these features are optional, ProPlot can be used without installing
any of these packages.

.. _usage_features:

Additional features
===================

Outside of the features provided by the `proplot.figure.Figure` and
`proplot.axes.Axes` subclasses, ProPlot includes several useful
classes and :ref:`constructor functions <why_constructor>`.

* The `~proplot.constructor.Colormap` and `~proplot.constructor.Cycle`
  constructor functions can be used to :ref:`slice <ug_cmaps_mod>`,
  and :ref:`merge <ug_cmaps_merge>` existing colormaps and color
  cycles. It can also :ref:`make new colormaps <ug_cmaps_new>`
  and :ref:`color cycles <ug_cycles_new>` from scratch.
* The `~proplot.colors.LinearSegmentedColormap` and
  `~proplot.colors.ListedColormap` subclasses replace the default matplotlib
  colormap classes and add several methods. The new
  `~proplot.colors.PerceptuallyUniformColormap` class is used to make
  colormaps with :ref:`perceptually uniform transitions <ug_perceptual>`.
* The `~proplot.demos.show_cmaps`, `~proplot.demos.show_cycles`,
  `~proplot.demos.show_colors`, `~proplot.demos.show_fonts`,
  `~proplot.demos.show_channels`, and `~proplot.demos.show_colorspaces`
  functions are used to visualize your :ref:`color scheme <ug_colors>`
  and :ref:`font options <ug_fonts>` and
  :ref:`inspect individual colormaps <ug_perceptual>`.
* The `~proplot.constructor.Norm` constructor function generates colormap
  normalizers from shorthand names. The new
  `~proplot.colors.LinearSegmentedNorm` normalizer scales colors evenly
  w.r.t. index for arbitrarily spaced monotonic levels, and the new
  `~proplot.colors.DiscreteNorm` meta-normalizer is used to
  :ref:`break up colormap colors into discrete levels <ug_discrete>`.
* The `~proplot.constructor.Locator`, `~proplot.constructor.Formatter`, and
  `~proplot.constructor.Scale` constructor functions return corresponding class
  instances from flexible input types. These are used to interpret keyword
  arguments passed to `~proplot.axes.Axes.format`, and can be used to quickly
  and easily modify :ref:`x and y axis settings <ug_cartesian>`.
* The `~proplot.config.rc` object, an instance of
  `~proplot.config.RcConfigurator`, is used for
  :ref:`modifying individual settings, changing settings in bulk, and
  temporarily changing settings in context blocks <ug_rc>`.
  It also introduces several :ref:`new setings <ug_config>`
  and sets up the inline plotting backend with `~proplot.config.inline_backend_fmt`
  so that your inline figures look the same as your saved figures.
