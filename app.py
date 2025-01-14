from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/setTradeConfig', methods=['POST'])
def set_trade_config():
    data = request.json
    trade_amount = data.get('tradeAmount')
    trade_day = data.get('tradeDay')

    if not trade_amount or not trade_day:
        return jsonify({'error': '取引金額と購入日を設定してください'}), 400

    # 環境変数を更新
    os.environ['TRADE_AMOUNT'] = str(trade_amount)
    os.environ['TRADE_DAY'] = str(trade_day)

    # GitHub Actionsのワークフローファイルを更新
    with open('.github/workflows/main.yml', 'r') as file:
        workflow = file.read()

    workflow = workflow.replace(
        "TRADE_AMOUNT: '10000'", f"TRADE_AMOUNT: '{trade_amount}'"
    ).replace(
        "cron: '0 0 * * *'", f"cron: '0 0 {trade_day} * *'"
    )

    with open('.github/workflows/main.yml', 'w') as file:
        file.write(workflow)

    return jsonify({'message': '設定が保存されました'})

if __name__ == '__main__':
    app.run(debug=True)