.. -*- coding: utf-8 -*-

.. _bob.med.tb.results:

=========
 Results
=========

This section summarizes results that can be obtained with this package.

Models optimization
-------------------

In the link below, you will find information about the optimization of each
model we used.

.. toctree::
   :maxdepth: 2

   optimization/pasa/index
   optimization/densenet/index
   optimization/logreg/index
   optimization/signstotb/index

Models training runtime and memory footprint
--------------------------------------------

In the link below, you will find information about the training runtime and the
memory footprint of each model we used.

.. toctree::
   :maxdepth: 2

   runtime/index

AUROC Scores
------------

* Benchmark results for models: Pasa, DenseNet, SignsToTB
* Each dataset is split in a training, a validation and a testing subset
* Datasets names are abbreviated as follows: Montgomery (MC), Shenzhen (CH), 
  Indian (IN)
* Models are only trained on the training subset
* During the training session, we keep checkpoints for the best performing 
  networks based on the validation set.  The best performing network during 
  training is used for evaluation.
* Model resource configuration links are linked to the originating 
  configuration files used to obtain these results.

K-folding
^^^^^^^^^

Stratified k-folding has been used (10 folds) to generate these results.

.. tip::

   To generate the following results, you first need to predict TB on each 
   fold, then use the :ref:`aggregpred command <bob.med.tb.cli.aggregpred>` to 
   aggregate the predictions together, and finally evaluate this new file using 
   the :ref:`compare command <bob.med.tb.cli.compare>`.

Pasa and DenseNet-121 (random initialization)
"""""""""""""""""""""""""""""""""""""""""""""

Thresholds used:

* Pasa trained on MC, test on MC, mean threshold: 0.5057
* Pasa trained on MC-CH, test on MC-CH, mean threshold: 0.4966
* Pasa trained on MC-CH-IN, test on MC-CH-IN, mean threshold: 0.4135
* Densenet trained on MC, test on MC, mean threshold: 0.5183
* Densenet trained on MC-CH, test on MC-CH, mean threshold: 0.2555
* Densenet trained on MC-CH-IN, test on MC-CH-IN, mean threshold: 0.4037

.. list-table::

   * - AUC
     - MC test
     - CH test
     - IN test
   * - Pasa (train: MC)
     - 0.890
     - 0.576
     - 0.642
   * - Pasa (train: MC+CH)
     - 0.870
     - 0.893
     - 0.669
   * - Pasa (train: MC+CH+IN)
     - 0.881
     - 0.898
     - 0.848
   * - DenseNet-121 (train: MC)
     - 0.822
     - 0.607
     - 0.625
   * - DenseNet-121 (train: MC+CH)
     - 0.883
     - 0.905
     - 0.672
   * - DenseNet-121 (train: MC+CH+IN)
     - 0.860
     - 0.917
     - 0.850

.. list-table::

    * - .. figure:: img/compare_pasa_mc_kfold_500.jpg
           :align: center
           :scale: 50%
           :alt: Testing sets ROC curves for Pasa model trained on normalized-kfold MC

           :py:mod:`Pasa <bob.med.tb.configs.models.pasa>`: Pasa trained on normalized-kfold MC
      - .. figure:: img/compare_pasa_mc_ch_kfold_500.jpg
           :align: center
           :scale: 50%
           :alt: Testing sets ROC curves for Pasa model trained on normalized-kfold MC-CH

           :py:mod:`Pasa <bob.med.tb.configs.models.pasa>`: Pasa trained on normalized-kfold MC-CH
      - .. figure:: img/compare_pasa_mc_ch_in_kfold_500.jpg
           :align: center
           :scale: 50%
           :alt: Testing sets ROC curves for Pasa model trained on normalized-kfold MC-CH-IN

           :py:mod:`Pasa <bob.med.tb.configs.models.pasa>`: Pasa trained on normalized-kfold MC-CH-IN
    * - .. figure:: img/compare_densenet_mc_kfold_2000.jpg
           :align: center
           :scale: 50%
           :alt: Testing sets ROC curves for DenseNet model trained on normalized-kfold MC

           :py:mod:`DenseNet <bob.med.tb.configs.models.densenet>`: DenseNet trained on normalized-kfold MC
      - .. figure:: img/compare_densenet_mc_ch_kfold_2000.jpg
           :align: center
           :scale: 50%
           :alt: Testing sets ROC curves for DenseNet model trained on normalized-kfold MC-CH

           :py:mod:`DenseNet <bob.med.tb.configs.models.densenet>`: DenseNet trained on normalized-kfold MC-CH
      - .. figure:: img/compare_densenet_mc_ch_in_kfold_2000.jpg
           :align: center
           :scale: 50%
           :alt: Testing sets ROC curves for DenseNet model trained on normalized-kfold MC-CH-IN

           :py:mod:`DenseNet <bob.med.tb.configs.models.densenet>`: DenseNet trained on normalized-kfold MC-CH-IN

DenseNet-121 (pretrained on ImageNet)
"""""""""""""""""""""""""""""""""""""

Thresholds used:

* DenseNet (pretrained on ImageNet) trained on MC, test on MC, mean threshold: 0.3581
* DenseNet (pretrained on ImageNet) trained on MC-CH, test on MC-CH, mean threshold: 0.3319
* DenseNet (pretrained on ImageNet) trained on MC-CH-IN, test on MC-CH-IN, mean threshold: 0.4048

.. list-table::

   * - AUC
     - MC test
     - CH test
     - IN test
   * - DenseNet-121 (train: MC)
     - 0.910
     - 0.814
     - 0.817
   * - DenseNet-121 (train: MC+CH)
     - 0.948
     - 0.946
     - 0.816
   * - DenseNet-121 (train: MC+CH+IN)
     - 0.925
     - 0.944
     - 0.911

.. list-table::

    * - .. figure:: img/compare_densenetpreIN_mc_kfold_600.jpg
           :align: center
           :scale: 50%
           :alt: Testing sets ROC curves for DenseNet model trained on normalized-kfold MC

           :py:mod:`DenseNet <bob.med.tb.configs.models.densenet>` DenseNet trained on normalized-kfold MC
      - .. figure:: img/compare_densenetpreIN_mc_ch_kfold_600.jpg
           :align: center
           :scale: 50%
           :alt: Testing sets ROC curves for DenseNet model trained on normalized-kfold MC-CH

           :py:mod:`DenseNet <bob.med.tb.configs.models.densenet>` DenseNet trained on normalized-kfold MC-CH
      - .. figure:: img/compare_densenetpreIN_mc_ch_ch_kfold_600.jpg
           :align: center
           :scale: 50%
           :alt: Testing sets ROC curves for DenseNet model trained on normalized-kfold MC-CH-IN

           :py:mod:`DenseNet <bob.med.tb.configs.models.densenet>` DenseNet trained on normalized-kfold MC-CH-IN

Logistic Regression Classifier
""""""""""""""""""""""""""""""

Thresholds used:

* LogReg trained on MC, test on MC, mean threshold: 0.534
* LogReg trained on MC-CH, test on MC-CH, mean threshold: 0.2838
* LogReg trained on MC-CH-IN, test on MC-CH-IN, mean threshold: 0.2371

.. list-table::

   * - AUC
     - MC test
     - CH test
     - IN test
   * - Indirect (train: MC)
     - 0.966
     - 0.867
     - 0.926
   * - Indirect (train: MC+CH)
     - 0.961
     - 0.901
     - 0.928
   * - Indirect (train: MC+CH+IN)
     - 0.951
     - 0.895
     - 0.920

.. list-table::

    * - .. figure:: img/compare_logreg_mc_kfold_150.jpg
           :align: center
           :scale: 50%
           :alt: Testing sets ROC curves for LogReg model trained on normalized-kfold MC

           :py:mod:`LogReg <bob.med.tb.configs.models.logistic_regression>`: LogReg trained on normalized-kfold MC
      - .. figure:: img/compare_logreg_mc_ch_kfold_100.jpg
           :align: center
           :scale: 50%
           :alt: Testing sets ROC curves for LogReg model trained on normalized-kfold MC-CH

           :py:mod:`LogReg <bob.med.tb.configs.models.logistic_regression>`: LogReg trained on normalized-kfold MC-CH
      - .. figure:: img/compare_logreg_mc_ch_in_kfold_100.jpg
           :align: center
           :scale: 50%
           :alt: Testing sets ROC curves for LogReg model trained on normalized-kfold MC-CH-IN

           :py:mod:`LogReg <bob.med.tb.configs.models.logistic_regression>`: LogReg trained on normalized-kfold MC-CH-IN

DenseNet-121 (pretrained on ImageNet and NIH CXR14)
"""""""""""""""""""""""""""""""""""""""""""""""""""

Thresholds used:

* DenseNetPre trained on MC, test on MC, mean threshold: 0.4126
* DenseNetPre trained on MC-CH, test on MC-CH, mean threshold: 0.3711
* DenseNetPre trained on MC-CH-IN, test on MC-CH-IN, mean threshold: 0.4255

.. list-table::

   * - AUC
     - MC test
     - CH test
     - IN test
   * - DenseNet-121 (train: MC)
     - 0.966
     - 0.917
     - 0.901
   * - DenseNet-121 (train: MC+CH)
     - 0.984
     - 0.979
     - 0.869
   * - DenseNet-121 (train: MC+CH+IN)
     - 0.965
     - 0.978
     - 0.931

.. list-table::

    * - .. figure:: img/compare_densenetpre_mc_kfold_300.jpg
           :align: center
           :scale: 50%
           :alt: Testing sets ROC curves for DenseNet model trained on normalized-kfold MC (pretrained on NIH)

           :py:mod:`DenseNet <bob.med.tb.configs.models.densenet>`: DenseNet trained on normalized-kfold MC (pretrained on NIH)
      - .. figure:: img/compare_densenetpre_mc_ch_kfold_300.jpg
           :align: center
           :scale: 50%
           :alt: Testing sets ROC curves for DenseNet model trained on normalized-kfold MC-CH (pretrained on NIH)

           :py:mod:`DenseNet <bob.med.tb.configs.models.densenet>`: DenseNet trained on normalized-kfold MC-CH (pretrained on NIH)
      - .. figure:: img/compare_densenetpre_mc_ch_in_kfold_300.jpg
           :align: center
           :scale: 50%
           :alt: Testing sets ROC curves for DenseNet model trained on normalized-kfold MC-CH-IN (pretrained on NIH)

           :py:mod:`DenseNet <bob.med.tb.configs.models.densenet>`: DenseNet trained on normalized-kfold MC-CH-IN (pretrained on NIH)


Global sensitivity analysis (relevance)
---------------------------------------

Model used to generate the following figures: LogReg trained on MC-CH-IN fold 0 for 100 epochs.

.. tip::

   Use the ``--relevance-analysis`` argument of the :ref:`predict command
   <bob.med.tb.cli.predict>` to generate the following plots.

* Green color: likely TB
* Orange color: Could be TB
* Dark red color: Unlikely TB

As CH is the largest dataset, its relevance analysis is computed on more images
and is supposed to be more stable. Similarly, train sets are larger. 
We notice the systematic importance of Nodule, Pleural Thickening, Fibrosis, 
Mass, Consolidation and Pleural Effusion.

.. list-table::

    * - .. figure:: img/relevance_analysis/logreg_mc_ch_in_f0_100_mc_train.jpg
           :align: center
           :scale: 50%
           :alt: Relevance analysis on train MC

           Relevance analysis on train MC
      - .. figure:: img/relevance_analysis/logreg_mc_ch_in_f0_100_mc_validation.jpg
           :align: center
           :scale: 50%
           :alt: Relevance analysis on validation MC

           Relevance analysis on validation MC
      - .. figure:: img/relevance_analysis/logreg_mc_ch_in_f0_100_mc_test.jpg
           :align: center
           :scale: 50%
           :alt: Relevance analysis on test MC

           Relevance analysis on test MC
    * - .. figure:: img/relevance_analysis/logreg_mc_ch_in_f0_100_ch_train.jpg
           :align: center
           :scale: 50%
           :alt: Relevance analysis on train CH

           Relevance analysis on train CH
      - .. figure:: img/relevance_analysis/logreg_mc_ch_in_f0_100_ch_validation.jpg
           :align: center
           :scale: 50%
           :alt: Relevance analysis on validation CH

           Relevance analysis on validation CH
      - .. figure:: img/relevance_analysis/logreg_mc_ch_in_f0_100_ch_test.jpg
           :align: center
           :scale: 50%
           :alt: Relevance analysis on test CH

           Relevance analysis on test CH
    * - .. figure:: img/relevance_analysis/logreg_mc_ch_in_f0_100_in_train.jpg
           :align: center
           :scale: 50%
           :alt: Relevance analysis on train IN

           Relevance analysis on train IN
      - .. figure:: img/relevance_analysis/logreg_mc_ch_in_f0_100_in_validation.jpg
           :align: center
           :scale: 50%
           :alt: Relevance analysis on validation IN

           Relevance analysis on validation IN
      - .. figure:: img/relevance_analysis/logreg_mc_ch_in_f0_100_in_test.jpg
           :align: center
           :scale: 50%
           :alt: Relevance analysis on test IN

           Relevance analysis on test IN


Ablation study
--------------

Here, we removed the data of each sign, one after the other, from the dataset 
for both model training and prediction. LogReg trained on MC-CH-IN fold 0 for 
100 epochs has been used to generate the following plot.

Predictive capabilities of our logistic regression model after removing the 
data for each radiological sign (d0-d13 correspond, in this order, to 
cardiomegaly, emphysema, effusion, hernia, infiltration, mass, nodule, 
atelectasis, pneumothorax, pleural thickening, pneumonia, fibrosis, edema, and 
consolidation).

- .. figure:: img/rad_sign_drop.png
     :width: 400px

.. include:: ../links.rst
