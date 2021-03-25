from dataclasses import dataclass, fields
from enum import Enum
from typing import Any, List


@dataclass
class Maybe:
    value: Any
    comment: str

    def __str__(self):
        if self.value is None:
            return f'None {self.comment}'

        return f'Some ({self.value})'


@dataclass
class DList:
    value: List[Any]
    comment: str

    def __str__(self):
        if not self.value:
            return f'[] : {self.comment}'

        return '[' + ', '.join(str(item) for item in self.value) + ']'


class Protocol(Enum):
    o2ib = 1
    tcp = 2

    def __str__(self):
        return f'P.{self.name}'


class DhallTuple:
    def __str__(self):
        def v(field):
            return getattr(self, field.name)

        return '{ ' + ', '.join(f'{k.name} = {v(k)}'
                                for k in fields(self)) + ' }'

    def __repr__(self):
        return self.__str__()


@dataclass
class Text:
    # The only reason why the class is here is that standard Python str type
    # gets stringified with single quotes (while Dhall supports double
    # quotes only).
    s: str

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'"{self.s}"'


@dataclass(repr=False)
class M0Clients(DhallTuple):
    s3: int
    other: int


@dataclass(repr=False)
class DisksDesc(DhallTuple):
    meta_data: Maybe  # [str]
    data: DList


@dataclass(repr=False)
class M0ServerDesc(DhallTuple):
    runs_confd: Maybe  # [bool]
    io_disks: DisksDesc


@dataclass(repr=False)
class NodeDesc(DhallTuple):
    hostname: Text
    data_iface: Text
    data_iface_type: Maybe  # [Protocol]
    io_disks: DList  # [str]
    meta_data1: Text
    meta_data2: Text
    s3_instances: int


@dataclass(repr=False)
class DiskRef(DhallTuple):
    path: Text
    node: Maybe


@dataclass(repr=False)
class PoolDesc(DhallTuple):
    name: Text
    disk_refs: Maybe  # [DList]
    data_units: int
    parity_units: int


@dataclass(repr=False)
class ProfileDesc(DhallTuple):
    name: Text
    pools: DList  # [str]


@dataclass(repr=False)
class ClusterDesc(DhallTuple):
    node_info: List[NodeDesc]
    pool_info: List[PoolDesc]
    profile_info: List[ProfileDesc]


@dataclass(repr=False)
class MissingKeyError(Exception):
    key: str
    def __str__(self):
        return f"Required key '{self.key}' not found"
