.. -*- coding: utf-8 -*-

.. _bob.med.tb.results.optimization.pasa:

=========================
 Pasa model optimization
=========================

.. note::

   The Pasa model contains 201'905 parameters.

Model hyperparameters from the original study were used: batch size of 4, 
learning rate 8e-5 and the default Adam optimizer parameters: beta_1=0.9, 
beta_2=0.999, epsilon = 1e-8. The Pasa model has not been pretrained.

Thresholds selection
--------------------

The threshold was systematically selected on the validation set of the datasets
on which the model was trained.

- Threshold for Pasa trained on MC: 0.577
- Threshold for Pasa trained on MC-CH: 0.417
- Threshold for Pasa trained on MC-CH-IN: 0.235