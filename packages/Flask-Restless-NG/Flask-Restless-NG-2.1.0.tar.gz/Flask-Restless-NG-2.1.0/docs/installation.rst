Downloading and installing Flask-Restless-NG
============================================

Flask-Restless can be downloaded from the `Python Package Index`_. The
development version can be downloaded from `GitHub`_. However, it is better to
install with ``pip`` (in a virtual environment provided by ``virtualenv``)::

    pip install Flask-Restless-NG

Flask-Restless supports Python 3.6+

Flask-Restless has the following dependencies (which will be automatically
installed if you use ``pip``):

* `Flask`_ version 0.10 or greater
* `SQLAlchemy`_ version 0.8 or greater
* `python-dateutil`_ version strictly greater than 2.2
* `Flask-SQLAlchemy`_, *only if* you want to define your models using Flask-SQLAlchemy

.. _Python Package Index: https://pypi.python.org/pypi/Flask-Restless
.. _GitHub: https://github.com/jfinkels/flask-restless
.. _Flask: http://flask.pocoo.org
.. _SQLAlchemy: https://sqlalchemy.org
.. _python-dateutil: http://labix.org/python-dateutil
.. _Flask-SQLAlchemy: https://packages.python.org/Flask-SQLAlchemy
