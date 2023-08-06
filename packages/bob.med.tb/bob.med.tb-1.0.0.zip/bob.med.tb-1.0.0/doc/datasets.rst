.. -*- coding: utf-8 -*-

.. _bob.med.tb.datasets:

====================
 Supported Datasets
====================

Here is a list of currently supported datasets in this package, alongside 
notable properties.  Each dataset name is linked to the location where 
raw data can be downloaded.  The list of images in each split is available
in the source code.

Tuberculosis datasets
---------------------

The following datasets contain only the tuberculosis final diagnosis (0 or 1).
In addition to the splits presented in the following table, 10 folds 
(for cross-validation) randomly generated are available for these datasets.

.. list-table::

   * - Dataset
     - Reference
     - H x W
     - Samples
     - Training
     - Validation
     - Test
   * - Montgomery_
     - [MONTGOMERY-SHENZHEN-2014]_
     - 4020 x 4892
     - 138
     - 88
     - 22
     - 28
   * - Shenzhen_
     - [MONTGOMERY-SHENZHEN-2014]_
     - Varying
     - 662
     - 422
     - 107
     - 133
   * - Indian_
     - [INDIAN-2013]_
     - Varying
     - 155
     - 83
     - 20
     - 52

Tuberculosis + radiological findings dataset
--------------------------------------------

The following dataset contains both the tuberculosis final diagnosis (0 or 1)
and radiological findings.

.. list-table::

   * - Dataset
     - Reference
     - H x W
     - Samples
     - Train
     - Test
   * - PadChest_
     - [PADCHEST-2019]_
     - Varying
     - 160'861
     - 160'861
     - 0

Radiological findings datasets
------------------------------

The following dataset contains only the radiological findings without any
information about tuberculosis.

.. note::

   NIH CXR14 labels for training and validation sets are the relabeled
   versions done by the author of the CheXNeXt study [CHEXNEXT-2018]_.

.. list-table::

   * - Dataset
     - Reference
     - H x W
     - Samples
     - Training
     - Validation
     - Test
   * - NIH_CXR14_re_
     - [NIH-CXR14-2017]_
     - 1024 x 1024
     - 109'041
     - 98'637
     - 6'350
     - 4'054

HIV-Tuberculosis datasets
-------------------------

The following datasets contain only the tuberculosis final diagnosis (0 or 1)
and come from HIV infected patients.
10 folds (for cross-validation) randomly generated are available for these
datasets.

Please contact the authors of these datasets to have access to the data.

.. list-table::

   * - Dataset
     - Reference
     - H x W
     - Samples
   * - TB POC
     - [TB-POC-2018]_
     - 2048 x 2500
     - 407
   * - HIV TB
     - [HIV-TB-2019]_
     - 2048 x 2500
     - 243

.. include:: links.rst
