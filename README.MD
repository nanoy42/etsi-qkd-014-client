# etsi_qkd_014_client

The ETSI GS QKD 014 specification is a specification for communication between a client and a QKD module to retrieve cryptographic keys that have been exchanged using a Quantum Key Distribution protocol.

The specifications can be found at the following address : <https://www.etsi.org/deliver/etsi_gs/QKD/001_099/014/01.01.01_60/gs_qkd014v010101p.pdf>

The current version of the software uses the version V1.1.1 of the specifications (version from 2019-02).

## Features

* Connect to a QKD server, using a custom CA, key and cert;
* Retrieve status of the QKD server with the `get_status` command;
* Retrieve a secure key using the `get_key` command;
* Retrieve a secure key knowing the key's ID using the `get_key_with_key_IDs` command.
## Documentation

The full documentation can be found at https://etsi-qkd014-client.readthedocs.io/en/latest/.

## License

This software is distributed under the GNU Lesser General Public License v3 ([GNU LGPLv3](https://www.gnu.org/licenses/lgpl-3.0.en.html)). A copy of the complete text of the license is included with the software (the LICENSE file).

The header of the license can be found below :

> Copyright (C) 2022 Yoann Piétri
> Copyright (C) 2022 LIP6 - Sorbonne Université
>
> etsi-qkd-14-client is free software: you can redistribute it and/or modify
> it under the terms of the GNU Lesser General Public License as published > by
> the Free Software Foundation, either version 3 of the License, or
> (at your option) any later version.
>
> etsi-qkd-14-client is distributed in the hope that it will be useful,
> but WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
> GNU Lesser General Public License for more details.
>
> You should have received a copy of the GNU Lesser General Public License
> along with etsi-qkd-14-client. If not, see <http://www.gnu.org/licenses>.

## Citation

If you use this software, please consider citation. Here is the biblatex entry :

```latex
@software{etsi_qkd_014_client,
  author = {{Yoann Piétri}},
  title = {ETSI QKD 014 client},
  url = {https://github.com/nanoy42/etsi_qkd_014_client},
  version = {0.1.1},
  date = {2022-06-02},
}
```

If `@software` is not available, you can also use

```latex
@misc{etsi_qkd_014_client,
  author = {{Yoann Piétri}},
  title = {ETSI QKD 014 client},
  url = {https://github.com/nanoy42/etsi_qkd_014_client},
  date = {2022-06-02},
}
```

Plain text citation :

> Yoann Piétri. (2022). ETSI QKD 014 client (0.1.1) [Computer software]. <https://github.com/nanoy42/etsi_qkd_014_client>
