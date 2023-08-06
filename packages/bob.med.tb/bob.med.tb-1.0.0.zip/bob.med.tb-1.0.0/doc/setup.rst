.. -*- coding: utf-8 -*-
.. _bob.med.tb.setup:

=======
 Setup
=======

Complete Bob's `installation`_ instructions. Then, to install this package, do
this:

.. code-block:: sh

   $ conda activate <myenv>
   (<myenv>) $ conda install bob.med.tb

.. note::

   The value ``<myenv>`` should correspond to the name of the environment where
   you initially installed your Bob packages.


Datasets
--------

The package supports multiple chest X-ray datasets, but does not include
the raw data itself, which you must procure.

To setup a dataset, do the following:

1. Download the dataset from the authors website (see
   :ref:`bob.med.tb.datasets` for download links and details), unpack it and
   store the directory leading to the uncompressed directory structure.

   .. warning::

      Our dataset connectors expect you provide "root" paths of raw datasets as
      you unpack them in their **pristine** state.  Changing the location of
      files within a dataset distribution will likely cause execution errors.

2.  For each dataset that you are planning to use, set the ``datadir`` to the
    root path where it is stored.  E.g.:

    .. code-block:: sh

       (<myenv>) $ bob config set bob.med.tb.montgomery.datadir "/path/to/montgomery"

    To check supported raw datasets and your current setup, do the following:

    .. code-block:: sh

       (<myenv>) $ bob tb dataset list
       Supported datasets:
       - montgomery: bob.med.tb.montgomery.datadir = "/Users/yourname/work/bob/dbs/montgomery"
       * montgomery_RS: bob.med.tb.montgomery_RS.datadir (not set)
       - shenzhen: bob.med.tb.shenzhen.datadir = "/Users/yourname/work/bob/dbs/shenzhen"
       * shenzhen_RS: bob.med.tb.shenzhen_RS.datadir (not set)
       - indian: bob.med.tb.indian.datadir = "/Users/yourname/work/bob/dbs/indian"
       * indian_RS: bob.med.tb.indian_RS.datadir (not set)
       - nih_cxr14_re: bob.med.tb.nih_cxr14_re.datadir = "/Users/yourname/work/bob/dbs/NIH_CXR14"

    This command will show the set location for each configured dataset, and
    the variable names for each supported dataset which has not yet been setup.

    .. note::

      Tuberculosis datasets having radiological signs in place of images are
      recognizable by the "_RS" at the end of their name and do not need a
      location to be set.

3. To check whether the downloaded version is consistent with the structure
   that is expected by this package, run ``bob tb dataset check
   <dataset>``, where ``<dataset>`` should be replaced by the
   dataset programmatic name. E.g., to check Montgomery files, use:

   .. code-block:: sh

      (<myenv>) $ bob tb dataset check montgomery
      ...

   If there are problems on the current file organisation, this procedure
   should detect and highlight which files are missing (cannot be loaded).

.. include:: links.rst
