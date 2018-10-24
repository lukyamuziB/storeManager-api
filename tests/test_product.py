"""
    This module will contain tests for the Product class
"""
from unittest import TestCase
from app.models.product import Product

class ProductTestCase(TestCase):

    def setUp(self):
        "Initialize variables"
        self.product = Product("Sugar", 2000)

    def test_one_product_object_created_successfully(self):
        "Tests if one product can be added"
        self.assertListEqual(
            [None, "Sugar", 2000, 1], 
            [
                self.product.product_id, 
                self.product.product_name, 
                self.product.product_price, 
                self.product.product_quantity
            ]
        )

    def test_three_product_object_created_successfully(self):
        "Tests if 3 products can be added"
        product = Product("Sugar", 2000, 3)
        self.assertListEqual(
            [None, "Sugar", 2000, 3], 
            [
                product.product_id, 
                product.product_name, 
                product.product_price, 
                product.product_quantity
            ]
        )
    

