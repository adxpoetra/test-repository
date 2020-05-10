# folder resources hanya untuk yang berhubungan langsung dengan users
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.item import ItemModel


class Item(Resource):  # nama item akan dipanggil pada link
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Ga boleh kosong cuy")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Setiap item harus mempunyai ID")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': "item {} tidak ditemukan".format(name)}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'data sudah ada cuy'}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'eror bro'}, 500  # internal server error

        return item.json(), 201  # statusnya menjadi created 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()  # cek data ga boleh kosong

        item = ItemModel.find_by_name(name)

        updated_item = ItemModel(name, **data)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):  # menampilkan list item
    def get(self):
        return{'items': [x.json() for x in ItemModel.query.all()]}
