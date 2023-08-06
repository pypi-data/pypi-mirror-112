Change Log
==========

..
   All enhancements and patches to eox_audit_model will be documented
   in this file.  It adheres to the structure of http://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).
   
   This project adheres to Semantic Versioning (http://semver.org/).
.. There should always be an "Unreleased" section for changes pending release.
Unreleased
----------

[0.5.0] - 2021-07-08
--------------------

Added
-----

* Display date in admin list view and use date format with ms
* Include an API wrapper to be used in API views to record the request data.
  Add an option to record sensitive data without the actual value.

[0.4.0] - 2021-05-24
--------------------

Added
_______

* Added support for django-ipware 3.0.0 .


[0.3.1] - 2021-05-18
--------------------

Fixed
_____

* Add missing parameters in celery task call.

[0.3.0] - 2021-04-29
--------------------

Change
______

* The model is created asynchronously in order to avoid atomic blocks.

[0.2.1] - 2020-12-28
--------------------

Fixed
_____

* Changes made in AuditModel.
* Added missing migration.

[0.2.0] - 2020-10-23
--------------------

Added
_______

* Added support for Django 2.2.

[0.1.0] - 2020-08-18
---------------------

Added
~~~~~

* First release on PyPI.
