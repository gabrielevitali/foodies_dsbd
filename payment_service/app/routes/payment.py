from flask import Blueprint, jsonify, request
from app.services.db_service import connect_to_db


payment_routes = Blueprint('payment', __name__)


@payment_routes.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


@payment_routes.route('/')
def payment_service():
    return jsonify({"message":"Welcome to the Payment Service via NGINX!"})