.. -*- coding: utf-8 -*-

.. _bob.med.tb.training:

==========
 Training
==========

Convolutional Neural Network (CNN)
----------------------------------

To train a new CNN, use the command-line interface (CLI) application ``bob
tb train``, available on your prompt.  To use this CLI, you must define the
input dataset that will be used to train the CNN, as well as the type of model
that will be trained.  You may issue ``bob tb train --help`` for a help
message containing more detailed instructions.

.. tip::

   We strongly advice training with a GPU (using ``--device="cuda:0"``).
   Depending on the available GPU memory you might have to adjust your batch
   size (``--batch``).

Examples
^^^^^^^^

To train Pasa CNN on the Montgomery dataset:

.. code-block:: sh

   $ bob tb train -vv pasa montgomery --batch-size=4 --epochs=150

To train DensenetRS CNN on the NIH CXR14 dataset:

.. code-block:: sh

   $ bob tb train -vv nih_cxr14 densenet_rs --batch-size=8 --epochs=10

Logistic regressor or shallow network
-------------------------------------

To train a logistic regressor or a shallow network, use the command-line 
interface (CLI) application ``bob tb train``, available on your prompt. To use 
this CLI, you must define the input dataset that will be used to train the 
model, as well as the type of model that will be trained.  
You may issue ``bob tb train --help`` for a help message containing more 
detailed instructions.

Examples
^^^^^^^^

To train a logistic regressor using predictions from DensenetForRS on the 
Montgomery dataset:

.. code-block:: sh

   $ bob tb train -vv logistic_regression montgomery_rs --batch-size=4 --epochs=20

To train Signs_to_TB using predictions from DensenetForRS on the Shenzhen 
dataset:

.. code-block:: sh

   $ bob tb train -vv signs_to_tb shenzhen_rs --batch-size=4 --epochs=20


