from django.test import TestCase, override_settings
import inspect

from src.base_classes.exceptions import InvalidFilterError
from src.base_classes.base_handler import BaseHandler
from tests.mock_objects.mock_filters import (
    TestFilterAddOnPre,
    TestFilterDoNothing,
    TestFilterAddOnPost,
    TestFilterRemoveOnPre,
    POSTACTIONKEY,
    POSTACTIONVALUE,
)

TEST_CHAIN = [
    "tests.mock_objects.mock_filters.TestFilterAddOnPre",
    "tests.mock_objects.mock_filters.TestFilterDoNothing",
    "tests.mock_objects.mock_filters.TestFilterAddOnPost",
    "tests.mock_objects.mock_filters.TestFilterRemoveOnPre",
]

FAULTY_TEST_CHAIN = [
    "tests.mock_objects.mock_filters.TestFilterDoNothing",
    "tests.mock_objects.mock_filters.FilterWithoutInheritance",
]


class TestBaseHandler(TestCase):
    def testGenericHandler(self):
        handler = object.__new__(BaseHandler)
        input_data = {"this": "is", "some": "test", "data": 124}
        output_data = handler._generic_handler(input_data, "")
        self.assertEqual(
            input_data,
            output_data,
            "_generic_handler function should not alter the data",
        )
        pass

    @override_settings(PROMETHEUS_FILTERS=TEST_CHAIN)
    def testLoadFilter(self):
        handler = BaseHandler()
        self.assertIsInstance(handler._filter_chain, TestFilterAddOnPre)
        handler = handler._filter_chain
        self.assertIsInstance(handler._filter_alertgroup, TestFilterDoNothing)
        handler = handler._filter_alertgroup
        self.assertIsInstance(handler._filter_alertgroup, TestFilterAddOnPost)
        handler = handler._filter_alertgroup
        self.assertIsInstance(handler._filter_alertgroup, TestFilterRemoveOnPre)
        handler = handler._filter_alertgroup
        self.assertTrue(inspect.ismethod(handler._filter_alertgroup))

    @override_settings(PROMETHEUS_FILTERS=TEST_CHAIN)
    def testRunFilterChain(self):
        key = "key"
        value = "value"
        test_data = {key: value}
        handler = BaseHandler()
        result = handler(test_data)
        self.assertEqual(len(result), 2)
        self.assertTrue(key in result)
        self.assertEqual(result.get(key), value)
        self.assertTrue(POSTACTIONKEY in result)
        self.assertEqual(result.get(POSTACTIONKEY), POSTACTIONVALUE)

    @override_settings(PROMETHEUS_FILTERS=FAULTY_TEST_CHAIN)
    def testFaultyFilterChain(self):
        with self.assertRaises(InvalidFilterError):
            BaseHandler()
