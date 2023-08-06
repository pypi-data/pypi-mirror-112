.. documentation master file, created by
   sphinx-quickstart on Fri Sep 25 10:54:55 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=============================================================================
Welcome to 'pathwalker' documentation!
=============================================================================

**pathwalker** is a micro module containing 2 helper methods for walking either
directories (:func:`pathwalker.walk_folder_paths`) or file paths
(:func:`pathwalker.walk_file_paths`) providing an additional filtering
by an unix filepath pattern.


.. image:: ../pathwalker-icon.svg
   :height: 196px
   :width: 196px
   :alt: A trash panda.
   :align: center

Installation
============

Install the latest release from pip.

.. code-block:: shell

   $ pip install pathwalker

.. toctree::
   :maxdepth: 3

   api_reference/index

Basic Usage
===========

Walk through folders only.

.. code-block:: python

     >>> from pathwalker import walk_folder_paths
     >>> for found_folder in walk_folder_paths(".", filter_pattern = "[!._]*"):
     ...    print(found_folder)
     docs
     tests


Walk through files only.

.. code-block:: python

     >>> from doctestprinter import doctest_iter_print
     >>> from pathwalker import walk_file_paths
     >>> found_files = sorted(
     ...     walk_file_paths(".", filter_pattern = "[!._]*.py", recursive=True),
     ...     key=lambda x: str(x)
     ... )
     >>> doctest_iter_print(found_files)
     docs/conf.py
     pathwalker.py
     setup.py
     tests/path_test.py



Indices and tables
==================

* :ref:`genindex`