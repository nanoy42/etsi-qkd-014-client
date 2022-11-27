# Copyright (C) 2022 Yoann Piétri
# Copyright (C) 2022 LIP6 - Sorbonne Université
#
# etsi-qkd-14-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# etsi-qkd-14-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with etsi-qkd-14-client. If not, see <http://www.gnu.org/licenses/>.

"""
File holding the main class for the QKD 014 client.
"""
from typing import Tuple

import requests


from .data import (
    DataError,
    DataKeyContainer,
    DataKeyIDs,
    DataKeyRequest,
    DataStatus,
    QKD014Data,
)


class QKD014Client:
    """
    The main class.

    Client for the QKD 014 specifications.
    """

    def __init__(
        self,
        kme_hostname: str,
        cert_path: str,
        key_path: str,
        ca_path: str,
        force_insecure: bool = False,
    ) -> None:
        """Init the client.

        Args:
            kme_hostname (str): Hostname or IP address of the KME.
            cert_path (str): path of the certificate file for the client.
            key_path (str): path of the secret key associated to the certificate of the client.
            ca_path (str): path of the root CA that will be used to check the autenticity of the certificate of the server.
            force_insecure (bool, optional): If true, the client will not proceed to the authenticity verification of the server. Defaults to False.
        """
        self.kme_hostname = kme_hostname
        self.cert_path = cert_path
        self.key_path = key_path
        self.ca_path = ca_path
        self.force_insecure = force_insecure

    def _get(self, url: str) -> requests.Response:
        """An alias to make a GET request.

        This automatically sets the verify and cert arguments of the get command.

        Args:
            url (str): target URL

        Returns:
            requests.Response: the response of the request.
        """
        if self.force_insecure:
            verify = False
        else:
            verify = self.ca_path

        return requests.get(
            url, verify=verify, cert=(self.cert_path, self.key_path), timeout=10
        )

    def _post(self, url: str, data: dict) -> requests.Response:
        """An alias to make a POST request.

        This automatically sets the verify and cert arguments of the post command.

        Args:
            url (str): target URL.
            data (dict): data of the request.

        Returns:
            requests.Response: response of the request.
        """
        if self.force_insecure:
            verify = False
        else:
            verify = self.ca_path

        return requests.post(
            url,
            json=data,
            verify=verify,
            cert=(
                self.cert_path,
                self.key_path,
            ),
            timeout=10,
        )

    def get_status(self, slave_sae_id: str) -> Tuple[int, QKD014Data]:
        """Get status command.

        Args:
            slave_sae_id (str): URL-encoded SAE ID of slave SAE.

        Returns:
            (int, QKD014Data): The first is the response code (200, 400, 401, 503). The second is an instance of QKD014Data. In this case it may be DataStatus or DataError.
        """
        url = f"https://{self.kme_hostname}/api/v1/keys/{slave_sae_id}/status"
        response = self._get(url)

        if response.status_code != 200:
            return response.status_code, DataError(response.json())
        return 200, DataStatus(response.json())

    def get_key(
        self,
        slave_sae_id: str,
        number: int = None,
        size: int = None,
        additional_slave_sae_ids: list[str] = None,
        extension_mandatory: dict = None,
        extension_optional: dict = None,
    ) -> Tuple[int, QKD014Data]:
        """Get key command.

        This requires certain parameters. If all are unset, this will issue a simple GET command,
        meaning that the default values will be used on the server's side.

        Args:
            slave_SAE_ID (str): URL-encoded SAE ID of slave SAE
            number (int, optional): Number of keys requested, if None is given, server's default value is 1.. Defaults to None.
            size (int, optional): Size of each key in bits, if None is given, server's default value is defined as key_size in Status data format. Defaults to None.
            additional_slave_sae_ids (list[str], optional): Array of IDs of slave SAEs. It is used for specifying two or more slave SAEs to share identical keys. The maximum number of IDs is defined as max_sae_id_count in Status data format. Defaults to None.
            extension_mandatory (dict, optional): Array of extension parameters specified as name/value pairs that KME shall handle or return an error. Parameter values may be of any type, including objects. Defaults to None.
            extension_optional (dict, optional): Array of extension parameters specified as name/value pairs that KME may ignore. Parameter values may be of any type, including objects. Defaults to None.

        Returns:
            (int, QKD014Data): The first is the response code (200, 400, 401, 503). The second is an instance of QKD014Data. In this case it may be DataKeyContainer or DataError.
        """
        url = f"https://{self.kme_hostname}/api/v1/keys/{slave_sae_id}/enc_keys"
        if (
            number is None
            and size is None
            and additional_slave_sae_ids is None
            and extension_mandatory is None
            and extension_optional is None
        ):
            # In this case, we are the simplified version case and we can juste make a GET request
            response = self._get(url)
        else:
            # We need to create the data object and pass it to the post request
            data = DataKeyRequest(
                number,
                size,
                additional_slave_sae_ids,
                extension_mandatory,
                extension_optional,
            )
            response = self._post(url, data.json())

        if response.status_code != 200:
            return response.status_code, DataError(response.json())
        return 200, DataKeyContainer(response.json())

    def get_key_with_key_IDs(
        self,
        master_sae_id: str,
        key_ids: list[str],
        key_ids_extensions: list[object] = None,
        key_ids_extension: object = None,
    ) -> Tuple[int, QKD014Data]:
        """Get key with key IDs command.

        Args:
            master_sae_id (str): URL-encoded SAE ID of master SAE
            key_ids (list[str]): list of key IDs in the UUID format (example: "550e8400-e29b-41d4-a716-446655440000")
            key_ids_extensions (list[object], optional): Reserved for future use. Defaults to None.
            key_ids_extension (object, optional): Reserved for future use. Defaults to None.

        Returns:
            (int, QKD014Data): The first is the response code (200, 400, 401, 503). The second is an instance of QKD014Data. In this case it may be DataKeyContainer or DataError.
        """
        url = f"https://{self.kme_hostname}/api/v1/keys/{master_sae_id}/dec_keys"
        data = DataKeyIDs(key_ids, key_ids_extensions, key_ids_extension)

        response = self._post(url, data.json())

        if response.status_code != 200:
            return response.status_code, DataError(response.json())
        return 200, DataKeyContainer(response.json())

    def __str__(self) -> str:
        """String representation of the client.

        Returns:
            str: string representation of the client.
        """
        res = "QKD014Client\n"
        res += f"\t KME : {self.kme_hostname}\n"
        res += f"\t Client certificate : {self.cert_path}\n"
        res += f"\t Client key : {self.key_path}\n"
        res += f"\t Root CA for server : {self.ca_path}\n"
        res += f"\t Force insecure : {self.force_insecure}"
        return res
