A full example
==============

Initiate client
###############

.. code-block:: python
    
    from etsi_qkd_014_client import QKD014Client

    client = QKD014Client(
        "192.168.10.101", # KME hosy
        "certificatesMatteo/encAlice/clientCert.pem", # Certificate of the client signed by client's CA
        "certificatesMatteo/encAlice/clientKey.pem", # Private key associated to to the certificate
        "certificatesMatteo/CA/rootCA.pem", # Server's root CA to verify the certificate of the server
        force_insecure=True # This will force non verification of the certificate of server
    )

    print(client)

    # QKD014Client
	#     KME : 192.168.10.101
	#     Client certificate : certificatesMatteo/encAlice/clientCert.pem
	#     Client key : certificatesMatteo/encAlice/clientKey.pem
	#     Root CA for server : certificatesMatteo/CA/rootCA.pem
	#     Force insecure : True



Get status
##########

.. code-block:: python
    
    from etsi_qkd_014_client import QKD014Client

    client = QKD014Client(
        "192.168.10.101",
        "certificatesMatteo/encAlice/clientCert.pem",
        "certificatesMatteo/encAlice/clientKey.pem",
        "certificatesMatteo/CA/rootCA.pem",
        force_insecure=True
    )

    code, data = client.get_status("SAEBOB")

    print(code) # 200

    print(data)

    # source_kme_id : KMSALICE
    # target_kme_id : KMSBOB
    # master_sae_id : SAEALICE
    # slave_sae_id : SAEBOB
    # key_size : 256
    # stored_key_count : 86
    # max_key_count : 100
    # max_key_per_request : 1
    # max_key_size : 256
    # min_key_size : 128
    # max_sae_id_count : 0


Key exchange
############

.. code-block:: python

    import base64
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

        print(key_alice) # H7prwEw/MNN8AcpMnSUyt2fIXguhofof3qLt2O9uc5U=

        print(f"".join(["{:08b}".format(x) for x in base64.b64decode(key_alice)]))

        # 0001111110111010011010111100000001001100001111110011000011010011011111000000000111001010010011001001110100100101001100101011011101100111110010000101111000001011101000011010000111111010000111111101111010100010111011011101100011101111011011100111001110010101