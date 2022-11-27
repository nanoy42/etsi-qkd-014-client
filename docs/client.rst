QKD014Client
============

The complete API reference of the client can be found here : :class:`~etsi_qkd_014_client.client.QKD014Client`.

The :class:`~etsi_qkd_014_client.client.QKD014Client` is the main class that you will use with this module.

It is the one that implements the three main methods described in the specifications : 

* :func:`~etsi_qkd_014_client.client.QKD014Client.get_status`
* :func:`~etsi_qkd_014_client.client.QKD014Client.get_key`
* :func:`~etsi_qkd_014_client.client.QKD014Client.get_key_with_key_IDs`

Initialization of the client
----------------------------

To initiate the client you need 4 required parameters : 

* ``kme_hostname`` : ip address of url of the API;
* ``cert_path`` : the path of the certificate of the client, signed by the root client CA;
* ``key_path`` : the path of the key associated to the certificate;
* ``ca_path`` : the path of the root CA used to sign the server's certificates.

and 1 optional parameter 

* ``force_insecure`` : wether to verify or not the certificate of the server (if ``force_insecure`` is ``True``, the certificate of the server will not be checked).

The full documentation of this function is :func:`etsi_qkd_014_client.client.QKD014Client.__init__`

An example of initialization is given below : 

.. code-block:: python

  from etsi_qkd_014_client import QKD014Client

  client_alice = QKD014Client(
      kme_hostname = "192.168.10.101",
      cert_path = "clientCert.pem",
      key_path = "clientKey.pem",
      ca_path = "rootCA.pem",
      force_insecure = True
   )

that can also be called without the parameters name : 

.. code-block:: python

  from etsi_qkd_014_client import QKD014Client

  client_alice = QKD014Client(
    "192.168.10.101",
    "clientCert.pem",
    "clientKey.pem",
    "rootCA.pem",
    True
  )

Using the client
----------------

Return values of the client
---------------------------

If you use one of the three public methods, they will return a tuple composed of an int that is the response code and an instance a class inheriting from :class:`~etsi_qkd_014_client.data.QKD014Data` that is the response data.

Response code
^^^^^^^^^^^^^
The response code is the same as the `HTTP response codes <https://en.wikipedia.org/wiki/List_of_HTTP_status_codes>`_.

Only a fraction of them can be returned according to the specifications and here they are :

+------+----------------------+
| Code | Description          |
+======+======================+
| 200  | Success              |
+------+----------------------+
| 400  | Bad request format   |
+------+----------------------+
| 401  | Unauthorized         |
+------+----------------------+
| 503  | Error on server side |
+------+----------------------+

In general, the code 200 will then be returned with a Data class corresponding to what was requested, and if another code is returned, it usually comes from with a :class:`~etsi_qkd_014_client.data.DataError` instance, that may hold additionnal information on the error.

Data
^^^^

The main class :class:`~etsi_qkd_014_client.data.QKD014Data` is an abstract class from which inherits 6 classes :

* :class:`~etsi_qkd_014_client.data.DataStatus`;
* :class:`~etsi_qkd_014_client.data.DataKeyRequest`;
* :class:`~etsi_qkd_014_client.data.DataKey`;
* :class:`~etsi_qkd_014_client.data.DataKeyContainer`;
* :class:`~etsi_qkd_014_client.data.DataKeyIDs`;
* :class:`~etsi_qkd_014_client.data.DataError`.

The public methods will however return only one of the three following class :

* :class:`~etsi_qkd_014_client.data.DataStatus` for the :func:`~etsi_qkd_014_client.client.QKD014Client.get_status` method;
* :class:`~etsi_qkd_014_client.data.DataKeyContainer` for the :func:`~etsi_qkd_014_client.client.QKD014Client.get_key` and :func:`~etsi_qkd_014_client.client.QKD014Client.get_key_with_key_IDs` methods;
* :class:`~etsi_qkd_014_client.data.DataError` in case of an error while calling one of the three methods.

You will also, however, deal with the :class:`~etsi_qkd_014_client.data.DataKey` class since the :class:`~etsi_qkd_014_client.data.DataKeyContainer` instance will contain a list of those.

.. warning::
  The :class:`~etsi_qkd_014_client.data.DataKeyRequest` and :class:`~etsi_qkd_014_client.data.DataKeyIDs` are helping classes for the requests, and should not be used as such by the end user.

DataError
"""""""""

An instance of the :class:`~etsi_qkd_014_client.data.DataError` class is returned in case an error occurred during the request. As described in the specifications it holds two fields :

* :attr:`~etsi_qkd_014_client.data.DataError.message` that is the error message returned by the server;
* :attr:`~etsi_qkd_014_client.data.DataError.details` that is an optional list of key/value pairs (``dict``) containing additional information on the error.


.. note::
  It does not hold the response code, that is returned individually from the data.

DataStatus
""""""""""

An instance of the :class:`~etsi_qkd_014_client.data.DataStatus` class is returned in case of a successful request to :func:`~etsi_qkd_014_client.client.QKD014Client.get_status`. There are several attributes accessible :

* :attr:`~etsi_qkd_014_client.data.DataStatus.source_kme_id`: KME ID of the KME;
* :attr:`~etsi_qkd_014_client.data.DataStatus.target_kme_id`: KME ID of the target KME;
* :attr:`~etsi_qkd_014_client.data.DataStatus.master_sae_id`: SAE ID of the calling master SAE;
* :attr:`~etsi_qkd_014_client.data.DataStatus.slave_sae_id`: SAE ID of the specified slave SAE;
* :attr:`~etsi_qkd_014_client.data.DataStatus.key_size`: Default size of key the KME can deliver to the SAE (in bit);
* :attr:`~etsi_qkd_014_client.data.DataStatus.stored_key_count`: Number of stored keys KME can deliver to the SAE;
* :attr:`~etsi_qkd_014_client.data.DataStatus.max_key_count`: Maximum number of stored_key_count;
* :attr:`~etsi_qkd_014_client.data.DataStatus.max_key_per_request`: Maximum number of keys per request;
* :attr:`~etsi_qkd_014_client.data.DataStatus.max_key_size`: Maximum size of key the KME can deliver to the SAE (in bit);
* :attr:`~etsi_qkd_014_client.data.DataStatus.min_key_size`: Minimum size of key the KME can deliver to the SAE (in bit);
* :attr:`~etsi_qkd_014_client.data.DataStatus.max_sae_id_count`: Maximum number of additional_slave_sae_ids the KME allows. "0" when the KME does not support key multicast;
* :attr:`~etsi_qkd_014_client.data.DataStatus.status_extension`: (Option) for future use.

DataKeyContainer
""""""""""""""""

An instance of the :class:`~etsi_qkd_014_client.data.DataKeyContainer` class is returned in case of a successful request to :func:`~etsi_qkd_014_client.client.QKD014Client.get_key` or :func:`~etsi_qkd_014_client.client.QKD014Client.get_key_with_key_IDs`. There are several attributes accessible :

* :attr:`~etsi_qkd_014_client.data.DataKeyContainer.keys`: Array of keys. The number of keys is specified by the "number" parameter in "Get key". If not specified, the default number of keys is 1. Each element in this array is an instance of the class :class:`~etsi_qkd_014_client.data.DataKey`;
* :attr:`~etsi_qkd_014_client.data.DataKeyContainer.key_container_extension`: (Option) for future use.

DataKey
"""""""

Instances of :class:`~etsi_qkd_014_client.data.DataKey` are contained in the :attr:`~etsi_qkd_014_client.data.DataKeyContainer.keys` attribute of an instance of :class:`~etsi_qkd_014_client.data.DataKeyContainer`. There are several attributes accessible :

* :attr:`~etsi_qkd_014_client.data.DataKey.key_id`: ID of the key: UUID format (example: "550e8400-e29b-41d4-a716-446655440000");
* :attr:`~etsi_qkd_014_client.data.DataKey.key_id_extension`: (Option) for future use;
* :attr:`~etsi_qkd_014_client.data.DataKey.key`: Key data encoded by base64 [7]. The key size is specified by the "size" parameter in "Get key". If not specified, the "key_size" value in Status data model is used as the default size.
* :attr:`~etsi_qkd_014_client.data.DataKey.key_extension`: (Option) for future use.