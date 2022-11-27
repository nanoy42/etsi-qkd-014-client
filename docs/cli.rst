Command Line Interface
======================

The package is shipped with a command line interface, that is used to test a QKD server implementing the QKD specifications. 

.. warning::

    This command line interface is intended for testing purposes only ! It should not be used for production.

Accessing the command line interface
------------------------------------

The command line can be accessed with the `cli.py` file and also with qkd014-client command line tool installed with the software.

Passing the required arguments
------------------------------

The required arguments, independently of which command is used, are : 

* hostname (of the server implementing the QKD 014 specifications);
* cert : certificate file path to use;
* key : private key path associated with the certificate;
* ca : the root CA path that signed the server's certificate;
* force : whether to force insecure connections or not.

These parameters can be given either directly with the command line or using a configuration file.

Through the command line
^^^^^^^^^^^^^^^^^^^^^^^^

Here is the way to give all the parameters : 

* hostname can be given with ``--hostname HOSTNAME`` or ``-H HOSTNAME``;
* cert can be given with ``--cert CERT`` or ``-c CERT``;
* key can be given with ``--key KEY`` or ``-k KEY``;
* ca can be given with ``--ca CA`` or ``-r CA``;
* by default force is false. You can set it to true with ``--force`` or ``-f``.


Through a configuration file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As an alternative to pass all those arguments on the command line, you can also create a configuration file that looks like

.. code-block:: ini

    [etsi_qkd_014_client]
    hostname = 192.168.1.1
    cert = cert.pem
    key = key.pem
    ca = ca.pem
    force = no 

Then you should call the script using the ``--config`` option::

    qkd014-client --config config.ini get_status

Precedence
^^^^^^^^^^

Configuration file takes priority over the command line arguments. That means that, for instance if the ``--config`` is given with a wrong configuration file, the script will raise an exception even if all the other parameters were given to the command line.

You cannot mix command line arguments and configuration file.

Commands
--------

There are 3 different subcommands :

* ``get_status`` command to get the status of the QKD server. This require the SAE ID of the slave SAE.
* ``get_key`` command to get one (or more) key(s). This require at least one additional parameter: the SAE ID of the slave SAE.
* ``get_key_with_ID`` command to get one (or more) key(s), knowing their ID. This require at least two additional parameters: the SAE ID of the slave SAE and the list of the ID(s) of the key(s).

Get status
^^^^^^^^^^

You can get the status of SAEBOB with::

    qkd014-client -H 192.168.10.101 -c clientCert.pem -k clientKey.pem -r rootCA.pem -f get_status SAEBOB

Get key
^^^^^^^

You can get a key with::

    qkd014-client -H 192.168.10.101 -c clientCert.pem -k clientKey.pem -r rootCA.pem -f get_key SAEBOB


Get key with ID
^^^^^^^^^^^^^^^

You can get a key with the ID with::

    qkd014-client -H 192.168.10.101 -c clientCert.pem -k clientKey.pem -r rootCA.pem -f get_key_with_id SAEALICE 8c3c8d07-4827-47b7-a61b-db9b95f01cb9
