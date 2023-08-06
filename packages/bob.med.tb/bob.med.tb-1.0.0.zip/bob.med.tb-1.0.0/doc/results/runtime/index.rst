.. -*- coding: utf-8 -*-

.. _bob.med.tb.results.runtime:

==============================================
 Models training runtime and memory footprint
==============================================

The Pasa and the Densenet models were trained on a machine equipped with an 11 
GB GeForce GTX 1080 Ti GPU, an 8-core processor, 48 GB of RAM and Debian 10. 
The Logistic Regression model was trained on a Macbook Pro with an 8-core 
processor, 32 GB of RAM and macOS Big Sur.

Pasa
----

- Training on MC: 2'000 epochs in 2.5 hours, ~2 GB of CPU memory, ~0.75 GB of GPU memory
- Training on MC-CH: 2'000 epochs in 17 hours, ~2 GB of CPU memory, ~0.75 GB of GPU memory
- Training on MC-CH-IN: 2'000 epochs in 16.5 hours, ~2 GB of CPU memory, ~0.75 GB of GPU memory

Densenet pretraining
--------------------
 
- Training on NIH CXR14: 10 epochs in 12 hours, ~7.2 GB of CPU memory, ~6.4 GB of GPU memory

Densenet fine-tuning
--------------------

- Training on MC: 300 epochs in 0.5 hours, ~2 GB of CPU memory, ~6.4 GB of GPU memory
- Training on MC-CH: 300 epochs in 2.5 hours, ~2 GB of CPU memory, ~6.4 GB of GPU memory
- Training on MC-CH-IN: 300 epochs in 3.5 hours, ~2 GB of CPU memory, ~6.4 GB of GPU memory

Logistic Regression
-------------------

- Training on MC: 100 epochs in a few seconds, ~17 GB of CPU memory
- Training on MC-CH: 100 epochs in a few seconds, ~17 GB of CPU memory
- Training on MC-CH-IN: 100 epochs in a few seconds, ~17 GB of CPU memory