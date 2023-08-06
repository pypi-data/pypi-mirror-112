.. -*- coding: utf-8 -*-

.. _bob.med.tb.results.optimization.densenet:

=============================
 Densenet model optimization
=============================

.. note::

   The Densenet121 model contains 7'216'513 parameters.

Training on TB datasets from scratch
------------------------------------

To select the optimal learning rate and batch size for the training on the
TB datasets from scratch (densenet not pretrained), 
we did a grid search with the following parameters.

- learning rate of 1e-4, 5e-5 and 1e-5
- batch size of 4 and 8

We systematically used the training set of the combined dataset MC-CH-IN for
this optimization.

**The minimum validation loss we found is 0.3168 by using a learning rate of
5e-5 and a batch size of 8**

Minimum validation loss grid search
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This table indicates the minimum validation loss obtained for each combination
of learning rate and batch size.

.. list-table::

   * - Learning rate
     - Batch size of 4
     - Batch size of 8
   * - 1e-4 (training for 600 epochs)
     - 0.3658
     - 0.3676
   * - 5e-5 (training for 150 epochs)
     - 0.3490
     - **0.3168**
   * - 1e-5 (training for 1000 epochs)
     - 0.3791
     - 0.3831

Thresholds selection
^^^^^^^^^^^^^^^^^^^^

The threshold was systematically selected on the validation set of the datasets
on which the model was trained.

- Threshold for Densenet trained on MC: 0.599
- Threshold for Densenet trained on MC-CH: 0.519
- Threshold for Densenet trained on MC-CH-IN: 0.472

Pre-training on NIH CXR14
-------------------------

We used the pretrained Densenet121 model provided by PyTorch. For the 
pretraining on the NIH CXR14 dataset, the hyperparameters from the CheXNeXt 
study were used: batch size of 8, learning rate 1e-4 and the default Adam 
optimizer parameters: beta_1=0.9, beta_2=0.999, epsilon = 1e-8.

Fine-tuning on TB datasets
--------------------------

To select the optimal learning rate and batch size for the fine-tuning 
(after the pre-training on NIH CXR14), 
we did a grid search with the following parameters.

- learning rate of 1e-4, 1e-5, 5e-6, 1e-6
- batch size of 4, 8 and 16

We systematically used the training set of the combined dataset MC-CH-IN for
this optimization.

**The minimum validation loss we found is 0.1511 by using a learning rate of
1e-4 and a batch size of 8**

Minimum validation loss grid search
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This table indicates the minimum validation loss obtained for each combination
of learning rate and batch size.

.. list-table::

   * - Learning rate
     - Batch size of 4
     - Batch size of 8
     - Batch size of 16
   * - 1e-4 (training for 300 epochs)
     - 0.2053
     - **0.1511**
     - 0.2372
   * - 1e-5 (training for 500 epochs)
     - 0.1832
     - 0.1931
     - 0.2326
   * - 5e-6 (training for 300 epochs)
     - 0.1932
     - 0.2234
     - 0.2298
   * - 1e-6 (training for 600 epochs)
     - 0.2086
     - 0.2139
     - 0.2138

Thresholds selection
^^^^^^^^^^^^^^^^^^^^

The threshold was systematically selected on the validation set of the datasets
on which the model was trained.

- Threshold for Densenet trained on MC: 0.688
- Threshold for Densenet trained on MC-CH: 0.386
- Threshold for Densenet trained on MC-CH-IN: 0.432

Other hyperparameters
^^^^^^^^^^^^^^^^^^^^^

The default Adam optimizer parameters were used: beta_1=0.9, beta_2=0.999, 
epsilon = 1e-8.