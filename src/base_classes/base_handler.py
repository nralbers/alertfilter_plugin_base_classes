import logging
from copy import deepcopy

from django.conf import settings
from django.utils.module_loading import import_string

from src.base_classes.exceptions import InvalidFilterError
from src.base_classes.base_filter import BaseFilter

logger = logging.getLogger(__name__)


class BaseHandler:
    _filter_chain = None

    def load_filters(self):
        """
        loads filter chain as defined in settings
        ALL FILTERS MUST INHERENT FORM BASEFILTER CLASS TO WORK
        :return:
        """
        handler = self._generic_handler
        logger.debug(f"loading filter chain as {settings.PROMETHEUS_FILTERS}")

        for filter_path in reversed(settings.PROMETHEUS_FILTERS):
            filter_class = import_string(filter_path)
            if BaseFilter not in filter_class.mro():
                message = f"{filter_path} has to inherit from filters.base_filter.filter.BaseFilter"
                logger.critical(message)
                raise InvalidFilterError(message)
            filter_instance = filter_class(handler)
            handler = filter_instance

        self._filter_chain = handler

    def _generic_handler(self, alertgroup, immutable_alertgroup):
        return alertgroup

    def __init__(self):
        self.load_filters()

    def __call__(self, alertgroup):
        logger.debug(
            f"calling {self._filter_chain.__class__.__name__} with {alertgroup}"
        )
        return self._filter_chain(alertgroup, deepcopy(alertgroup))
