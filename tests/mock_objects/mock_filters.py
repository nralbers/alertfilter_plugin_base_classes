from base_classes.base_filter import BaseFilter
from base_classes.exceptions import HTTP400Error, HTTP503Error, SilenceEvent
from tests.mock_objects.mock_exception import MockException

PREACTIONKEY = "preaction"
PREACTIONVALUE = "added on pre"
POSTACTIONKEY = "postaction"
POSTACTIONVALUE = "added on post"


class TestFilterDoNothing(BaseFilter):
    def prefilter(self, alertgroup):
        return alertgroup

    def postfilter(self, alertgroup):
        return alertgroup


class TestFilterAddOnPre(BaseFilter):
    def prefilter(self, alertgroup):
        alertgroup[PREACTIONKEY] = PREACTIONVALUE
        return alertgroup

    def postfilter(self, alertgroup):
        return alertgroup


class TestFilterAddOnPost(BaseFilter):
    def prefilter(self, alertgroup):
        return alertgroup

    def postfilter(self, alertgroup):
        alertgroup[POSTACTIONKEY] = POSTACTIONVALUE
        return alertgroup


class TestFilterRemoveOnPre(BaseFilter):
    def prefilter(self, alertgroup):
        del alertgroup[PREACTIONKEY]
        return alertgroup

    def postfilter(self, alertgroup):
        return alertgroup


class TestFilterRaiseHttp400(BaseFilter):
    def prefilter(self, alertgroup):
        pass

    def postfilter(self, alertgroup):
        raise HTTP400Error()


class TestFilterRaiseHttp503(BaseFilter):
    def prefilter(self, alertgroup):
        pass

    def postfilter(self, alertgroup):
        raise HTTP503Error()


class TestFilterRaiseMockException(BaseFilter):
    def prefilter(self, alertgroup):
        pass

    def postfilter(self, alertgroup):
        raise MockException()


class TestFilterSilence(BaseFilter):
    def prefilter(self, alertgroup):
        pass

    def postfilter(self, alertgroup):
        raise SilenceEvent()


class FilterWithoutInheritance:
    pass


class MockFilter:
    def __call__(self, data, immutable_alertgroup):
        return data
