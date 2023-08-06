=====
Usage
=====

Basic Usages
------------

To use FEMAP neutral Parser in a project::

        >>> from femap_neutral_parser import Parser

To instantiate a new parser, just pass a filepath::

        >>> neutral = Parser("fea.NEU")

To have a list of available blocks::

        >>> neutral.available_blocks()
        {'header': 100, 'output_sets': 450, 'output_vectors': 451}

Or maybe in a more human-friendly way is to use `info()` method, which prints
available results and outputs::

        >>> neutral.info()
        Analysis
        ========
         * subcase 1: Analyse. NASTRAN SPC 1 - NASTRAN SPC 1 - NASTRAN SPC 1 - lc1. test (Static)
         * subcase 2: Analyse. NASTRAN SPC 1 - NASTRAN SPC 1 - NASTRAN SPC 1 - lc2. test (Static)

        Outputs
        =======
        access to one of them using `.output_vectors[<title>][<SubcaseID>]['record']

         * Total Translation
         * T1 Translation
         * T2 Translation
         * ...
         * Bar EndA Min Comb Stress
         * Bar EndB Min Comb Stress

Access available blocs by attribute::

        >>> neutral.output_sets
        {1: {'title': 'Analyse. NASTRAN SPC 1 - TTL - 9g FWD. test',
          'from_prog': 'Unknown',
          'anal_type': 'Static',
          'process_type': None,
          'integer_format': None,
          'value': 0.0,
          'notes': ''},
         2: {'title': 'Analyse. NASTRAN SPC 1 - TTL - 6.9g DOWN. test',
          'from_prog': 'Unknown',
          'anal_type': 'Static',
          'process_type': None,
          'integer_format': None,
          'value': 0.0,
          'notes': ''}}

Vectors for output (block451) are organized as nested dictionaries ``[<vector title>][<LCID>]``::

        >>> neutral.output_vectors["Total Translation"][2]
        {'vecID': 1,
         'min_val': 0.0,
         'max_val': 2.578386,
         'abs_max': 2.578386,
         'component_vec': [10002.0, 10003.0, 10004.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
         'id_min': 1,
         'id_max': 7,
         'calc_warn': True,
         'comp_dir': 1,
         'cent_total': True,
         'record': array([( 1, 0.000000e+00), ( 2, 2.045391e-01), ( 3, 0.000000e+00),
                ( 4, 1.468270e-02), ( 5, 9.231050e-05), ( 6, 6.276400e-01),
                ( 7, 2.578386e+00), ( 8, 1.025100e-01), ( 9, 2.578363e+00),
                (10, 1.100510e+00), (11, 1.916094e+00), (12, 2.389742e+00)],
               dtype=[('NodeID', '<i8'), ('Total Translation', '<f8')])}

To access the ``numpy.ndarray`` wrapping the actual values, just get the ``record`` key::

        >>> arr = neutral.output_vectors["Total Translation"][2]["record"]
        >>> arr
        array([( 1, 0.000000e+00), ( 2, 2.045391e-01), ( 3, 0.000000e+00),
               ( 4, 1.468270e-02), ( 5, 9.231050e-05), ( 6, 6.276400e-01),
               ( 7, 2.578386e+00), ( 8, 1.025100e-01), ( 9, 2.578363e+00),
               (10, 1.100510e+00), (11, 1.916094e+00), (12, 2.389742e+00)],
              dtype=[('NodeID', '<i8'), ('Total Translation', '<f8')])

which is actually a `structured numpy array <https://numpy.org/doc/stable/user/basics.rec.html>`_. This makes easier some processing or conversion to Pandas DataFrames (if Pandas is available)::

        >>> arr["NodeID"]
        array([ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12])
        >>> import pandas as pd
        >>> pd.DataFrame(arr).set_index("NodeID")
                Total Translation
        NodeID                   
        1                0.000000
        2                0.204539
        3                0.000000
        4                0.014683
        5                0.000092
        6                0.627640
        7                2.578386
        8                0.102510
        9                2.578363
        10               1.100510
        11               1.916094
        12               2.389742

Aggregated Outputs
------------------

An aggregated output is available using `Parser.vectors()` method. For example, to get all outputs for translations vectors::

        >>> arr = neutral.vectors(("T1 Translation", 
        ...                        "T2 Translation", 
        ...                        "T3 Translation"), 
        ...                       SubcaseIDs=None)
        >>> print(pd.DataFrame(arr).set_index(["SubcaseID", "NodeID"]))
                          T1 Translation  T2 Translation  T3 Translation
        SubcaseID NodeID                                                
        1         1             0.000000             0.0        0.000000
                  2            -0.187082             0.0        0.000000
                  3             0.000000             0.0        0.000000
                  4             0.070112             0.0        0.000000
                  5             0.000000             0.0       -0.005772
                  6             0.000000             0.0       -0.569351
                  7             0.000000             0.0       -1.299296
                  8            -0.093761             0.0       -0.005755
                  9             0.035551             0.0       -1.299279
                  10            0.000000             0.0       -0.956073
                  11            0.000000             0.0       -1.564502
                  12            0.000000             0.0       -1.602912
        2         1             0.000000             0.0        0.000000
                  2            -0.204539             0.0        0.000000
                  3             0.000000             0.0        0.000000
                  4            -0.014683             0.0        0.000000
                  5             0.000000             0.0       -0.000092
                  6             0.000000             0.0       -0.627640
                  7             0.000000             0.0       -2.578386
                  8            -0.102510             0.0       -0.000092
                  9            -0.007445             0.0       -2.578352
                  10            0.000000             0.0       -1.100510
                  11            0.000000             0.0       -1.916094
                  12            0.000000             0.0       -2.389742




