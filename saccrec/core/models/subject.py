from typing import Optional, Union

from datetime import date, datetime

from saccrec.consts import DATE_FORMAT
from saccrec.core import Genre, SubjectStatus


_FULL_NAME_FIELD = 'full_name'
_GENRE_FIELD = 'genre'
_BORNDATE_FIELD = 'borndate'
_STATUS_FIELD = 'status'


class Subject:
    
    def __init__(
        self,
        full_name: str = '',
        genre: Optional[Union[Genre, str]] = None,
        borndate: [date, str] = None,
        status: Optional[Union[SubjectStatus, str]] = None
    ):
        self._full_name = full_name

        if isinstance(genre, str):
            self._genre = Genre(genre)
        else:
            self._genre = genre

        if isinstance(borndate, str):
            self._genre = datetime.strptime(borndate, DATE_FORMAT)
        else:
            self._borndate = borndate

        if isinstance(status, str):
            self._status = SubjectStatus(status)
        else:
            self._status = status

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, value: str):
        self._full_name = full_name
    
    @property
    def genre(self) -> Optional[Genre]:
        return self._genre

    @genre.setter
    def genre(self, value: Optional[Union[Genre, str]]):
        if isinstance(value, str):
            self._genre = Genre(value)
        else:
            self._genre = value

    @property
    def borndate(self) -> Optional[date]:
        return self._borndate

    @borndate.setter
    def borndate(self, value: date):
        self._borndate = borndate

    @property
    def status(self) -> Optional[SubjectStatus]:
        return self._status

    @status.setter
    def status(self, value: Optional[Union[SubjectStatus, str]]):
        if isinstance(value, str):
            self._status = SubjectStatus(value)
        else:
            self._status = value

    @property
    def json(self) -> dict:
        return {
            _FULL_NAME_FIELD: self.full_name,
            _GENRE_FIELD: self._genre.value if self._genre is not None else None,
            _BORNDATE_FIELD: self.borndate.strftime(DATE_FORMAT),
            _STATUS_FIELD: self.status.value if self._status is not None else None,
        }

    @classmethod
    def from_json(cls, json: dict) -> 'Subject':
        return Subject(
            full_name=json.get(_FULL_NAME_FIELD, 'Unknown'),
            genre=json.get(_GENRE_FIELD, Genre.Unknown),
            borndate=json.get(_BORNDATE_FIELD, None),
            status=json.get(_STATUS_FIELD, SubjectStatus.Unknown)
        )
    