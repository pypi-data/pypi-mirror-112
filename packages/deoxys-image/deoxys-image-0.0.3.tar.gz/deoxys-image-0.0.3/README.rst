============
deoxys-image
============


.. image:: https://readthedocs.org/projects/deoxys-image/badge/?version=latest
        :target: https://deoxys-image.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://travis-ci.com/huynhngoc/deoxys-image.svg
   :target: https://travis-ci.com/huynhngoc/deoxys-image

.. image:: https://coveralls.io/repos/github/huynhngoc/deoxys-image/badge.svg
   :target: https://coveralls.io/github/huynhngoc/deoxys-image

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black


Image transformation


* Free software: MIT license
* Documentation: https://deoxys-image.readthedocs.io.


Features
--------

Apply different image-processing functions to images:

* Affine Transformation: rotation, translation, scaling, flipping
* Point operation: increase/decrease brightness and contrast, add Gaussian noise
* Filter operation: Gaussian blur

Increase speed with multiprocessing by setting the following environment variables:

* On Windows: `set NUM_CPUS=4`
* On Linux: `export NUM_CPUS=4`

If the runtime environment does not have write-access to `/tmp/ray`, change the `RAY_ROOT` environment variable to another accessible path.
