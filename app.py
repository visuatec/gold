from flask import Flask, jsonify, request, send_from_directory
from bs4 import BeautifulSoup
import requests
import re
from xe_convert import get_exchange_rate

app = Flask(__name__)


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/gold-price", methods=["GET"])
def get_gold_price():
    url = "https://sjc.com.vn/giavang/textContent.php"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find("table")

    pattern = r"Vàng nhẫn SJC 99,99  1 chỉ, 2 chỉ, 5 chỉ\s+(\d{2},\d{3},\d{3})\s+(\d{2},\d{3},\d{3})"
    match = re.search(pattern, table.text)

    if match:
        amount1, amount2 = match.groups()
        one_chi = int(amount1.replace(",", "")) / 10
        five_chi = one_chi * 5
        exchange_rate = float(get_exchange_rate("USD", "VND"))

        result = {
            "buy_price": amount1,
            "sell_price": amount2,
            "1_chi_vnd": one_chi,
            "5_chi_vnd": five_chi,
            "1_chi_usd": round(one_chi / exchange_rate, 2),
            "5_chi_usd": round(five_chi / exchange_rate, 2),
            "5_rings_usd": round((five_chi / exchange_rate) * 5, 2),
        }
        return jsonify(result)
    else:
        return jsonify({"error": "Pattern not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
