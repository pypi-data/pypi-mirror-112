mcconv
======

**(!) The library is under development.
Many of the features will be implemented on the first request!
`Request features here <https://eicweb.phy.anl.gov/monte_carlo/mcconv/-/issues>`_ (!)**

Converter of MCEG  files from old EIC generators to HEPMC.

Provides command line interface (CLI) and python API to convert old (and not old) event
generators mainly used for EIC to HepMC.

**CLI supported types** (out of the box):

- LUND (vanilla pythia6)
- LUND GEMC (various generators especially from Clas12)
- Pythia6 RadCor (aka Pythia-EIC, Pythia6-BNL, Pythia6-HERMES)
- Beagle
- Eic-smear (aka Eic-tree)

**Python API supported types**

- Any type of text event+particles formats
- Eic-smear (aka Eic-tree)

Get started
~~~~~~~~~~~


.. code:: bash

    pip install mcconv
    mcconv my_file.txt

Will try to autodetect the type and produce my_file.hepmc

Flags:

- -d, --debug - Enable debugging output. More than verbose")
- -v, --verbose - Enable verbose output. Info level")
- -i, --in-type - Input file type: [auto, pythia6-bnl, ...]
- -f, --format - HepMC format [2,3]
- -o, --output - "File name of resulting hepmc (default ouptut.hepmc)
- -s, --nskip - Number of events to skip
- -p, --nprocess - Number of events to process

Flat vs topologic convert
------------------------

There are two conversion methods: **flat** and **topologic** convert.

HepMC assumes event as a graph of vertexes and particles. For example:

.. code::
                          p7
    p1                   /
      \v1__p3      p5---v4
            \_v3_/       \
            /    \        p8
       v2__p4     \
      /            p6
    p2

**flat** conversion just uses final state particle 4 vectors and put them
into a single hepmc vertex. One can add particle and event level attributes
(like true x and Q2, polarization, etc).

This method is the fastest and the only needed method for a further processing
with DD4Hep or Delphes.


**topologic** conversion (IS NOT IMPLEMENTED and will be implemented on the first
requiest or in some future) - tries to convert all particles and build hepmc graph.



Python API
----------

Python API allows to:

1. Convert MC files (same as CLI)
3. Read MC files event by event (partially implemented)
2. Read MC files as Pandas arrays (in implementation)
4. Read MC files as Awkward arrays (planned)

Convert to HepMC
~~~~~~~~~~~~~~~~

.. code:: python

   hepmc_convert('input.root', 'ouput.hepmc',
                 input_type=McFileTypes.EIC_SMEAR,
                 hepmc_vers=3,
                 nprocess=100000)


Where McFileTypes is one of:

.. code:: python

    McFileTypes.UNKNOWN
    McFileTypes.BEAGLE
    McFileTypes.HEPMC2
    McFileTypes.HEPMC3
    McFileTypes.LUND
    McFileTypes.LUND_GEMC
    McFileTypes.PYTHIA6_EIC
    McFileTypes.EIC_SMEAR

If McFileTypes.UNKNOWN is provided, hepmc_convert tries to **autodetect** type.
One can also do it by autodetect function:

.. code:: python

    from mcconv import detect_mc_type

    mc_file_type = detect_mc_type('my_file.root')
