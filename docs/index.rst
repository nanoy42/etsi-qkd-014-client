Welcome to etsi_qkd_014_client's documentation!
===============================================

``etsi_qkd_014_client`` is a library that implements the `ETSI GS QKD 014 <https://www.etsi.org/deliver/etsi_gs/QKD/001_099/014/01.01.01_60/gs_qkd014v010101p.pdf>`_ specifications and easily allows you to interact with a QKD server implementing the server side of these specifications.

Here is an example for a simple key exchange using the client

.. code-block:: python

   from etsi_qkd_014_client import QKD014Client

   client_alice = QKD014Client(
      "192.168.10.101",
      "clientCert.pem",
      "clientKey.pem",
      "rootCA.pem",
      force_insecure=True
   )

   client_bob = QKD014Client(
      "192.168.10.106",
      "clientBobCert.pem",
      "clientBobKey.pem",
      "rootCA.pem",
      force_insecure=True
   )

   code, data = client_alice.get_key("SAEBOB") # By default, this request one key of 256 bits

   print(code) # 200

   print(data)

   # Key id : 8c3c8d07-4827-47b7-a61b-db9b95f01cb9
   # Key : H7prwEw/MNN8AcpMnSUyt2fIXguhofof3qLt2O9uc5U=

   if code == 200:
      key_id = data.keys[0].key_id
      key_alice = data.keys[0].key

      code, data = client_bob.get_key_with_key_IDs("SAEALICE", [key_id])

      print(code) # 200

      print(data)

      # Key id : 8c3c8d07-4827-47b7-a61b-db9b95f01cb9
      # Key : H7prwEw/MNN8AcpMnSUyt2fIXguhofof3qLt2O9uc5U=

      key_bob = data.keys[0].key

      print(key_alice == key_bob) # True

**Features**

* Connect to a QKD server, using a custom CA, key and cert;
* Retrieve status of the QKD server with the :func:`~etsi_qkd_014_client.client.QKD014Client.get_status` command;
* Retrieve a secure key using the :func:`~etsi_qkd_014_client.client.QKD014Client.get_key` command;
* Retrieve a secure key knowing the key's ID using the :func:`~etsi_qkd_014_client.client.QKD014Client.get_key_with_key_IDs` command.

.. toctree::
   :maxdepth: 2
   :caption: Quickstart guide

   installation
   quickstart
   client
   examples
   cli


.. toctree::
   :maxdepth: 2
   :caption: API reference guide

   api/client
   api/data
   api/cli

.. toctree::
   :maxdepth: 2
   :caption: Other

   contributing
   citation
   license