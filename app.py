# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import datetime

app = Flask(__name__)

# Main
class VO(object):
    def __init__(self):
        self._count = 0
        self._price = 0

    def getcount(self):
        return self._count

    def setcount(self, count):
        self._count = count

    def getprice(self):
        return self._price

    def setprice(self, price):
        self._price = price

    count = property(getcount, setcount)
    price = property(getprice, setprice)

vo = VO()

def pickup_premium():
    """UR の景品を確定して排出する"""
    ur = ["景品1", "景品2", "景品3", "景品4", "景品5", "景品6", "景品7",
          "景品8", "景品9", "景品10", "景品11", "景品12"]
    return np.random.choice(ur)

def pickup_rare(weight):
    """重みに応じてレアガチャを排出する"""
    rarities = ["R", "SR", "UR"]
    picked_rarity = np.random.choice(rarities, p=weight)

    if picked_rarity == "UR":
        picked_rarity = "".join((picked_rarity, "(", pickup_premium(), ")"))

    return picked_rarity

def turn_rare():
    """レアガチャを回す"""
    result = []
    # 小数点第三位を切り上げて 94.85%, 5.04%, 0.12%
    weight = [0.94849, 0.0504, 0.00111]
    result.append(pickup_rare(weight))
    return result

def turn_10rare():
    """10 連レアガチャを回す"""
    result = []
    # 小数点第三位を切り上げて 90.28%, 9.29%, 0.45%
    weight = [0.90278, 0.09281, 0.00441]
    for v in range(0, 9):
        result.append(pickup_rare(weight))
    result.append("SR")
    return result

# Routing
@app.route('/')
def index():
    title = "ようこそ"
    message = "ガチャを回すにはボタンをクリックしてください"
    return render_template('index.html',
                           message=message, title=title)

@app.route('/post', methods=['POST', 'GET'])
def post():
    time = datetime.datetime.today().strftime("%H:%M:%S")
    message = ""
    if request.method == 'POST':
        result = []
        if 'rare' in request.form:
            title = "ガチャを回しました！"
            vo.price = vo.price + 300
            vo.count = vo.count + 1
            result = turn_rare()
        if '10rare' in request.form:
            title = "ガチャを回しました！"
            vo.price = vo.price + 3000
            vo.count = vo.count + 1
            result = turn_10rare()
        if 'reset' in request.form:
            title = "リセットしました"
            vo.price = 0
            vo.count = 0
            result = ""
            message = "リセットしました"
        return render_template('index.html',
                               result=result, title=title,
                               time=time, vo=vo,
                               message=message)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=3000)
