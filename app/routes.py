"""
    Contain all api endpoints
"""
import json
from flask import request, jsonify
from flask_restful import Resource, Api, reqparse
from app import app
from app.models.product import Product
from app.models.sale import Sale

api = Api(app)

products = []
sales = []

class SingleProductEndPoint(Resource):
    "Returns a single product"
    def get(self, product_id):
        'Returns a single product with id of product_id'
        for product in products:
            if product.product_id == int(product_id):
                response_data = dict(
                        product_id=product.product_id,
                        product_name=product.product_name,
                        product_price=product.product_price,
                        product_count=product.product_count
                    )
                return jsonify(response_data)
        return {
            'message': 'Product with id {} does not exist'.format(product_id)
        }
class ProductEndPoint(Resource):
    "Handles all requests to /products endpoint"
    def get(self):
        'Handles all get requests to /products endpoint'
        response_data = []
        if products:
            for product in products:
                data = dict(
                    product_id = product.product_id,
                    product_name = product.product_name,
                    product_price = product.product_price,
                    product_count = product.product_count
                )
                response_data.append(data)
            json_data = jsonify(response_data)
            return json_data
                
        return {'message': 'No Products added yet'}

    def post(self):
        'Handles all post requests to /products endpoint'
        parser = reqparse.RequestParser()
        parser.add_argument(
            'product_name', 
            type=str, 
            required=True,
            help="Product Name can not be empty" 
        )
        parser.add_argument(
            'product_price', 
            type=int, 
            required=True,
            help="Product Price can not be empty" 
        )
        args = parser.parse_args()
        product_name = args['product_name']
        product_price = args['product_price']

        if products:
            for product in products:
                if product.product_name == product_name:
                    return {
                        'message' : 'Product {} already exists'.format(product_name)
                    }

        product_id = len(products) + 1
        new_product = Product(
            product_name = product_name,
            product_price = product_price
        )
        new_product.product_id = product_id
        products.append(new_product)

        return {
            'message': 'Product {} with id {} successfully added'.format(
                product_name, product_id),
            }, 201

class SingleSaleEndPoint(Resource):
    "Returns a single sale"
    def get(self, sale_id):
        'Returns a single sale with id of sale_id'
        for sale in sales:
            if sale.sale_id == int(sale_id):
                response_data = dict(
                        sale_id=sale.sale_id,
                        product_id=sale.product_id,
                        products_sold=sale.products_sold,
                        sale_date=sale.sale_date
                    )
                return jsonify(response_data)
        return {
            'message': 'Sale with id {} does not exist'.format(sale_id)
        }


class SaleEndPoint(Resource):
    "Handles all requests to /sales endpoint"

    def get(self):
        'Handles all get requests /sales'
        response_data = []
        if sales:
            for sale in sales:
                data = dict(
                    sale_id = sale.sale_id,
                    product_id = sale.product_id,
                    products_sold = sale.products_sold,
                    sale_date = sale.sale_date
                )
                response_data.append(data)
            return jsonify(response_data)
        return {'message': 'No Sales made yet'}
    
    def post(self):
        'Handles all post requests to /sales endpoint'
        parser = reqparse.RequestParser()
        parser.add_argument(
            'product_id', 
            type=int, 
            required=True,
            help="Product id can not be empty" 
        )

        parser.add_argument(
            'products_sold', 
            type=int, 
            required=True,
            help="Products sold can not be empty" 
        )

        args = parser.parse_args()
        product_id = args['product_id']
        products_sold = args['products_sold']

        if products:
            for product in products:
                if product.product_id == int(product_id):
                    sale = Sale(
                        product_id = product.product_id,
                        products_sold = products_sold 
                    )
                    sale.sale_id = len(sales) + 1
                    sales.append(sale)
                    return {
                        'message': '{} {}(s) successfully sold'.format(
                            products_sold, 
                            product.product_name
                            )
                    }
        return {
            'message': 'Product with Product id {} does not exist'.format(product_id)
            }

# Endpoints to url mapping
api.add_resource(ProductEndPoint, '/api/v1/products')
api.add_resource(SingleProductEndPoint, '/api/v1/products/<product_id>')
api.add_resource(SaleEndPoint, '/api/v1/sales')
api.add_resource(SingleSaleEndPoint, '/api/v1/sales/<sale_id>')