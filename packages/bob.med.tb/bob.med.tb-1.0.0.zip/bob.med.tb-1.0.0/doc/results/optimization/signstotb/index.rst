.. -*- coding: utf-8 -*-

.. _bob.med.tb.results.optimization.signstotb:

==============================
 SignsToTB model optimization
==============================

.. note::

   The SignsToTB model contains 161 parameters.

SignsToTB is a shallow model created to predict TB presence based on the
fourteen radiological signs predicted by the DensenetRS model. To train this
model, we created new features for the Montgomery, Shenzhen and Indian dataset 
by predicting the presence of radiological signs on each of them with 
DensenetRS. Those new datasets versions can be identified by the _RS 
(for Radiological Signs) in their name.

To select the optimal learning rate and the optimal number of neurons for the 
SignsToTB model, we did a grid search with the following parameters.

- 2, 5, 10 and 14 neurons
- learning rate of 1e-2, 1e-3, 1e-4 and 1e-5
- batch size of 4
- 1'000 epochs

We systematically used the training set of the combined dataset MC-CH-IN for
this optimization.

**The minimum validation loss we found is 0.307 by using a learning rate of
1e-2 and 10 neurons.**

Minimum validation loss grid search
-----------------------------------

.. list-table::

   * - Learning rate
     - 2 neurons
     - 5 neurons
     - 10 neurons
     - 14 neurons
   * - 1e-2
     - 0.310
     - 0.314
     - **0.307**
     - 0.317
   * - 1e-3
     - 0.336
     - 0.315
     - 0.314
     - 0.317
   * - 1e-4
     - 0.341
     - 0.309
     - 0.321
     - 0.313
   * - 1e-5
     - 0.326
     - 0.357
     - 0.337
     - 0.323

Other hyperparameters
^^^^^^^^^^^^^^^^^^^^^

The default Adam optimizer parameters were used: beta_1=0.9, beta_2=0.999, 
epsilon = 1e-8.