from dto.prototypes import DataPrototype, ResponsePrototype
from dto.auth import JwtData, Role
from datetime import datetime
from enum import Enum


class Action(Enum):
    Submit = "submit"
    Update = "update"
    Create = "create"

    @staticmethod
    def get(value):
        try:
            role = Action(value)
        except ValueError:
            return None
        return role


class Submit(Enum):
    Accept = True
    Decline = False

    @staticmethod
    def get(value):
        try:
            role = Submit(value)
        except ValueError:
            return None
        return role


class OrderStatus(Enum):
    Created = "created"
    Accepted = "accepted"
    Updated = "updated"


class Order(DataPrototype):
    def __init__(self, order_json):
        self.desc = order_json.get("desc")
        self.cost = order_json.get("cost")
        self.name = order_json.get("name")
        self.deadline = order_json.get("deadline")
        self.status = "created"
        self.check_empty()


class ClientOrderSubmit(DataPrototype):
    def __init__(self, data_json):
        self.submit = Submit.get(data_json.get("submit"))
        self.order_id = data_json.get("id_order")
        self.check_empty()


class MasterOrderDesc(DataPrototype):
    def __init__(self, data_json):
        self.order_id = data_json.get("id_order")
        self.product_type = data_json.get("type")
        self.cost = data_json.get("cost")
        self.mater_desc = data_json.get("master_desc")
        self.check_empty()


class UpdateOrder(DataPrototype):
    def __init__(self, jwt_data: JwtData, update_json):
        self.jwt_data = jwt_data
        self.action = Action.get(update_json.get("action"))
        if self.action == Action.Update:
            self.update = MasterOrderDesc(update_json)
        elif self.action == Action.Submit:
            self.submit = ClientOrderSubmit(update_json)
        elif self.action == Action.Create:
            self.create = Order(update_json)
        self.check_empty()


class OrderRecord:
    def __init__(self, record):
        self.order_id = record[0]
        self.deadline = record[1]
        self.cost = record[2]
        self.status = record[3]


class Orders(ResponsePrototype):
    def __init__(self, orders_tuple):
        self.orders = [OrderRecord(order).__dict__ for order in orders_tuple]
