from unittest import TestCase

from base_classes.base_filter import BaseFilter
from tests.mock_objects import mock_filters
from tests.alerts.valid_alert_group import get_valid_alertgroup


class TestBaseFilters(TestCase):
    def setUp(self):
        self.KEY = "key"
        self.VALUE = "value"
        self.test_data = {self.KEY: self.VALUE}
        self.mock_filter = mock_filters.MockFilter()

    def tearDown(self):
        self.test_data = None
        self.mock_filter = None

    def testDoNothing(self):
        test_filter = mock_filters.TestFilterDoNothing(self.mock_filter)
        result = test_filter(self.test_data, "")
        self.assertEqual(result, self.test_data)

    def testDoPre(self):
        test_filter = mock_filters.TestFilterAddOnPre(self.mock_filter)
        result = test_filter(self.test_data, "")
        self.assertEqual(len(result), 2)
        self.assertTrue(self.KEY in result)
        self.assertEqual(result.get(self.KEY), self.VALUE)
        self.assertTrue(mock_filters.PREACTIONKEY in result)
        self.assertEqual(
            result.get(mock_filters.PREACTIONKEY), mock_filters.PREACTIONVALUE
        )

    def testDoPost(self):
        test_filter = mock_filters.TestFilterAddOnPost(self.mock_filter)
        result = test_filter(self.test_data, "")
        self.assertEqual(len(result), 2)
        self.assertTrue(self.KEY in result)
        self.assertEqual(result.get(self.KEY), self.VALUE)
        self.assertTrue(mock_filters.POSTACTIONKEY in result)
        self.assertEqual(
            result.get(mock_filters.POSTACTIONKEY), mock_filters.POSTACTIONVALUE
        )

    def testFilterChain(self):
        test_filter = mock_filters.TestFilterAddOnPost(self.mock_filter)
        test_filter = mock_filters.TestFilterAddOnPre(test_filter)
        test_filter = mock_filters.TestFilterDoNothing(test_filter)
        result = test_filter(self.test_data, "")
        self.assertEqual(len(result), 3)
        self.assertTrue(self.KEY in result)
        self.assertEqual(result.get(self.KEY), self.VALUE)
        self.assertTrue(mock_filters.PREACTIONKEY in result)
        self.assertEqual(
            result.get(mock_filters.PREACTIONKEY), mock_filters.PREACTIONVALUE
        )
        self.assertTrue(mock_filters.POSTACTIONKEY in result)
        self.assertEqual(
            result.get(mock_filters.POSTACTIONKEY), mock_filters.POSTACTIONVALUE
        )

    def testFilterChainOrder(self):
        test_filter = mock_filters.TestFilterRemoveOnPre(self.mock_filter)
        test_filter = mock_filters.TestFilterAddOnPost(test_filter)
        test_filter = mock_filters.TestFilterAddOnPre(test_filter)
        test_filter = mock_filters.TestFilterDoNothing(test_filter)
        result = test_filter(self.test_data, "")
        self.assertEqual(len(result), 2)
        self.assertTrue(self.KEY in result)
        self.assertEqual(result.get(self.KEY), self.VALUE)
        self.assertTrue(mock_filters.POSTACTIONKEY in result)
        self.assertEqual(
            result.get(mock_filters.POSTACTIONKEY), mock_filters.POSTACTIONVALUE
        )

    def test_pre_filter(self):
        BaseFilter.__abstractmethods__ = set()
        base_filter = BaseFilter(None)
        alert_group = get_valid_alertgroup()
        with self.assertRaises(NotImplementedError):
            base_filter.prefilter(alert_group)

    def test_post_filter(self):
        BaseFilter.__abstractmethods__ = set()
        base_filter = BaseFilter(None)
        alert_group = get_valid_alertgroup()
        with self.assertRaises(NotImplementedError):
            base_filter.postfilter(alert_group)
