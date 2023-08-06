.. -*- coding: utf-8 -*-

.. _bob.med.tb.usage:

=======
 Usage
=======

This package supports a fully reproducible research experimentation cycle for
tuberculosis detection with support for the following activities.

.. figure:: img/direct_vs_indirect.png
   :width: 700px

Direct detection
----------------

* Training: Images are fed to a Convolutional Neural Network (CNN),
  that is trained to detect the presence of tuberculosis
  automatically, via error back propagation. The objective of this phase is to
  produce a CNN model.
* Inference (prediction): The CNN is used to generate TB predictions.
* Evaluation: Predications are used to evaluate CNN performance against 
  provided annotations, and to generate measure files and score tables. Optimal 
  thresholds are also calculated.
* Comparison: Use predictions results to compare performance of multiple 
  systems.

Indirect detection
------------------

* Training (step 1): Images are fed to a Convolutional Neural Network (CNN),
  that is trained to detect the presence of radiological signs
  automatically, via error back propagation. The objective of this phase is to
  produce a CNN model.
* Inference (prediction): The CNN is used to generate radiological signs 
  predictions.
* Conversion of the radiological signs predictions into a new dataset.
* Training (step 2): Radiological signs are fed to a shallow network, that is 
  trained to detect the presence of tuberculosis automatically, via error back 
  propagation. The objective of this phase is to produce a shallow model.
* Inference (prediction): The shallow model is used to generate TB predictions.
* Evaluation: Predications are used to evaluate CNN performance against
  provided annotations, and to generate measure files and score tables.
* Comparison: Use predictions results to compare performance of multiple 
  systems.

We provide :ref:`command-line interfaces (CLI)<bob.med.tb.cli.single>` that 
implement each of the phases above. This interface is configurable using
:ref:`Bob's extensible configuration framework <bob.extension.framework>`.  In
essence, each command-line option may be provided as a variable with the same
name in a Python file.  Each file may combine any number of variables that are
pertinent to an application.

.. tip::

   For reproducibility, we recommend you stick to configuration files when
   parameterizing our CLI. Notice some of the options in the CLI interface
   (e.g. ``--dataset``) cannot be passed via the actual command-line as it
   may require complex Python types that cannot be synthetized in a single
   input parameter.

We provide a number of :ref:`preset configuration files
<bob.med.tb.cli.config.list.all>` that can be used in one or more of the
activities described in this section.  Our command-line framework allows you to
refer to these preset configuration files using special names (a.k.a.
"resources"), that procure and load these for you automatically.

Scripts
-------

.. toctree::
   :maxdepth: 2

   training
   evaluation
   predtojson
   aggregpred


.. include:: links.rst
