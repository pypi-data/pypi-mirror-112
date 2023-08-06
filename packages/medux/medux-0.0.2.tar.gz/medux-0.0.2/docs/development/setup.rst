Setup MedUX for Development
===========================

For MedUX devel opment, you have to first setup the correct environment. As MedUX stands upon GDAPS' shoulders, and plugins can be distributed via PyPi and developed separately, there are a few caveats. This setup helps you through this process.

Make sure you have ``Python 3.6+``, ``pip`` and ``virtualenv`` installed.

Clone the MedUX repository:

.. code-block:: bash

    git clone git@gitlab.com:nerdocs/medux/medux.git
    cd medux

Create a virtualenv for Python:

.. code-block:: bash

    virtualenv .venv
    . ./venv/bin/activate

Install all the required dependencies now:

.. code-block:: bash

    pip install --upgrade pip
    pip install requirements/dev.txt
    python manage.py migrate
    python manage.py syncplugins

The script creates an ``admin`` user per default, password ``admin``.

Now create an ``.env`` file in the ``medux/medux`` directory. You can use the ``.env.example`` file there as a template, and set the variables according to your needs.

.. code-block:: bash

    python manage.py runserver

Happy coding...

If you want to create a plugin, have a look at the :ref:`Plugins` section