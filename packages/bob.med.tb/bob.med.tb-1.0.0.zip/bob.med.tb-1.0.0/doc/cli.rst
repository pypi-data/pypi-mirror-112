.. -*- coding: utf-8 -*-

.. _bob.med.tb.cli:

==============================
 Command-Line Interface (CLI)
==============================

This package provides a single entry point for all of its applications using
:ref:`Bob's unified CLI mechanism <bob.extension.cli>`.  A list of available
applications can be retrieved using:

.. command-output:: bob tb --help


Setup
-----

A CLI application to list and check installed (raw) datasets.

.. _bob.med.tb.cli.dataset:

.. command-output:: bob tb dataset --help


List available datasets
=======================

Lists supported and configured raw datasets.

.. _bob.med.tb.cli.dataset.list:

.. command-output:: bob tb dataset list --help


Check available datasets
========================

Checks if we can load all files listed for a given dataset (all subsets in all
protocols).

.. _bob.med.tb.cli.dataset.check:

.. command-output:: bob tb dataset check --help


Preset Configuration Resources
------------------------------

A CLI application allows one to list, inspect and copy available configuration
resources exported by this package.

.. _bob.med.tb.cli.config:

.. command-output:: bob tb config --help


.. _bob.med.tb.cli.config.list:

Listing Resources
=================

.. command-output:: bob tb config list --help


.. _bob.med.tb.cli.config.list.all:

Available Resources
===================

Here is a list of all resources currently exported.

.. command-output:: bob tb config list -v


.. _bob.med.tb.cli.config.describe:

Describing a Resource
=====================

.. command-output:: bob tb config describe --help


.. _bob.med.tb.cli.single:

Applications for experiments
----------------------------

These applications allow to run every step of the experiment cycle.  They also
work well with our preset :ref:`configuration resources
<bob.med.tb.cli.config.list.all>`.


.. _bob.med.tb.cli.train:

Training CNNs or shallow networks
=================================

Training creates of a new PyTorch_ model.  This model can be used for 
inference.

.. command-output:: bob tb train --help


.. _bob.med.tb.cli.predict:

Prediction with CNNs or shallow networks
========================================

Inference takes as input a PyTorch_ model and generates output probabilities.
The generated csv file indicates from 0 to 1 (floating-point number), 
the probability of TB presence on a chest X-ray, from less probable (0.0)
to more probable (1.0).

.. command-output:: bob tb predict --help

.. _bob.med.tb.cli.evaluate:

CNN Performance Evaluation
==========================

Evaluation takes inference results and compares it to ground-truth, generating
measure files and score tables which are useful to understand model performance.

.. command-output:: bob tb evaluate --help

.. _bob.med.tb.cli.compare:

Performance Comparison
======================

Performance comparison takes the prediction results and generate
combined figures and tables that compare results of multiple systems.

.. command-output:: bob tb compare --help

.. _bob.med.tb.cli.predtojson:

Converting predictions to JSON dataset
======================================

This script takes radiological signs predicted on a TB dataset and generate
a new JSON dataset from them.

.. command-output:: bob tb predtojson --help

.. _bob.med.tb.cli.aggregpred:

Aggregate multiple prediction files together
============================================

This script takes a list of prediction files and aggregate them into a single
file. This is particularly useful for cross-validation.

.. command-output:: bob tb aggregpred --help


.. include:: links.rst
