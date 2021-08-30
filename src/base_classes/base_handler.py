import logging
from copy import deepcopy
from importlib import import_module

from base_classes.exceptions import InvalidFilterError
from base_classes.base_filter import BaseFilter

logger = logging.getLogger(__name__)


class BaseHandler:
    _filter_chain = None

    def load_filters(self, filterchain):
        """
        loads filter chain as defined in settings
        ALL FILTERS MUST INHERENT FORM BASEFILTER CLASS TO WORK
        :return:
        """
        handler = self._generic_handler
        logger.debug(f"loading filter chain as {filterchain}")

        for filter_path in reversed(filterchain):
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

    def __init__(self, filterchain):
        self.load_filters(filterchain)

    def __call__(self, alertgroup):
        logger.debug(
            f"calling {self._filter_chain.__class__.__name__} with {alertgroup}"
        )
        return self._filter_chain(alertgroup, deepcopy(alertgroup))


# copied form django utils module loading, to make this code not depedant on django
def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError(
            'Module "%s" does not define a "%s" attribute/class'
            % (module_path, class_name)
        ) from err
