from __future__ import annotations
from abc import ABC, abstractmethod

class Resource(ABC):
    """Abstract base for hardware resources with safe invariants."""
    __slots__ = ("_name", "_manufacturer", "_total", "_allocated")

    def __init__(self, name: str, manufacturer: str, total: int, allocated: int):
        if self.__class__ is Resource:
            raise TypeError("Resource is abstract and cannot be instantiated directly")
        self._name = self._validate_str("name", name)
        self._manufacturer = self._validate_str("manufacturer", manufacturer)
        self._total = self._validate_int_nonneg("total", total)
        self._allocated = self._validate_int_nonneg("allocated", allocated)
        if self._allocated > self._total:
            raise ValueError("allocated cannot exceed total")
        self._validate_specific()

    # Hook for subclasses
    @abstractmethod
    def _validate_specific(self) -> None: ...

    # Read-only properties
    @property
    def name(self) -> str: return self._name
    @property
    def manufacturer(self) -> str: return self._manufacturer
    @property
    def total(self) -> int: return self._total
    @property
    def allocated(self) -> int: return self._allocated
    @property
    def category(self) -> str: return self.__class__.__name__

    # Behaviors
    def claim(self, n: int) -> None:
        n = self._validate_int_pos("n", n)
        if self._allocated + n > self._total:
            raise ValueError("not enough free units to claim")
        self._allocated += n

    def freeup(self, n: int) -> None:
        n = self._validate_int_pos("n", n)
        if n > self._allocated:
            raise ValueError("cannot free more than allocated")
        self._allocated -= n

    def died(self, n: int) -> None:
        n = self._validate_int_pos("n", n)
        free = self._total - self._allocated
        if n > free:
            raise ValueError("cannot remove more units than currently free")
        self._total -= n

    def purchased(self, n: int) -> None:
        n = self._validate_int_pos("n", n)
        self._total += n

    # Representation
    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
                f"name={self._name!r}, manufacturer={self._manufacturer!r}, "
                f"total={self._total!r}, allocated={self._allocated!r}{self._repr_tail()})")

    def __str__(self) -> str:
        return (f"{self.category}(name={self._name}, manufacturer={self._manufacturer}, "
                f"total={self._total}, allocated={self._allocated}{self._str_tail()})")

    def _repr_tail(self) -> str: return ""
    def _str_tail(self) -> str: return ""

    # Validators
    @staticmethod
    def _validate_str(field: str, value) -> str:
        if not isinstance(value, str) or not value.strip():
            raise TypeError(f"{field} must be a non-empty string")
        return value

    @staticmethod
    def _validate_int_nonneg(field: str, value) -> int:
        if not isinstance(value, int):
            raise TypeError(f"{field} must be int")
        if value < 0:
            raise ValueError(f"{field} must be >= 0")
        return value

    @staticmethod
    def _validate_int_pos(field: str, value) -> int:
        if not isinstance(value, int):
            raise TypeError(f"{field} must be int")
        if value <= 0:
            raise ValueError(f"{field} must be > 0")
        return value


class Storage(Resource):
    __slots__ = ("_capacity_GB",)
    def __init__(self, name: str, manufacturer: str, total: int, allocated: int, capacity_GB: int):
        self._capacity_GB = self._validate_int_nonneg("capacity_GB", capacity_GB)
        super().__init__(name, manufacturer, total, allocated)
    @property
    def capacity_GB(self) -> int: return self._capacity_GB
    def _validate_specific(self) -> None: return None
    def _repr_tail(self) -> str: return f", capacity_GB={self._capacity_GB!r}"
    def _str_tail(self) -> str: return f", capacity_GB={self._capacity_GB}"


class CPU(Resource):
    __slots__ = ("_cores", "_socket", "_power_watts")
    def __init__(self, name: str, manufacturer: str, total: int, allocated: int,
                 cores: int, socket: str, power_watts: int):
        self._cores = self._validate_int_pos("cores", cores)
        self._socket = self._validate_str("socket", socket)
        self._power_watts = self._validate_int_pos("power_watts", power_watts)
        super().__init__(name, manufacturer, total, allocated)
    @property
    def cores(self) -> int: return self._cores
    @property
    def socket(self) -> str: return self._socket
    @property
    def power_watts(self) -> int: return self._power_watts
    def _validate_specific(self) -> None: return None
    def _repr_tail(self) -> str:
        return (f", cores={self._cores!r}, socket={self._socket!r}, "
                f"power_watts={self._power_watts!r}")
    def _str_tail(self) -> str:
        return f", cores={self._cores}, socket={self._socket}, power_watts={self._power_watts}"

class HDD(Storage):
    __slots__ = ("_size", "_rpm")
    def __init__(self, name: str, manufacturer: str, total: int, allocated: int,
                 capacity_GB: int, size: str, rpm: int):
        self._size = self._validate_str("size", size)
        self._rpm = self._validate_int_pos("rpm", rpm)
        super().__init__(name, manufacturer, total, allocated, capacity_GB)
    @property
    def size(self) -> str: return self._size
    @property
    def rpm(self) -> int: return self._rpm
    def _validate_specific(self) -> None: return None
    def _repr_tail(self) -> str:
        return super()._repr_tail() + f", size={self._size!r}, rpm={self._rpm!r}"
    def _str_tail(self) -> str:
        return super()._str_tail() + f", size={self._size}, rpm={self._rpm}"

class SSD(Storage):
    __slots__ = ("_interface",)
    def __init__(self, name: str, manufacturer: str, total: int, allocated: int,
                 capacity_GB: int, interface: str):
        self._interface = self._validate_str("interface", interface)
        super().__init__(name, manufacturer, total, allocated, capacity_GB)
    @property
    def interface(self) -> str: return self._interface
    def _validate_specific(self) -> None: return None
    def _repr_tail(self) -> str:
        return super()._repr_tail() + f", interface={self._interface!r}"
    def _str_tail(self) -> str:
        return super()._str_tail() + f", interface={self._interface}"
