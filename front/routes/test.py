# from db.userm_model import Userm_model
# import secrets
# from werkzeug.security import generate_password_hash
# from . import app
#
# @app.route('/text', methods=['GET'])
# def text():
#     hashed_password = generate_password_hash("123456")
#     arr = [
#         ["世界遺産ひとり", "user01@example.com"],
#         ["旅人の足跡", "user02@example.com"],
#         ["文化探求者", "user03@example.com"],
#         ["神社巡り", "user04@example.com"],
#         ["風景の詩", "user05@example.com"],
#         ["歴史の語り部", "user06@example.com"],
#         ["自然愛好者", "user07@example.com"],
#         ["祭りの心", "user08@example.com"],
#         ["伝統工芸", "user09@example.com"],
#         ["都会と田舎", "user10@example.com"],
#         ["温泉巡礼者", "user11@example.com"],
#         ["美食探訪", "user12@example.com"],
#         ["四季折々", "user13@example.com"],
#         ["古都の風", "user14@example.com"],
#         ["寺院の静けさ", "user15@example.com"],
#         ["文学愛好家", "user16@example.com"],
#         ["芸術の旅人", "user17@example.com"],
#         ["夜景の夢", "user18@example.com"],
#         ["田舎の彩り", "user19@example.com"],
#         ["日本文化研究者", "user20@example.com"],
#         ["桜の見物人", "user21@example.com"],
#         ["風鈴の音色", "user22@example.com"],
#         ["紅葉狩り", "user23@example.com"],
#         ["夜桜鑑賞", "user24@example.com"],
#         ["古寺散策", "user25@example.com"],
#         ["和風の心", "user26@example.com"],
#         ["詩的情景", "user27@example.com"],
#         ["祭りの達人", "user28@example.com"],
#         ["庭園愛好者", "user29@example.com"],
#         ["平安の香り", "user30@example.com"],
#         ["夏祭りの情熱", "user31@example.com"],
#         ["海辺の散策者", "user32@example.com"],
#         ["城郭探訪", "user33@example.com"],
#         ["秘境探検家", "user34@example.com"],
#         ["秋の味覚", "user35@example.com"],
#         ["温泉愛好家", "user36@example.com"],
#         ["陶芸鑑賞者", "user37@example.com"],
#         ["茶道愛好家", "user38@example.com"],
#         ["和菓子の達人", "user39@example.com"],
#         ["旅する心", "user40@example.com"]
#     ]
#
#     for i in arr:
#         user_id = secrets.token_hex(5)
#         while Userm_model().user_authentication(user_id):
#             user_id = secrets.token_hex(5)
#         user = {
#             "user_id": user_id,
#             "nickname": i[0],
#             "user_email_address": i[1],
#             "user_password": hashed_password,
#             "user_type": 1
#         }
#         Userm_model().add_user(user)
#
#
# if __name__ == '__main__':
#     pass