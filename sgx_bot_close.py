import requests
import smtplib
import os
import yfinance as yf

from datetime import datetime
from zoneinfo import ZoneInfo

SGT = ZoneInfo("Asia/Singapore")

from email.mime.text import MIMEText
from datetime import datetime

# =========================================
# APIs
# =========================================

AGGREGATE_API = "https://api.sgx.com/securities/v1.1/aggregate/"

STI_INDEX_API = "https://api.sgx.com/indices/v1.0/pid/.STI/"

ALL_SECURITIES_API = "https://api.sgx.com/securities/v1.1?params=nc%2Cadjusted-vwap%2Cbond_accrued_interest%2Cbond_clean_price%2Cbond_dirty_price%2Cbond_date%2Cb%2Cbv%2Cp%2Cc%2Cchange_vs_pc%2Cchange_vs_pc_percentage%2Ccx%2Ccn%2Cdp%2Cdpc%2Cdu%2Ced%2Cfn%2Ch%2Ciiv%2Ciopv%2Clt%2Cl%2Co%2Cp_%2Cpv%2Cptd%2Cs%2Csv%2Ctrading_time%2Cv_%2Cv%2Cvl%2Cvwap%2Cvwap-currency"

# =========================================
# HEADERS
# =========================================

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.sgx.com/"
}

# =========================================
# EMAIL CONFIG
# =========================================

EMAIL_USER = os.getenv("EMAIL_USER")

EMAIL_PASS = os.getenv("EMAIL_PASS")

EMAIL_TO = os.getenv("EMAIL_TO")

# =========================================
# STI COMPONENTS
# =========================================

STI_COMPONENTS = {

    "A17U": {
        "zh": "凯德腾飞房地产信托",
        "en": "CapitaLand Ascendas REIT",
        "currency": "SGD"
    },

    "C38U": {
        "zh": "凯德综合商业信托",
        "en": "CapitaLand Integrated Commercial Trust",
        "currency": "SGD"
    },

    "9CI": {
        "zh": "凯德投资",
        "en": "CapitaLand Investment",
        "currency": "SGD"
    },

    "C09": {
        "zh": "城市发展",
        "en": "City Developments",
        "currency": "SGD"
    },

    "D05": {
        "zh": "星展集团",
        "en": "DBS",
        "currency": "SGD"
    },

    "D01": {
        "zh": "DFI零售集团",
        "en": "DFI Retail Group",
        "currency": "USD"
    },

    "J69U": {
        "zh": "星狮地产信托",
        "en": "Frasers Centrepoint Trust",
        "currency": "SGD"
    },

    "BUOU": {
        "zh": "星狮物流商产信托",
        "en": "Frasers Logistics & Commercial Trust",
        "currency": "SGD"
    },

    "G13": {
        "zh": "云顶新加坡",
        "en": "Genting Singapore",
        "currency": "SGD"
    },

    "H78": {
        "zh": "香港置地",
        "en": "Hongkong Land",
        "currency": "USD"
    },

    "J36": {
        "zh": "怡和控股",
        "en": "Jardine Matheson",
        "currency": "USD"
    },

    "BN4": {
        "zh": "吉宝",
        "en": "Keppel",
        "currency": "SGD"
    },

    "AJBU": {
        "zh": "吉宝数据中心房地产信托",
        "en": "Keppel DC REIT",
        "currency": "SGD"
    },

    "ME8U": {
        "zh": "丰树工业信托",
        "en": "Mapletree Industrial Trust",
        "currency": "SGD"
    },

    "M44U": {
        "zh": "丰树物流信托",
        "en": "Mapletree Logistics Trust",
        "currency": "SGD"
    },

    "N2IU": {
        "zh": "丰树泛亚商业信托",
        "en": "Mapletree Pan Asia Commercial Trust",
        "currency": "SGD"
    },

    "O39": {
        "zh": "华侨银行",
        "en": "OCBC",
        "currency": "SGD"
    },

    "S58": {
        "zh": "新翔集团",
        "en": "SATS",
        "currency": "SGD"
    },

    "5E2": {
        "zh": "海庭",
        "en": "Seatrium",
        "currency": "SGD"
    },

    "U96": {
        "zh": "胜科工业",
        "en": "Sembcorp Industries",
        "currency": "SGD"
    },

    "C6L": {
        "zh": "新航",
        "en": "Singapore Airlines",
        "currency": "SGD"
    },

    "S68": {
        "zh": "新交所",
        "en": "Singapore Exchange",
        "currency": "SGD"
    },

    "Z74": {
        "zh": "新电信",
        "en": "Singtel",
        "currency": "SGD"
    },

    "S63": {
        "zh": "新科工程",
        "en": "ST Engineering",
        "currency": "SGD"
    },

    "Y92": {
        "zh": "泰国酿酒",
        "en": "Thai Beverage",
        "currency": "SGD"
    },

    "U11": {
        "zh": "大华银行",
        "en": "UOB",
        "currency": "SGD"
    },

    "U14": {
        "zh": "华业集团",
        "en": "UOL",
        "currency": "SGD"
    },

    "V03": {
        "zh": "创业公司",
        "en": "Venture Corp",
        "currency": "SGD"
    },

    "F34": {
        "zh": "丰益国际",
        "en": "Wilmar International",
        "currency": "SGD"
    },

    "BS6": {
        "zh": "扬子江船业",
        "en": "Yangzijiang Shipbuilding",
        "currency": "SGD"
    }
}

# =========================================
# ASIA INDEXES
# =========================================

ASIA_INDEXES = {

    "上海": "000001.SS",
    "深圳": "399001.SZ",
    "香港": "^HSI",
    "台湾": "^TWII",
    "东京": "^N225",
    "首尔": "^KS11"
}

# =========================================
# HELPERS
# =========================================

SMALL_NUM = {
    0: "零",
    1: "一",
    2: "两",
    3: "三",
    4: "四",
    5: "五",
    6: "六",
    7: "七",
    8: "八",
    9: "九",
    10: "十"
}


def chinese_small_num(n):

    if n <= 10:
        return SMALL_NUM[n]

    return str(n)


def chinese_large_number(num):

    num = int(num)

    yi = num // 100000000

    wan = (num % 100000000) // 10000

    if yi > 0:
        return f"{yi}亿{wan}万"

    if wan > 0:
        return f"{wan}万"

    return str(num)


def chinese_weekday():

    now = datetime.now(SGT)

    mapping = {
        0: "星期一",
        1: "星期二",
        2: "星期三",
        3: "星期四",
        4: "星期五",
        5: "星期六",
        6: "星期日"
    }

    return mapping[
        now.weekday()
    ]


def chinese_date():

    now = datetime.now(SGT)

    return f"{now.month}月{now.day}日"


def market_direction(pct):

    if pct > 0:

        return {
            "title": "上涨",
            "verb": "上扬",
            "move": "涨"
        }

    return {
        "title": "下跌",
        "verb": "下挫",
        "move": "跌"
    }


def currency_suffix(stock):

    if stock["currency"] == "USD":
        return "美元"

    return "元"


# =========================================
# FETCH JSON
# =========================================

def fetch_json(url):

    r = requests.get(
        url,
        headers=HEADERS,
        timeout=10
    )

    r.raise_for_status()

    return r.json()

# =========================================
# FETCH ASIA INDEXES
# =========================================

def fetch_asia_indexes():

    results = {}

    for market, ticker in ASIA_INDEXES.items():

        data = yf.Ticker(ticker)

        hist = data.history(period="2d")

        latest = hist.iloc[-1]

        prev = hist.iloc[-2]

        pct = (
            (
                latest["Close"]
                - prev["Close"]
            )
            / prev["Close"]
        ) * 100

        results[market] = round(
            pct,
            2
        )

    return results


# =========================================
# EMAIL
# =========================================

def send_email(story):

    msg = MIMEText(
        story,
        "plain",
        "utf-8"
    )

    msg["Subject"] = datetime.now(SGT).strftime(
    "SGX闭市即时（%Y%m%d）"
)

    msg["From"] = EMAIL_USER

    msg["To"] = EMAIL_TO

    server = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    server.starttls()

    server.login(
        EMAIL_USER,
        EMAIL_PASS
    )

    server.send_message(msg)

    server.quit()


# =========================================
# MAIN
# =========================================

def main():

    # -----------------------------
    # MON-FRI ONLY
    # -----------------------------

    weekday = datetime.today().weekday()

    if weekday >= 5:

        print("Weekend detected. Skip.")

        return

    # -----------------------------
    # FETCH APIs
    # -----------------------------

    aggregate = fetch_json(
        AGGREGATE_API
    )["data"]

    sti = fetch_json(
        STI_INDEX_API
    )["data"][0]
    
    all_stocks_response = fetch_json(
    ALL_SECURITIES_API
)

# -----------------------------
# EXTRACT PRICES ARRAY
# -----------------------------

    all_stocks = all_stocks_response["data"]["prices"]

# -----------------------------
# FILTER STI COMPONENTS
# -----------------------------

    sti_stocks = []

    for stock in all_stocks:
        
        symbol = stock["nc"]
        
        if symbol in STI_COMPONENTS:
            
            stock["zh_name"] = STI_COMPONENTS[symbol]["zh"]
            
            stock["en_name"] = STI_COMPONENTS[symbol]["en"]

            stock["currency"] = STI_COMPONENTS[symbol]["currency"]
            
            sti_stocks.append(stock)

    # -----------------------------
    # MARKET BREADTH
    # -----------------------------

    up = 0
    down = 0
    flat = 0

    for stock in sti_stocks:

        pct = stock["p"]

        if pct > 0:
            up += 1

        elif pct < 0:
            down += 1

        else:
            flat += 1

    # -----------------------------
    # TOP GAINER / LOSER
    # -----------------------------

    gainers = sorted(
        [
            s for s in sti_stocks
            if s["p"] > 0
        ],
        key=lambda x: x["p"],
        reverse=True
    )

    losers = sorted(
        [
            s for s in sti_stocks
            if s["p"] < 0
        ],
        key=lambda x: x["p"]
    )

    top_gainer = gainers[0]

    top_loser = losers[0]

    # -----------------------------
    # ASIA INDEXES
    # -----------------------------

    asia = fetch_asia_indexes()

    # -----------------------------
    # STORY
    # -----------------------------

    # -----------------------------
    # DIRECTION
    # -----------------------------

    direction = market_direction(
        sti["ptc"]
    )

    # -----------------------------
    # STORY
    # -----------------------------

    story = f"""
海指{chinese_weekday()}闭市{market_direction(sti['ptc'])}{abs(sti['ptc']):.2f}%

新加坡海峡时报指数{chinese_weekday()}（{chinese_date()}）闭市收报{sti['lp']:.2f}点，{direction_word(sti['ptc'])}{abs(sti['c']):.2f}点或{abs(sti['ptc']):.2f}%。

上海股市{direction_word(asia['上海'])}{abs(asia['上海']):.2f}%、深圳股市{direction_word(asia['深圳'])}{abs(asia['深圳']):.2f}%、香港股市{direction_word(asia['香港'])}{abs(asia['香港']):.2f}%。

其他市场方面，台湾股市{direction_word(asia['台湾'])}{abs(asia['台湾']):.2f}%，东京{direction_word(asia['东京'])}{abs(asia['东京']):.2f}%，首尔{direction_word(asia['首尔'])}{abs(asia['首尔']):.2f}%。

新加坡股市{chinese_weekday()}全场成交量{chinese_large_number(aggregate['volume'])}股，总交易额{chinese_large_number(aggregate['value'])}元。上升股{int(aggregate['advancers'])}只，下跌股{int(aggregate['decliners'])}只。

海指主要成分股{up}只上涨，{flat}只持平，{down}只下跌。

涨幅最大的是{top_gainer['zh_name']}（{top_gainer['en_name']}），起{abs(top_gainer['p']):.2f}%，收报{top_gainer['lt']:.2f}{currency_suffix(top_gainer)}。

{gainers[1]['zh_name']}（{gainers[1]['en_name']}）涨{abs(gainers[1]['p']):.2f}%，收报{gainers[1]['lt']:.2f}{currency_suffix(gainers[1])}。{gainers[2]['zh_name']}（{gainers[2]['en_name']}）涨{abs(gainers[2]['p']):.2f}%收报{gainers[2]['lt']:.2f}{currency_suffix(gainers[2])}。{gainers[3]['zh_name']}（{gainers[3]['en_name']}）涨{abs(gainers[3]['p']):.2f}%，收报{gainers[3]['lt']:.2f}{currency_suffix(gainers[3])}。

跌幅最大的是{top_loser['zh_name']}（{top_loser['en_name']}），收报{top_loser['lt']:.2f}{currency_suffix(top_loser)}，跌幅{abs(top_loser['p']):.2f}%。

{losers[1]['zh_name']}（{losers[1]['en_name']}）跌{abs(losers[1]['p']):.2f}%，收报{losers[1]['lt']:.2f}{currency_suffix(losers[1])}。{losers[2]['zh_name']}（{losers[2]['en_name']}）跌{abs(losers[2]['p']):.2f}%，收报{losers[2]['lt']:.2f}{currency_suffix(losers[2])}。{losers[3]['zh_name']}（{losers[3]['en_name']}）跌{abs(losers[3]['p']):.2f}%，收报{losers[3]['lt']:.2f}{currency_suffix(losers[3])}。
"""

    # -----------------------------
    # PRINT
    # -----------------------------

    print(story)

    # -----------------------------
    # SAVE FILE
    # -----------------------------

    filename = datetime.now().strftime(
        "%Y%m%d_market_close.txt"
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(story)

    # -----------------------------
    # SEND EMAIL
    # -----------------------------

    send_email(story)

    print("Email sent.")


# =========================================
# RUN
# =========================================

if __name__ == "__main__":

    main()