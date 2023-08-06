.. -*- coding: utf-8 -*-

.. _bob.med.tb.predtojson:

========================================
 Converting predictions to JSON dataset
========================================

This guide explains how to convert radiological signs predictions from a model
into a JSON dataset. It can be used to create new versions of TB datasets
with the predicted radiological signs to be able to use a shallow model. 
We input predictions (CSV files) and output a dataset.json file.

Use the sub-command :ref:`predtojson
<bob.med.tb.cli.predtojson>` to create your JSON dataset file:

.. code-block:: sh

   $ bob tb predtojson -vv train train/predictions.csv test test/predictions.csv --output-folder=pred_to_json


.. include:: links.rst
