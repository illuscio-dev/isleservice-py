.. islelib documentation master file, created by
   sphinx-quickstart on Mon Oct  1 00:18:03 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Isleservice
===========

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Isleservice is Illuscio's python microservice template. It builds on top of the
`islelib`_ template for python libraries. This documentation will focus on the
differences between the two templates rather than re-iterating the base features
inherited from `islelib`_.

Table of Contents
=================

* :ref:`basic-usage`
* :ref:`setting-up`
* :ref:`writing`
* :ref:`deploying`

.. _basic-usage:

Basic Usage
===========

>>> python service
STARTING UP: isleservice
CURRENT PATH: /Users/.../isleservice-py/service
ROUTE MODULE FOUND: greet
ROUTE FOUND: /schema.yml
ROUTE FOUND: /docs
ROUTE FOUND: /greet
INFO: Started server process [41979]
INFO: Waiting for application startup.
INFO: Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)

Isleservice comes with a number of pre-built quality-of-life macros for developers so
they can code more and manage less, most of which are accessed through ``make``
commands.

.. _setting-up:

Setting up your Service
=======================

Setting up a service follows the same steps as setting up a library in ``islelib``
with a few small notes:

   * You service will inherit the name passed to ``make name``. The main package of your
     service will always be ``service`` do not change the package name, as some of the
     service framework relies on it.

.. _writing:

Writing Your Service
====================

Linting, Testing and Basic documentation are all handled identically to `islelib`_.

Services are based off of `spanreed`_ ``SpanApi`` objects. It is suggested you be
familiar with it and the libraries it is built to work with:

   * `responder`_
   * `grahamcracker`_
   * `marshamllow`_
   * `dataclasses`_
   * `typing`_

**Isleservice requires python 3.7 or later.**


Making an Objects module
------------------------

One of the listed dependencies of isleservice is ``isleservice-objects``. This is a
template for defining the model objects, schemas, and errors that the service requires.

It is suggested that these objects be written in a separate package, then imported, so
client programs can have access to your same model and error objects without having to
install the entire service (or without you having to make your service's code available
to those writing client applications or other services in your environment.)

You can import and add these objects to your service as needed in the
``./service/api.py`` file.

Creating Routes
---------------

Your service's routes should be declared as ``spanreed.SpanRoute`` class-views.
Routes must be placed in the ``./service/routes`` folder. All .py files in this folder
(and any sub-folders) are imported automatically when the service starts up, so by
decorating your routes accordingly, they are automatically added to the service at
runtime when it starts up.

Your service is ready to go!

API Documentation by RedDoc
---------------------------

In place of the normal documentation supplied by sphinx, `islelib`_ uses a plugin that
hijacks sphinx to build `redoc`_ API documentation. This will take effect once the
service has been named through ``make name``.

Please review `spanserver's`_ documentation to familiarize yourself with the way API
documentation through openapi is produced.

Type the following command into the terminal:

>>> make doc

The three-panel documentation schema will be built and embedded in the sphinx
documentation.

.. _deploying:

Deploying Your Service
======================

Service containers are built through `Azure Devops`_ just as islelib libraries are.
Azure Pipelines can be configured to use `Dockerhub`_ or any dockerhub-compatible API
(illuscio uses `Azure Container Registry`_).

On Azure define the following variables in a library-group, then link the group to your
service's pipeline:

   * **CONTAINER_REGISTRY_ID**: Your dockerhub/registry user ID
   * **CONTAINER_REGISTRY_PASSWORD**: Your dockerhub/registry user password
   * **CONTAINER_REGISTRY_URL**: Your dockerhub/registry base url

Azure will automatically build a new image of your service and update your registry with
it. It will add both tags for the latest version and update the ``latest`` tag to the
newest build.

.. warning::

   **SECURITY NOTE:** Dockerhub will default to a public repo when pushing a
   new service for the first time. To avoid this, create a private repo *before*
   executing your first build.

   The default for azure container registry is private, so no action needs to be taken
   before a build.

.. note::

   For more information on the Azure build process this template uses, see the
   `remote build pipeline templates repo`_.

Dockerfile Template
===================

The dockerfile included in this template uses a multi-stage build process, allowing
users to pass the following environmental variables in for the build:

   * **PIP_INDEX_URL**: First pypi index to use during pip install.
   * **PIP_EXTRA_INDEX_URL**: Second pypi index to use during pip install.

Because one or both of these variables may contain login information for private
indexes, they are used in the build container, which is then discarded. Services
are installed into a virtual environment, which is then copied to the output
container for the actual service to build.

The base image used for services in ``python:3.8-slim``, into which the required
dependencies for building wheels are added. After build, the entire virtual environment
is copied into our service container, and used to run the service.

.. web links:
.. _islelib: https://illuscio-dev-islelib-py.readthedocs-hosted.com/en/latest/
.. _responder: https://github.com/kennethreitz/responder
.. _typing: https://docs.python.org/3/library/typing.html
.. _dataclasses: https://docs.python.org/3/library/dataclasses.html
.. _Azure Devops: https://azure.microsoft.com/en-us/services/devops/
.. _grahamcracker:
.. _marshamllow: https://marshmallow.readthedocs.io/en/3.0/
.. _readthedocs: https://readthedocs.com/
.. _spanreed:
.. _sphinx: http://www.sphinx-doc.org/en/master/
.. _swagger: https://swagger.io/solutions/api-design/
.. _Dockerhub: https://hub.docker.com/
.. _Azure Container Registry: https://azure.microsoft.com/en-us/services/container-registry/
.. _redoc: https://github.com/Redocly/redoc
.. _spanserver's: https://illuscio-dev-spanreed-py.readthedocs-hosted.com/en/latest/
.. _remote build pipeline templates repo: https://github.com/illuscio-dev/azure-pipelines-templates
