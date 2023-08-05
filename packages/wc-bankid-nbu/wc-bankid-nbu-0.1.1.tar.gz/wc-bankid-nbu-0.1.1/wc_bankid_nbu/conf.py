from dataclasses import dataclass
from pathlib import Path


__all__ = 'LIB_PATH', 'SignerSettings',

LIB_PATH = Path(__file__).parent


@dataclass
class SignerSettings:
    PRIVATE_KEY_PATH: str
    PRIVATE_KEY_PASS: str

    FILE_STORE_PATH: str = '/data/certificates'
    C_PATH: str = LIB_PATH / 'contrib' / 'eu_sign' / 'linux' / '64'
    MODULE: str = 'wc_bankid_nbu.contrib.eu_sign.EUSignCP'

    CERTIFICATES_SIGN_NAME: str = 'EU-5B63D88375D92018040000002E3D0000B1950000.cer'
    CERTIFICATES_DISTRIBUTION_NAME: str = 'EU-5B63D88375D92018040000002E3D0000B2950000.cer'
