from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# データベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trade_config.db'  # SQLiteデータベースのURIを設定
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 変更追跡機能を無効にする
db = SQLAlchemy(app)  # SQLAlchemyのインスタンスを作成

# データベースモデルの定義
class TradeConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # プライマリキー
    trade_amount = db.Column(db.Integer, nullable=False)  # 取引金額
    trade_day = db.Column(db.Integer, nullable=False)  # 購入日

# アプリケーションコンテキスト内でデータベース操作を実行
with app.app_context():
    # データベースから最新の取引設定を取得
    latest_config = TradeConfig.query.order_by(TradeConfig.id.desc()).first()
    if latest_config:
        # 最新の取引設定が存在する場合、その値をGitHub Actionsの出力として設定
        print(f"::set-output name=TRADE_AMOUNT::{latest_config.trade_amount}")
        print(f"::set-output name=TRADE_DAY::{latest_config.trade_day}")
    else:
        # 最新の取引設定が存在しない場合、デフォルト値をGitHub Actionsの出力として設定
        print("::set-output name=TRADE_AMOUNT::30000")
        print("::set-output name=TRADE_DAY::28")