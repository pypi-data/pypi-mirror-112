Deploy MedUX on a server
========================

This is tested on Ubuntu server 20.04.

Production environment
----------------------

Have a look at our install script. If you want to use nginx, and uvicorn/gunicorn on an Ubunu 20.04 LTS server, just execute

.. code-block:: bash

    curl https://gitlab.com/nerdocs/medux/medux/-/raw/master/scripts/install.sh | bash

This script should ask for a few things (your ``DOMAIN`` etc.) and takes care of setting up your complete environment on an Ubuntu server, including installing the necessary system packages, setting up the user, virtual python environment for MedUX and doing the Nginx config, using the following standard packages:

* Nginx
* Django + Uvicorn + Gunicorn
* PostgreSQL

It tries to be as "automagical" as possible and uses sensible defaults for ``SECRET_KEY`` and the database password, creating them randomly when needed.

Have a look at the script to see what it does.

However, if you want to use other options, like Apache, MySQL, or Daphne etc., you are free to do it in another way.

You can edit ``/etc/nginx/sites-available/medux.conf`` to your needs at the end, for e.g. setting up SSL.

