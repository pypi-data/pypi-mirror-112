from typing import List, Optional, TypedDict


__all__ = (
    'PersonalInfoDTO', 'PersonalDataDTO', 'PersonalDataResult',
    'AddressDTO', 'DocumentDTO',
)


class PersonalInfoDTO(TypedDict):
    last_name: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]

    phone: Optional[str]
    email: Optional[str]

    rnokpp: Optional[str]

    client_id: Optional[str]
    client_id_text: Optional[str]

    birth_day: Optional[str]
    sex: Optional[str]
    social_status: Optional[str]

    is_peps: Optional[bool]
    is_terrorist: Optional[bool]
    is_restricted: Optional[bool]
    is_high_risk: Optional[bool]
    is_ua_resident: Optional[bool]


class AddressDTO(TypedDict):
    type: Optional[str]
    country: Optional[str]
    state: Optional[str]
    area: Optional[str]
    city: Optional[str]
    street: Optional[str]
    street_number: Optional[str]
    flat_number: Optional[str]


class DocumentDTO(TypedDict):
    type: Optional[str]
    name: Optional[str]
    series: Optional[str]
    number: Optional[str]
    issued_by: Optional[str]
    issued_by_country: Optional[str]
    issued_at: Optional[str]
    expired_at: Optional[str]


class PersonalDataDTO(TypedDict):
    info: PersonalInfoDTO
    addresses: List[AddressDTO]
    documents: List[DocumentDTO]

class PersonalDataResult(TypedDict):
    data: PersonalDataDTO
    certificate: dict
