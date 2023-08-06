.. _iris.common.resolve:

===================
iris.common.resolve
===================



.. currentmodule:: iris

.. automodule:: iris.common.resolve

In this module:

 * :py:obj:`Resolve`


At present, :class:`~iris.common.resolve.Resolve` is used by Iris solely
during cube maths to combine a left-hand :class:`~iris.cube.Cube`
operand and a right-hand :class:`~iris.cube.Cube` operand into a resultant
:class:`~iris.cube.Cube` with common metadata, suitably auto-transposed
dimensions, and an appropriate broadcast shape.

However, the capability and benefit provided by :class:`~iris.common.resolve.Resolve`
may be exercised as a general means to easily and consistently combine the metadata
of two :class:`~iris.cube.Cube` operands together into a single resultant
:class:`~iris.cube.Cube`. This is highlighted through the following use case
patterns.

Firstly, creating a ``resolver`` instance with *specific* :class:`~iris.cube.Cube`
operands, and then supplying ``data`` with suitable dimensionality and shape to
create the resultant resolved :class:`~iris.cube.Cube`, e.g.,

.. testsetup::

    import iris
    import numpy as np
    from iris.common import Resolve
    cube1 = iris.load_cube(iris.sample_data_path("A1B_north_america.nc"))
    cube2 = iris.load_cube(iris.sample_data_path("E1_north_america.nc"))[0]
    cube2.transpose()
    cube3, cube4 = cube1, cube2
    data = np.zeros(cube1.shape)
    data1 = data * 10
    data2 = data * 20
    data3 = data * 30

.. doctest::

    >>> print(cube1)
    air_temperature / (K)               (time: 240; latitude: 37; longitude: 49)
         Dimension coordinates:
              time                           x              -              -
              latitude                       -              x              -
              longitude                      -              -              x
         Auxiliary coordinates:
              forecast_period                x              -              -
         Scalar coordinates:
              forecast_reference_time: 1859-09-01 06:00:00
              height: 1.5 m
         Attributes:
              Conventions: CF-1.5
              Model scenario: A1B
              STASH: m01s03i236
              source: Data from Met Office Unified Model 6.05
         Cell methods:
              mean: time (6 hour)

    >>> print(cube2)
    air_temperature / (K)               (longitude: 49; latitude: 37)
         Dimension coordinates:
              longitude                           x             -
              latitude                            -             x
         Scalar coordinates:
              forecast_period: 10794 hours
              forecast_reference_time: 1859-09-01 06:00:00
              height: 1.5 m
              time: 1860-06-01 00:00:00, bound=(1859-12-01 00:00:00, 1860-12-01 00:00:00)
         Attributes:
              Conventions: CF-1.5
              Model scenario: E1
              STASH: m01s03i236
              source: Data from Met Office Unified Model 6.05
         Cell methods:
              mean: time (6 hour)

    >>> print(data.shape)
    (240, 37, 49)
    >>> resolver = Resolve(cube1, cube2)
    >>> result = resolver.cube(data)
    >>> print(result)
    air_temperature / (K)               (time: 240; latitude: 37; longitude: 49)
         Dimension coordinates:
              time                           x              -              -
              latitude                       -              x              -
              longitude                      -              -              x
         Auxiliary coordinates:
              forecast_period                x              -              -
         Scalar coordinates:
              forecast_reference_time: 1859-09-01 06:00:00
              height: 1.5 m
         Attributes:
              Conventions: CF-1.5
              STASH: m01s03i236
              source: Data from Met Office Unified Model 6.05
         Cell methods:
              mean: time (6 hour)

Secondly, creating an *empty* ``resolver`` instance, that may be called *multiple*
times with *different* :class:`~iris.cube.Cube` operands and *different* ``data``,
e.g.,

.. doctest::

    >>> resolver = Resolve()
    >>> result1 = resolver(cube1, cube2).cube(data1)
    >>> result2 = resolver(cube3, cube4).cube(data2)

Lastly, creating a ``resolver`` instance with *specific* :class:`~iris.cube.Cube`
operands, and then supply *different* ``data`` *multiple* times, e.g.,

    >>> payload = (data1, data2, data3)
    >>> resolver = Resolve(cube1, cube2)
    >>> results = [resolver.cube(data) for data in payload]

..

    .. autoclass:: iris.common.resolve.Resolve
        :members:
        :undoc-members:
        :inherited-members:

