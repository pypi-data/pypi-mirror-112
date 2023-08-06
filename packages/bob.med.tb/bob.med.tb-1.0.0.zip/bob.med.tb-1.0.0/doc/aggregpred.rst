.. -*- coding: utf-8 -*-

.. _bob.med.tb.aggregpred:

=======================================================
 Aggregate multiple prediction files into a single one
=======================================================

This guide explains how to aggregate multiple prediction files into a single
one. It can be used when doing cross-validation to aggregate the predictions of
k different models before evaluating the aggregated predictions. 
We input multiple prediction files (CSV files) and output a single one.

Use the sub-command :ref:`aggregpred
<bob.med.tb.cli.aggregpred>` aggregate your prediction files together:

.. code-block:: sh

   $ bob tb aggregpred -vv path/to/fold0/predictions.csv path/to/fold1/predictions.csv --output-folder=aggregpred


.. include:: links.rst
