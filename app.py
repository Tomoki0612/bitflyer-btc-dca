from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm
import os

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'your_secret_key'  # セッション用の秘密鍵を設定

# データベースの設定
# インスタンスフォルダ内にデータベースファイルを作成するパスを指定
db_path = os.path.join(app.instance_path, 'trade_config.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # SQLAlchemyのエラーログを有効にする
db = SQLAlchemy(app)

# インスタンスフォルダが存在しない場合は作成
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# データベースモデルの定義
# TradeConfigテーブルのスキーマを定義
class TradeConfig(db.Model):
    __tablename__ = 'trade_config'
    id = db.Column(db.Integer, primary_key=True)  # 主キー
    trade_amount = db.Column(db.Integer, nullable=False)  # 取引金額
    trade_day = db.Column(db.Integer, nullable=False)  # 取引日

# アプリケーションコンテキスト内でデータベースの初期化
with app.app_context():
    db.create_all()  # テーブルを作成
    print("Database tables created")

# ルートURLにアクセスしたときにindex.htmlを返す
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# 取引設定を保存するAPIエンドポイント
@app.route('/api/setTradeConfig', methods=['POST'])
def set_trade_config():
    data = request.json  # リクエストのJSONデータを取得
    trade_amount = data.get('tradeAmount')  # 取引金額を取得
    trade_day = data.get('tradeDay')  # 取引日を取得

    # 取引金額と取引日が設定されていない場合はエラーメッセージを返す
    if not trade_amount or not trade_day:
        return jsonify({'error': '取引金額と購入日を設定してください'}), 400

    # データベースに保存
    new_config = TradeConfig(trade_amount=trade_amount, trade_day=trade_day)
    db.session.add(new_config)  # 新しい取引設定を追加
    db.session.commit()  # 変更をコミット
    print(f"Saved config: trade_amount={trade_amount}, trade_day={trade_day}")

    return jsonify({'message': '設定が保存されました'})

# ログインページのエンドポイント
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'password':
            flash('ログインに成功しました', 'success')
            return redirect(url_for('serve_index'))
        else:
            flash('ユーザー名またはパスワードが間違っています', 'danger')
    return render_template('login.html', form=form)

# アプリケーションをデバッグモードで実行
if __name__ == '__main__':
    app.run(debug=True)