.. -*- coding: utf-8 -*-

.. _bob.med.tb.eval:

==========================
 Inference and Evaluation
==========================

This guides explains how to run inference or a complete evaluation using
command-line tools.  Inference produces probability of TB presence for input 
images, while evaluation will analyze such output against existing annotations 
and produce performance figures.


Inference
---------

In inference (or prediction) mode, we input data, the
trained model, and output a CSV file containing the prediction outputs for
every input image.

To run inference, use the sub-command :ref:`predict
<bob.med.tb.cli.predict>` to run prediction on an existing dataset:

.. code-block:: sh

   $ bob tb predict -vv <model> -w <path/to/model.pth> <dataset>


Replace ``<model>`` and ``<dataset>`` by the appropriate :ref:`configuration
files <bob.med.tb.configs>`.  Replace ``<path/to/model.pth>`` to a path
leading to the pre-trained model.

.. tip::

   An option to generate grad-CAMs is available for the 
   :py:mod:`DensenetRS <bob.med.tb.configs.models_datasets.densenet_rs>` model. 
   To activate it, use the ``--grad-cams`` argument.

.. tip::

   An option to generate a relevance analysis plot is available. 
   To activate it, use the ``--relevance-analysis`` argument.


Evaluation
----------

In evaluation, we input a dataset and predictions to generate
performance summaries that help analysis of a trained model.  Evaluation is
done using the :ref:`evaluate command <bob.med.tb.cli.evaluate>` followed
by the model and the annotated dataset configuration, and the path to the
pretrained weights via the ``--weight`` argument.

Use ``bob tb evaluate --help`` for more information.

E.g. run evaluation on predictions from the Montgomery set, do the following:

.. code-block:: bash

    bob tb evaluate -vv montgomery -p /predictions/folder -o /eval/results/folder


Comparing Systems
-----------------

To compare multiple systems together and generate combined plots and tables,
use the :ref:`compare command <bob.med.tb.cli.compare>`.  Use ``--help`` for
a quick guide.

.. code-block:: bash

   $ bob tb compare -vv A A/metrics.csv B B/metrics.csv --output-figure=plot.pdf --output-table=table.txt --threshold=0.5

.. include:: links.rst
