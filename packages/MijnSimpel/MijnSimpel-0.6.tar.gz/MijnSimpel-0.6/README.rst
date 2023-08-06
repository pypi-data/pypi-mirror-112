Mijn Simpel (Python) Client
===========================

Access `mijn.simpel.nl`_ from Python and command line.

.. _mijn.simpel.nl: https://mijn.simpel.nl


Supported API / resources
-------------------------

  =============================  ===================================
  Command                        Description
  =============================  ===================================
  subscriptions                  List subscriptions.
  cdrs                           Show cdrs.
  ceiling                        Show ceiling.
  correction-for-billing-period  Show correction for billing period.
  dashboard                      Show dashboard.
  latest-invoice                 Show latest invoice.
  other-costs                    Show other costs.
  products                       Show products.
  usage-summary                  Show usage summary.
  =============================  ===================================
  
  
Installation
------------

This will install the cli and the Python module ``mijn_simpel``::

    pip install .


Using CLI
---------

The cli goes with a *--help*, so try::

    mijn-simpel --help

It also recognize these environment variables:

* *MIJN_SIMPEL_USERNAME*
* *MIJN_SIMPEL_PASSWORD*
* *MIJN_SIMPEL_SUBSCRIPTION_ID*
* *MIJN_SIMPEL_COOKIE_JAR*


Using in Python
---------------

Please check `mijn_simpel/cli.py`_ for the example.

.. _mijn_simpel/cli.py: mijn_simpel/cli.py


Hacking
-------

Try installing with::

    pip install -e .

And then you can modify the source code and use it right away.
