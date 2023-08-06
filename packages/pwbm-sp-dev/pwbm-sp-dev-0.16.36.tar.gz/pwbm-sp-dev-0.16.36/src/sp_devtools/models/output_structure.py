from datetime import date
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, conint, constr, root_validator, stricturl, validator

from sp_devtools.constants import PeriodicityTypes


class TableRow(BaseModel):
    series_correlation_id: Optional[constr(strip_whitespace=True, min_length=1)]
    series_id: Optional[Optional[UUID]]
    number: Optional[conint(ge=0)]
    indent: Optional[conint(ge=0)]
    label: Optional[constr(strip_whitespace=True)]

    @root_validator(pre=True)
    def validate_number(cls, values):
        for key in ('number', 'indent'):
            if isinstance(values[key], str) and not values[key].isdigit():
                values[key] = None
        return values


class Table(BaseModel):
    correlation_id: constr(strip_whitespace=True, min_length=1)
    id: Optional[Optional[UUID]]
    name: Optional[constr(strip_whitespace=True)]
    description: Optional[constr(strip_whitespace=True)]
    source_url: Optional[stricturl(tld_required=False)]
    rows: Optional[List[TableRow]]


class Tag(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    value: Optional[constr(strip_whitespace=True, min_length=1)]


class DataPoint(BaseModel):
    periodicity: str
    period: str
    value: str

    @validator('period')
    def validate_period(cls, period, values):
        if values['periodicity'] != PeriodicityTypes.custom:
            try:
                date.fromisoformat(period)
            except ValueError:
                raise ValueError(f'Period "{period}" is invalid ISO format string')
        return period


class Series(BaseModel):
    correlation_id: constr(strip_whitespace=True, min_length=1)
    id: Optional[UUID]
    name: constr(strip_whitespace=True)
    description: Optional[constr(strip_whitespace=True)]
    source_url: Optional[stricturl(tld_required=False)]
    data_type: Optional[constr(strip_whitespace=True, min_length=1)]
    tags: Optional[List[Tag]]
    data_values: Optional[List[DataPoint]]

    @validator('data_type')
    def prepare_data_type(cls, data_type):
        if data_type:
            return data_type.lower()


class Meta(BaseModel):
    producer: constr(strip_whitespace=True, min_length=1) = 'PWBM Scraping Platform'
    namespace: constr(strip_whitespace=True, min_length=1)
    task_id: Optional[conint(ge=0)]


class UploadStructure(BaseModel):
    format_version: Literal['0.2'] = '0.2'
    file_meta: Meta
    tables: Optional[List[Table]]
    series: Optional[List[Series]]
