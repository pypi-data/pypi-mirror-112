import os
import json
from base64 import b64decode, b64encode
from typing import Sequence, TYPE_CHECKING, Tuple
from functools import cached_property
from importlib import import_module
from contextlib import contextmanager
from pathlib import Path

from .exceptions import SignerNotLoaded, SignerPrivateKeyNotRead
from .conf import SignerSettings

if TYPE_CHECKING:
    from wc_bankid_nbu.contrib.eu_sign.EUSignCP import EU_INTERFACE


__all__ = 'update_env', 'Signer',


@contextmanager
def update_env(library_path: str):
    old = os.environ.get('LD_LIBRARY_PATH')
    os.environ['LD_LIBRARY_PATH'] = library_path

    yield

    os.environ['LD_LIBRARY_PATH'] = old


class Signer:
    settings: SignerSettings
    interface: 'EU_INTERFACE'
    loaded: bool
    _private_key_data: dict

    def __init__(self, settings: SignerSettings):
        self.settings = settings
        self.loaded = False
        self.interface = None

    @cached_property
    def module(self):
        return import_module(self.settings.MODULE)

    def env(self):
        return update_env(str(self.settings.C_PATH))

    def raise_for_unloaded(self):
        if not self.loaded:
            raise SignerNotLoaded()

    def configure(self):
        self.interface.SetFileStoreSettings({
            'szPath': self.settings.FILE_STORE_PATH,
            'bCheckCRLs': False,
            'bOwnCRLsOnly': True,
            'bAutoRefresh': False,
            'bFullAndDeltaCRLs': True,
            'bAutoDownloadCRLs': False,
            'bSaveLoadedCerts': True,
            'dwExpireTime': 3600,
        })

    def load(self):
        with self.env():
            self.module.EULoad()
            self.interface = self.module.EUGetInterface()

        self.interface.Initialize()
        self.configure()
        self.loaded = True

    def unload(self):
        with self.env():
            self.loaded = False
            self.interface.Finalize()
            self.module.EUUnload()

    @contextmanager
    def signer(self, unload: bool = True):
        if not self.loaded:
            self.load()

        yield self

        if unload:
            self.unload()

    def read_private_key(self):
        self.raise_for_unloaded()

        if self.interface.IsPrivateKeyReaded():
            return self._private_key_data

        with open(self.settings.PRIVATE_KEY_PATH, 'rb') as f:
            self._private_key_data = {}
            key = f.read()
            self.interface.ReadPrivateKeyBinary(
                key,
                len(key),
                self.settings.PRIVATE_KEY_PASS,
                self._private_key_data
            )

            if not self.interface.IsPrivateKeyReaded():
                raise SignerPrivateKeyNotRead()

        return self._private_key_data

    def _get_certificate(self, filename: str, b64: bool = False):
        with open(filename, 'rb') as f:
            data = f.read()

            if not b64:
                return data

            return b64encode(data).decode('ascii')

    def _fstore_path(self, name: str) -> str:
        return Path(self.settings.FILE_STORE_PATH) / name

    def get_distribution_certificate(self, b64: bool = False):
        return self._get_certificate(
            self._fstore_path(self.settings.CERTIFICATES_DISTRIBUTION_NAME),
            b64=b64,
        )

    def get_sign_certificate(self, b64: bool = False):
        return self._get_certificate(
            self._fstore_path(self.settings.CERTIFICATES_SIGN_NAME),
            b64=b64,
        )

    def decrypt(self, cert: str, encrypted: str) -> Tuple[dict, dict]:
        self.raise_for_unloaded()

        info = {}
        data: Sequence[bytes] = []
        result = []
        decoded = b64decode(encrypted)
        decoded_cert = b64decode(cert)

        self.interface.DevelopDataEx(
            encrypted, decoded, len(decoded), decoded_cert, len(decoded_cert),
            data, info
        )
        self.interface.VerifyDataInternal(
            b64encode(data[0]), data[0], len(data[0]),
            result, info
        )
        self.interface.GetDataFromSignedData(
            b64encode(data[0]), data[0], len(data[0]),
            result
        )

        return json.loads(result[0].decode()), info
