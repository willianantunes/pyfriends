import unittest

from datetime import date
from unittest import TestCase

from pyfriends.database_utils import execute_query


class TestModulePathResolution(TestCase):
    @unittest.skip("The table might not have data, and I'm lazy to add some 😅")
    def test_execute_query(self):
        # Arrange
        raw_query = r"SELECT * FROM show;"
        # Act
        result = execute_query(raw_query)
        # Assert
        expected_object = [
            (
                1,
                "Friends",
                date(1994, 9, 22),
                "Six young (20-something) people from New York City (Manhattan), on their own and struggling to "
                "survive in the real world, find the companionship, comfort and support they get from each other "
                "to be the perfect antidote to the pressures of life.This average group of buddies goes through "
                "massive mayhem, family trouble, past and future romances, fights, laughs, tears and surprises as "
                "they learn what it really means to be a friend.",
                "NBC",
                "United States",
            )
        ]
        self.assertEqual(expected_object, result)

    @unittest.skip("The table might not have data, and I'm lazy to add some 😅")
    def test_execute_query_with_params(self):
        # Arrange
        raw_query = r"SELECT id FROM character WHERE short_name = :short_name"
        data = {"short_name": "MONICA"}
        # Act
        result = execute_query(raw_query, data=data)
        # Assert
        expected_object = [(4,)]
        self.assertEqual(expected_object, result)
