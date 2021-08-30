from unittest import TestCase
import inspect

from base_classes.exceptions import InvalidFilterError
from base_classes.base_handler import BaseHandler
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

    def testLoadFilter(self):
        handler = BaseHandler(TEST_CHAIN)
        self.assertIsInstance(handler._filter_chain, TestFilterAddOnPre)
        handler = handler._filter_chain
        self.assertIsInstance(handler._filter_alertgroup, TestFilterDoNothing)
        handler = handler._filter_alertgroup
        self.assertIsInstance(handler._filter_alertgroup, TestFilterAddOnPost)
        handler = handler._filter_alertgroup
        self.assertIsInstance(handler._filter_alertgroup, TestFilterRemoveOnPre)
        handler = handler._filter_alertgroup
        self.assertTrue(inspect.ismethod(handler._filter_alertgroup))

    def testRunFilterChain(self):
        key = "key"
        value = "value"
        test_data = {key: value}
        handler = BaseHandler(TEST_CHAIN)
        result = handler(test_data)
        self.assertEqual(len(result), 2)
        self.assertTrue(key in result)
        self.assertEqual(result.get(key), value)
        self.assertTrue(POSTACTIONKEY in result)
        self.assertEqual(result.get(POSTACTIONKEY), POSTACTIONVALUE)

    def testFaultyFilterChain(self):
        with self.assertRaises(InvalidFilterError):
            BaseHandler(FAULTY_TEST_CHAIN)
