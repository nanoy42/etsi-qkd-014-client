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
Classes for the data structures
"""

import abc

ETSI_QKD_014_PROTOCOL_VERSION = "1.1.1"


class QKD014Data(abc.ABC):
    """
    Abstract data class for QKD014.
    """

    pass


class DataStatus(QKD014Data):
    """
    Class representing the response data of the get_status command.

    Args:
        data (dict): response of the get_status command in json format.

    Raises:
        Exception: if the data does not meet the QKD 014 specifications.
    """

    source_kme_id: str  #: KME ID of the KME.
    target_kme_id: str  #: KME ID of the target KME.
    master_sae_id: str  #: SAE ID of the calling master SAE.
    slave_sae_id: str  #: SAE ID of the specified slave SAE.
    key_size: int  #: Default size of key the KME can deliver to the SAE (in bit).
    stored_key_count: int  #: Number of stored keys KME can deliver to the SAE.
    max_key_count: int  #: Maximum number of stored_key_count.
    max_key_per_request: int  #: Maximum number of keys per request.
    max_key_size: int  #: Maximum size of key the KME can deliver to the SAE (in bit).
    min_key_size: int  #: Minimum size of key the KME can deliver to the SAE (in bit).
    max_sae_id_count: int  #: Maximum number of additional_slave_SAE_IDs the KME allows. "0" when the KME does not support key multicast.
    status_extension: object  #: (Option) for future use.

    def __init__(self, data: dict) -> None:
        """
        Init the instance.

        Args:
            data (dict): response of the get_status command in json format.

        Raises:
            Exception: if the data does not meet the QKD 014 specifications.
        """
        try:
            self.source_kme_id = data["source_KME_ID"]
            self.target_kme_id = data["target_KME_ID"]
            self.master_sae_id = data["master_SAE_ID"]
            self.slave_sae_id = data["slave_SAE_ID"]
            self.key_size = int(data["key_size"])
            self.stored_key_count = int(data["stored_key_count"])
            self.max_key_count = int(data["max_key_count"])
            self.max_key_per_request = int(data["max_key_per_request"])
            self.max_key_size = int(data["max_key_size"])
            self.min_key_size = int(data["min_key_size"])
            self.max_sae_id_count = int(data["max_SAE_ID_count"])
        except KeyError as exc:
            raise Exception(
                f"Data does not meet the ETSI QKD 014 specifications for Status Data (version {ETSI_QKD_014_PROTOCOL_VERSION})"
            ) from exc

    def __str__(self) -> str:
        """
        Return a string representation of the object.
        """
        return f"""
source_KME_ID : {self.source_kme_id}
target_KME_ID : {self.target_kme_id}
master_SAE_ID : {self.master_sae_id}
slave_SAE_ID : {self.slave_sae_id}
key_size : {self.key_size}
stored_key_count : {self.stored_key_count}
max_key_count : {self.max_key_count}
max_key_per_request : {self.max_key_per_request}
max_key_size : {self.max_key_size}
min_key_size : {self.min_key_size}
max_SAE_ID_count : {self.max_sae_id_count}
"""


class DataKeyRequest(QKD014Data):
    """Data class to generate the data request for the get key command."""

    number: int  #: (Option) Number of keys requested, default value is 1.
    size: int  #: (Option) Size of each key in bits, default value is defined as key_size in Status data format.
    additional_slave_sae_ids: list[
        str
    ]  #: (Option) Array of IDs of slave SAEs. It is used for specifying two or more slave SAEs to share identical keys. The maximum number of IDs is defined as max_SAE_ID_count in Status data format.
    extension_mandatory: list[
        dict
    ]  #: (Option) Array of extension parameters specified as name/value pairs that KME shall handle or return an error. Parameter values may be of any type, including objects.
    extension_optional: list[
        dict
    ]  #: (Option) Array of extension parameters specified as name/value pairs that KME may ignore. Parameter values may be of any type, including objects.

    def __init__(
        self,
        number: int = None,
        size: int = None,
        additional_slave_sae_ids: list[str] = None,
        extension_mandatory: dict = None,
        extension_optional: dict = None,
    ) -> None:
        """Init the data key request instance.

        Args:
            number (int, optional): Number of keys requested, server's default value is 1. Defaults to None.
            size (int, optional): Size of each key in bits, server's default value is defined as key_size in Status data format. Defaults to None.
            additional_slave_sae_ids (list[str], optional): Array of IDs of slave SAEs. It is used for specifying two or more slave SAEs to share identical keys. The maximum number of IDs is defined as max_sae_id_count in Status data format. Defaults to None.
            extension_mandatory (dict, optional): Array of extension parameters specified as name/value pairs that KME shall handle or return an error. Parameter values may be of any type, including objects. Defaults to None.
            extension_optional (dict, optional): Array of extension parameters specified as name/value pairs that KME may ignore. Parameter values may be of any type, including objects. Defaults to None.
        """
        self.number = number
        self.size = size
        self.additional_slave_sae_ids = additional_slave_sae_ids
        self.extension_mandatory = extension_mandatory
        self.extension_optional = extension_optional

    def json(self) -> dict:
        """Render the actual json object to use in the request

        Returns:
            json: JSON object as specified in the specifications.
        """
        data = {}
        if self.number:
            data["number"] = self.number

        if self.size:
            data["size"] = self.size

        if self.additional_slave_sae_ids:
            data["additional_slave_SAE_IDs"] = self.additional_slave_sae_ids

        if self.extension_mandatory:
            data["extension_mandatory"] = self.extension_mandatory

        if self.extension_optional:
            data["extension_optional"] = self.extension_optional

        return data

    def __str__(self) -> str:
        """String representation of the instance.

        Returns:
            str: String representation of the instance.
        """
        return f"""
Number : {self.number}
Size : {self.size}
Additional slave SAE IDs : {self.additional_slave_sae_ids}
Extension mandatory : {self.extension_mandatory}
Extension optional : {self.extension_optional}
"""


class DataKey(QKD014Data):
    """Data for a key.

    This is not formally defined in the ETSI QKD 014 specifications.
    """

    key_id: str  #: ID of the key: UUID format (example: "550e8400-e29b-41d4-a716-446655440000").
    key: str  #: Key data encoded by base64 [7]. The key size is specified by the "size" parameter in "Get key". If not specified, the "key_size" value in Status data model is used as the default size.
    key_id_extension: object  #: (Option) for future use
    key_extension: object  #: (Option) for future use.

    def __init__(
        self,
        key_id: str,
        key: str,
        key_id_extension: object = None,
        key_extension: object = None,
    ):
        """Init the instance

        Args:
            key_id (str): ID of the key: UUID format (example: "550e8400-e29b-41d4-a716-446655440000").
            key (str): Key data encoded by base64 [7]. The key size is specified by  the "size" parameter in "Get key". If not specified, the  "key_size" value in Status data model is used as the default size.
            key_id_extension (object, optional): For future use. Defaults to None.
        """
        self.key_id = key_id
        self.key = key
        self.key_id_extension = key_id_extension
        self.key_extension = key_extension

    def __str__(self) -> str:
        """String representation of the instance

        Returns:
            str: String representation of the instance.
        """
        res = ""
        res += f"Key id : {self.key_id}\n"
        res += f"Key : {self.key}\n"

        if self.key_id_extension:
            res += f"Key ID extension : {self.key_id_extension}\n"

        if self.key_extension:
            res += f"Key extension : {self.key_extension}\n"
        return res


class DataKeyContainer(QKD014Data):
    """
    Class representing the data response of the get key command.
    """

    keys: list[
        DataKey
    ]  #: Array of keys. The number of keys is specified by the "number" parameter in "Get key". If not specified, the default number of keys is 1.
    key_container_extension: object  #: (Option) for future use.

    def __init__(self, data: dict) -> None:
        """Init the instance

        Args:
            data (json): response of the get key command.

        Raises:
            Exception: if the data does not meet the specifications.
        """
        try:
            self.keys = []
            for key_data in data["keys"]:
                self.keys.append(
                    DataKey(
                        key_data["key_ID"],
                        key_data["key"],
                        key_data.get("key_ID_extension"),
                    )
                )
        except KeyError as exc:
            raise Exception(
                f"Data does not meet the ETSI QKD 014 specifications for Key Container Data (version {ETSI_QKD_014_PROTOCOL_VERSION})"
            ) from exc
        self.key_container_extension = data.get("key_container_extension")

    def __str__(self) -> str:
        """String representation of the instance

        Returns:
            str: string representation of the instance.
        """
        res = ""
        for key in self.keys:
            res += str(key)
            res += "\n"
        if self.key_container_extension:
            res += f"Key container extension : {self.key_container_extension}"
        return res


class DataKeyIDs(QKD014Data):

    """Data strucutre to use as request data for get key with key IDs."""

    key_IDS: list[str]
    key_ids_extension: object
    key_ids_extensions: list[object]

    def __init__(
        self,
        key_ids: list[str],
        key_ids_extensions: list[object] = None,
        key_ids_extension=None,
    ) -> None:
        """Init the instance.

        Args:
            key_ids (array of string): Array of IDs in UUID format (example: "550e8400-e29b-41d4-a716-446655440000")
            key_ids_extensions (array of objects, optional): For future use. Defaults to None.
            key_ids_extension (object, optional): For future use. Defaults to None.
        """
        self.key_ids = key_ids
        self.key_ids_extensions = key_ids_extensions
        self.key_ids_extension = key_ids_extension

    def json(self) -> dict:
        """Render the actual json object to use in the request.

        Returns:
            json: JSON object as specified in the specifications.
        """
        data = {}
        data["key_IDs"] = []
        for i, key_id in enumerate(self.key_ids):
            key_data = {}
            key_data["key_ID"] = key_id

            if self.key_ids_extensions:
                key_data["key_ID_extension"] = self.key_ids_extensions[i]

            data["key_IDs"].append(key_data)

        if self.key_ids_extension:
            data["key_IDs_extension"] = self.key_ids_extension

        return data

    def __str__(self) -> str:
        """String representation of the instance.

        Returns:
            str: String representation of the instance.
        """
        res = ""

        for i, key in enumerate(self.key_ids):
            res += f"Key ID : {key}"
            if self.key_ids_extensions:
                res += f"Key ID extension : {self.key_ids_extensions[i]}"
            res += "\n"

        if self.key_ids_extension:
            res += f"Key IDs extension : {self.key_ids_extension}"

        return res


class DataError(QKD014Data):
    """Data structures for error."""

    message: str  #: Error message
    details: list[
        dict
    ]  #: (Option) Array to supply additional detailed error information specified as name/value pairs. Values may be of any type, including objects.

    def __init__(self, data: dict) -> None:
        """Init the instance.

        Args:
            data (json): Data returned by the server in case of error.

        Raises:
            Exception: if the data does not meet the specifications.
        """
        try:
            self.message = data["message"]
        except KeyError as exc:
            raise Exception(
                f"Data does not meet the ETSI QKD 014 specifications for Error Data (version {ETSI_QKD_014_PROTOCOL_VERSION})"
            ) from exc
        self.details = None
        if "details" in data:
            self.details = data["details"]

    def __str__(self) -> str:
        """String representation of the instance.

        Returns:
            str: String representation of the instance.
        """
        return f"""
Message : {self.message}
Details : {self.details}
"""
