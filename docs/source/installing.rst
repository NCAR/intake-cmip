Installing
==========

You can install intake-cmip with ``pip``, ``conda``, or by installing from source.

Pip
---

Pip can be used to install intake-cmip::

   pip install intake-cmip

Conda
-----

To install the latest version of intake-cmip from the
`conda-forge <https://conda-forge.github.io/>`_ repository using
`conda <https://www.anaconda.com/downloads>`_::

    conda install -c conda-forge intake-cmip

Install from Source
-------------------

To install intake-cmip from source, clone the repository from `github
<https://github.com/NCAR/intake-cmip>`_::

    git clone https://github.com/NCAR/intake-cmip.git
    cd intake-cmip
    pip install .

You can also install directly from git master branch::

    pip install git+https://github.com/NCAR/intake-cmip


Test
----

Test intake-cmip with ``pytest``::

    git clone https://github.com/NCAR/intake-cmip.git
    cd intake-cmip
    pytest - v