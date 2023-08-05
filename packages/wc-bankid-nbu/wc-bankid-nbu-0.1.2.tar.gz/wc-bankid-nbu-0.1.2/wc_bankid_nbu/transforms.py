from typing import Dict, List, Sequence, Tuple, Union
from functools import partial
from datetime import date, datetime
from .dtos import AddressDTO, PersonalDataDTO, PersonalInfoDTO


__all__ = 'personal_data_response_to_dto',


Pairs = Sequence[Tuple[str, str]]
Transforms = Dict[str, callable]


def to_boolean(value: Union[str, int, bool]):
    return (
        value == '1'
        if isinstance(value, str)
        else
        value == 1
        if isinstance(value, int)
        else
        bool(value)
    )


def to_date(value: Union[str, int]):
    return (
        date.fromtimestamp(value)
        if isinstance(value, int)
        else
        datetime.strptime(value, '%d.%m.%Y').date()
        if isinstance(value, str)
        else
        None
    )


def remap_names(names: dict, value: str, default_key: str = '__default__'):
    return names[value] if value in names else names.get(default_key)


def generic_transformer(pairs: Pairs, transforms: Transforms, passed: dict) -> dict:
    result = {}

    for field, source in pairs:
        if source in passed:
            data = passed[source]

            if data is None:
                continue

            if field in transforms:
                data = transforms[field](data)

            result[field] = data

    return result


info_transformer = partial(
    generic_transformer,
    (
        ('last_name', 'lastName'),
        ('first_name', 'firstName'),
        ('middle_name', 'middleName'),

        ('phone', 'phone'),
        ('email', 'email'),

        ('rnokpp', 'inn'),

        ('client_id', 'clId'),
        ('client_id_text', 'clIdText'),

        ('birth_day', 'birthDay'),
        ('sex', 'sex'),
        ('social_status', 'socStatus'),

        ('is_peps', 'flagPEPs'),
        ('is_terrorist', 'flagPersonTerror'),
        ('is_restricted', 'flagRestriction'),
        ('is_high_risk', 'flagTopLevelRisk'),
        ('is_ua_resident', 'uaResident'),
    ),
    {
        # FIXME: It must return date type
        # 'birth_day': to_date,

        'is_peps': to_boolean,
        'is_terrorist': to_boolean,
        'is_restricted': to_boolean,
        'is_high_risk': to_boolean,
        'is_ua_resident': to_boolean,
    },
)
address_transformer = partial(
    generic_transformer,
    (
        ('type', 'type'),
        ('country', 'country'),
        ('state', 'state'),
        ('area', 'area'),
        ('city', 'city'),
        ('street', 'street'),
        ('street_number', 'houseNo'),
        ('flat_number', 'flatNo'),
    ),
    {},
)
document_transformer = partial(
    generic_transformer,
    (
        ('type', 'type'),
        ('type', 'typeName'),
        ('series', 'series'),
        ('number', 'number'),
        ('issued_by', 'issue'),
        ('issued_by_country', 'issueCountryIso2'),
        ('issued_at', 'dateIssue'),
        ('expired_at', 'dateExpiration'),
    ),
    {
        'type': partial(remap_names, {
            'passport': 'passport_book',
            'idpassport': 'passport_id',
            'zpassport': 'passport_international',
            'ident': 'identity',
        })
    },
)


def personal_data_response_to_dto(response: dict) -> PersonalDataDTO:
    result: PersonalDataDTO = {}

    result['info'] = info_transformer(response)

    addresses = result['addresses'] = []

    for address in response.get('addresses') or []:
        addresses.append(address_transformer(address))

    documents = result['documents'] = []

    for document in response.get('documents') or []:
        documents.append(document_transformer(document))

    return result
