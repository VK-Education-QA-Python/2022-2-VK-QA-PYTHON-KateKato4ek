from base import BaseTest
from model import (
    UniqRequestsCountTable,
    AmountOfRequestsByTypeTable,
    MostFrequentRequestsTable,
    MostFrequent4XXRequestsTable,
    MostFrequent5XXRequestsByIpTable
)

class TestSQL(BaseTest):
    def test_task1(self):
        self.builder.calc_uniq_requests_count()
        assert self.get_rows_count(UniqRequestsCountTable) == 1

    def test_task2(self):
        self.builder.calc_amount_of_requests_by_type()
        assert self.get_rows_count(AmountOfRequestsByTypeTable) == 5

    def test_task3(self):
        count = 10
        self.builder.calc_most_frequent_requests(count=count)
        assert self.get_rows_count(MostFrequentRequestsTable) == count

    def test_task4(self):
        count = 5
        self.builder.calc_most_frequent_4XX_requests(count=count)
        assert self.get_rows_count(MostFrequent4XXRequestsTable) == count

    def test_task5(self):
        count = 5
        self.builder.calc_most_frequent_5XX_requests_by_ip(count=count)
        assert self.get_rows_count(MostFrequent5XXRequestsByIpTable) == count
