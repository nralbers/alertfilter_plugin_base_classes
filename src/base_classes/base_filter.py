import logging
from abc import ABC, abstractmethod

from django.conf import settings


class BaseFilter(ABC):
    def __init__(self, filter_alertgroup):
        self._filter_alertgroup = filter_alertgroup
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"{self.__class__.__name__} created")
        # One-time configuration and initialization.

    @abstractmethod
    def prefilter(self, alertgroup):
        raise NotImplementedError

    def _call_next_filter(self, alertgroup, immutable_alertgroup):
        self.logger.debug(
            f"calling {self._filter_alertgroup.__class__.__name__} with {alertgroup}"
        )
        filtered_alertgroup = self._filter_alertgroup(alertgroup, immutable_alertgroup)
        return filtered_alertgroup

    @abstractmethod
    def postfilter(self, alertgroup):
        raise NotImplementedError

    def __call__(self, alertgroup, immutable_alertgroup):
        self.immutable_alertgroup = immutable_alertgroup
        # Code to be executed for each alertgroup before later filters are called.
        # ex: alertgroup['prefilter'] = True
        prefiltered_alertgroup = self.prefilter(alertgroup)
        filtered_alertgroup = self._call_next_filter(
            prefiltered_alertgroup, immutable_alertgroup
        )
        # Code to be executed for each alertgroup after later filters are called.
        # ex: filtered_alertgroup['postfilter'] = True
        postfiltered_alertgroup = self.postfilter(filtered_alertgroup)

        return postfiltered_alertgroup
