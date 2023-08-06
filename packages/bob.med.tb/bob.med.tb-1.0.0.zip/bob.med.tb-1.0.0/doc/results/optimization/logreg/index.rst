.. -*- coding: utf-8 -*-

.. _bob.med.tb.results.optimization.logreg:

===========================
 LogReg model optimization
===========================

.. note::

   The Logistic Regression model contains 15 parameters.

LogReg is a logistic regression model created to predict TB presence based on 
the fourteen radiological signs predicted by the DensenetRS model. To train 
this model, we created new features for the Montgomery, Shenzhen and Indian 
dataset by predicting the presence of radiological signs on each of them with 
DensenetRS. Those new datasets versions can be identified by the _RS 
(for Radiological Signs) in their name.

To select the optimal learning rate and the optimal number of neurons for the 
LogReg model, we did a grid search with the following parameters.

- learning rate from 1e-1 to 1e-4
- batch size of 4, 8 and 16

We systematically used the training set of the combined dataset MC-CH-IN for
this optimization.

**The minimum validation loss we found is 0.3835 by using a learning rate of
1e-2 and a batch size of 4**

Minimum validation loss grid search
-----------------------------------

.. list-table::

   * - Learning rate
     - Batch size of 4
     - Batch size of 8
     - Batch size of 16
   * - 1e-1 (training for 50 epochs)
     - 0.3932
     - 0.4013
     - 0.4229
   * - 1e-2 (training for 100 epochs)
     - **0.3835**
     - 0.3998
     - 0.4126
   * - 1e-3 (training for 200 epochs)
     - 0.3875
     - 0.4075
     - 0.4188
   * - 1e-4 (training for 800 epochs)
     - 0.3942
     - 0.4059
     - 0.4123

Thresholds selection
--------------------

The threshold was systematically selected on the validation set of the datasets
on which the model was trained.

- Threshold for LogReg trained on MC: 0.568
- Threshold for LogReg trained on MC-CH: 0.372
- Threshold for LogReg trained on MC-CH-IN: 0.430

Other hyperparameters
^^^^^^^^^^^^^^^^^^^^^

The default Adam optimizer parameters were used: beta_1=0.9, beta_2=0.999, 
epsilon = 1e-8.