from typing import Generic, TypeVar, Type
from abc import ABC, abstractmethod

T = TypeVar("T")


class BaseConverter(Generic[T], ABC):
    """Base Converter, all converters must inherit from this converter"""

    def __init__(self, annotation=None):
        self.annotation: Type[T] = annotation

    @abstractmethod
    def convert(self, value: str) -> T:
        """ Method that converts the string sent, to it's desired type."""
