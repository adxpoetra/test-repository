import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()  # agar bisa dipanggil di seluruh def
    # username dan password ga boleh kosong
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Username Ga boleh kosong cuy")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Password boleh kosong cuy")

    def post(self):
        data = UserRegister.parser.parse_args()  # memanggil parser diatas

        # ini artinya klo hasilnya if bukan None beri peringatan
        if UserModel.find_by_username(data['username']):
            return {"message": "Username {} telah dibuat sebelumnya".format(data['username'])}, 400

        user = UserModel(**data)
        user.save_to_db()

        # menggunakan {} dan .format untuk mendeteksi username yang dibuat
        return {"message": "User {} berhasil dibuat".format(data['username'])}
