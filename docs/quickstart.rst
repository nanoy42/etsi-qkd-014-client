Quickstart
==========

Once the software is installed, you can get the status of your KME with : 

.. code-block:: python

    from etsi_qkd_014_client import QKD014Client

    client = QKD014Client(
      "192.168.1.1",
      "clientCert.pem",
      "clientKey.pem",
      "rootCA.pem",
      force_insecure=True
   )

   _, rep = client.get_status("SAEBOB")

   print(rep)


Then get a key with

.. code-block:: python

   _, rep = client.get_key("SAEBOB")

    print(rep.keys[0].key)
    key_id = rep.keys[0].key_id


and finally get the key on the other KME with

.. code-block:: python

    client_b = QKD014Client(
      "192.168.1.2",
      "clientBobCert.pem",
      "clientBobKey.pem",
      "rootCA.pem",
      force_insecure=True
   )

   _, rep = client_b.get_key_with_key_IDs("SAEALICE", [key_id])
   
   print(rep.keys[0].key)

If you want to know more, you can head to the next section that will go more in depth about the client.