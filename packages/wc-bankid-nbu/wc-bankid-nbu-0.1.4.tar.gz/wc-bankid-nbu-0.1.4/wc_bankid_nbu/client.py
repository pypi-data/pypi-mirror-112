from functools import cached_property
from requests import request

from .query import QueryBuilder
from .signer import Signer
from .dtos import PersonalDataResult, PersonalDataDTO
from .transforms import personal_data_response_to_dto


__all__ = 'APIClient', 'TestAPIClient'


def urlprop(postfix: str):
    return cached_property(lambda self: self.BASE_URL + postfix)


class APIClient:
    BASE_URL: str = 'https://id.bank.gov.ua/v1'
    AUTHORIZATION_URL: str = urlprop('/bank/oauth2/authorize')
    ACCESS_TOKEN_URL: str = urlprop('/bank/oauth2/token')
    REFRESH_TOKEN_URL: str = urlprop('/bank/oauth2/refresh_token')
    PERSONAL_DATA_URL: str = urlprop('/bank/resource/client')

    signer: Signer

    def __init__(self, signer: Signer = None):
        assert signer is not None, 'You must provide `signer`.'

        self.signer = signer

    def parse_personal_data(self, response: dict) -> PersonalDataDTO:
        return personal_data_response_to_dto(response)

    def get_personal_data(
        self,
        query: QueryBuilder,
        access_token: str,
    ) -> PersonalDataResult:
        with self.signer.signer() as signer:
            parameters = {
                **query.to_foreign(),
                'cert': signer.get_distribution_certificate(b64=True)
            }

            response = self.make_request(
                self.PERSONAL_DATA_URL,
                headers={
                    'Accept': 'application/json',
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json',
                },
                json=parameters,
                method='POST',
            ).json()

            signer.read_private_key()
            data, certificate = signer.decrypt(
                response['cert'], response['customerCrypto']
            )

        return {
            'data': self.parse_personal_data(data),
            'certificate': certificate,
        }

    def make_request(self, url, method='GET', *args, **kwargs):
        kwargs.setdefault('headers', {})

        response = request(method, url, *args, **kwargs)
        response.raise_for_status()
        return response


class TestAPIClient(APIClient):
    BASE_URL: str = 'https://testid.bank.gov.ua/v1'
