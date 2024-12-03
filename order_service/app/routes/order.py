from flask import Blueprint, jsonify, request
from app.services.db_service import connect_to_db


order_routes = Blueprint('order', __name__)


@order_routes.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


@order_routes.route('/')
def order_service():
    return jsonify({"message":"Welcome to the Order Service via NGINX!"})