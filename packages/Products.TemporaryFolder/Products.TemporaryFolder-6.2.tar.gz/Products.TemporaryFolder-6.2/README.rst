.. image:: https://github.com/zopefoundation/Products.TemporaryFolder/actions/workflows/tests.yml/badge.svg
        :target: https://github.com/zopefoundation/Products.TemporaryFolder/actions/workflows/tests.yml

.. image:: https://coveralls.io/repos/github/zopefoundation/Products.TemporaryFolder/badge.svg?branch=master
   :target: https://coveralls.io/github/zopefoundation/Products.TemporaryFolder?branch=master

.. image:: https://img.shields.io/pypi/v/Products.TemporaryFolder.svg
   :target: https://pypi.org/project/Products.TemporaryFolder/
   :alt: Current version on PyPI

.. image:: https://img.shields.io/pypi/pyversions/Products.TemporaryFolder.svg
   :target: https://pypi.org/project/Products.TemporaryFolder/
   :alt: Supported Python versions

Overview
========

Zope temporary storage / folder support.


Please note
-----------
Before release 5.2 of the ``tempstorage`` package sessioning configurations
using this temporary folder implementation were discouraged because the
temporary storage backend could lose data. This is no longer the case.

Don't forget to add or uncomment the temporary storage database definition
as shown below in your Zope configuration if you want to instantiate a
temporary folder. After a Zope restart, visit the Zope Management Interface
and select ZODB Mount Point from the list of addable items to activate the
temporary folder mount point::

  <zodb_db temporary>
      <temporarystorage>
        name Temporary database (for sessions)
      </temporarystorage>
      mount-point /temp_folder
      container-class Products.TemporaryFolder.TemporaryContainer
  </zodb_db>

When upgrading from version 5.3 to 6.0 and removing the ZODB Mount Point
configuration shown above from your Zope configuration you need to manually
delete the ``/temp_folder`` object in the ZMI before restarting your Zope
instance with version 6.0. If you see tracebacks
``ZConfig.ConfigurationError: No database configured for mount point at
/temp_folder`` after the upgrade, please reinstate the ``zodb_db temporary``
Zope configuration as shown above, restart Zope and manually delete
``/temp_folder``. Then remove the ``zodb_db temporary`` configuration and
restart Zope.
