from social_core.backends.oauth import BaseOAuth2
from wc_bankid_nbu import (
    PersonalPhysicalDataQuery, APIClient, PersonalInfoDTO,
    TAddress, TDocument, FPerson, FAddress, FDocument,
)


__all__ = 'BankIDNBUBaseBackend',


class BankIDNBUBaseBackend(BaseOAuth2):
    """BankID NBU OAuth authentication backend"""

    name = 'bankid-nbu'
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [('id', 'id'), ('expires', 'expires')]

    client: APIClient
    PERSONAL_DATA_QUERY = (
        PersonalPhysicalDataQuery()
        .fields(
            FPerson.FIRST_NAME, FPerson.MIDDLE_NAME, FPerson.LAST_NAME,
            FPerson.BIRTH_DAY, FPerson.SEX, FPerson.SOCIAL_STATUS,

            FPerson.PHONE, FPerson.EMAIL, FPerson.RNOKPP,
            FPerson.CLIENT_ID, FPerson.CLIENT_ID_TEXT,
            FPerson.IS_HIGH_RISK, FPerson.IS_PEPS, FPerson.IS_RESTRICTED,
            FPerson.IS_TERRORIST,

            FPerson.IS_UA_RESIDENT,
        )
        .address(
            TAddress.FACTUAL,
            FAddress.COUNTRY, FAddress.REGION, FAddress.DISTRICT, FAddress.CITY,
            FAddress.STREET, FAddress.STREET_NUMBER, FAddress.FLAT_NUMBER,
        )
        .address(
            TAddress.JURIDICAL,
            FAddress.COUNTRY, FAddress.REGION, FAddress.DISTRICT, FAddress.CITY,
            FAddress.STREET, FAddress.STREET_NUMBER, FAddress.FLAT_NUMBER,
        )
        .document(
            TDocument.PASSPORT_BOOK,
            FDocument.TYPE,
            FDocument.SERIES, FDocument.NUMBER,
            FDocument.ISSUED_BY, FDocument.ISSUED_BY_COUNTRY,
            FDocument.ISSUED_AT, FDocument.EXPIRED_AT,
        )
        .document(
            TDocument.PASSPORT_ID,
            FDocument.TYPE,
            FDocument.SERIES, FDocument.NUMBER,
            FDocument.ISSUED_BY, FDocument.ISSUED_BY_COUNTRY,
            FDocument.ISSUED_AT, FDocument.EXPIRED_AT,
        )
    )

    def authorization_url(self):
        return self.client.AUTHORIZATION_URL

    def access_token_url(self):
        return self.client.ACCESS_TOKEN_URL

    def refresh_token_url(self):
        return self.client.REFRESH_TOKEN_URL

    def get_user_id(self, details, response):
        info = (response.get('data') or {}).get('info') or {}

        return info.get('rnokpp') or info.get('email')

    def get_user_details(self, response):
        """Return user details from BankID NBU account"""
        info: PersonalInfoDTO = response['data']['info']

        return {
            'username': info.get('email') or info.get('rnokpp') or info.get('phone'),
            'email': info.get('email') or '',
            'first_name': info.get('first_name') or '',
            'last_name': info.get('last_name') or '',
        }

    def user_data(self, access_token: str, *args, **kwargs):
        data = self.client.get_personal_data(
            self.PERSONAL_DATA_QUERY, access_token
        )

        return {'data': data['data']}
