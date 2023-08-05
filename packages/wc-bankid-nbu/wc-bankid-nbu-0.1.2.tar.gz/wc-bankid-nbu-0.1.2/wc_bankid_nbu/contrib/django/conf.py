from dataclasses import dataclass

from px_settings.contrib.django import settings as s
from wc_bankid_nbu import SignerSettings as SSBase


__all__ = (
    'SignerSettings',
    'signer_settings',
)


@s('WC_BANKID_NBU_SIGNER')
@dataclass
class SignerSettings(SSBase):
    pass


signer_settings = SignerSettings()
