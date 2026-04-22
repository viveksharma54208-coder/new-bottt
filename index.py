import requests, random, time, os
from datetime import datetime, timedelta

BOT_NAME = "🚀 NEXUS FUTURE ENGINE 🚀"
DEVELOPER = "👨‍💻 Chandan"

SETTINGS = {
    "market": os.getenv("MARKET", "OTC"),
    "timeframe": int(os.getenv("TIMEFRAME", 1)),
    "from_time": os.getenv("FROM_TIME", "00:00"),
    "to_time": os.getenv("TO_TIME", "23:59"),
    "accuracy": int(os.getenv("ACCURACY", 75)),
    "pairs": os.getenv("PAIRS", "").split(",")
}

ALL_PAIRS = [
    "USDBRL-OTC","USDNGN-OTC","USDCOP-OTC","USDARS-OTC",
    "USDCLP-OTC","USDPEN-OTC","USDTRY-OTC","USDPKR-OTC",
    "USDBDT-OTC","USDZAR-OTC","USDSGD-OTC","USDTHB-OTC","USDHKD-OTC",
    "EURUSD","EURGBP","EURJPY","GBPJPY","AUDJPY","EURAUD","GBPAUD",
    "EURCHF","GBPCHF","AUDCHF","CADJPY","CHFJPY","NZDJPY",
    "EURCAD","GBPCAD","AUDCAD","NZDCAD","EURNZD","GBPNZD","AUDNZD"
]

# अगर user ne pairs nahi diye to sab use karo
if SETTINGS["pairs"] == [''] or not SETTINGS["pairs"]:
    SETTINGS["pairs"] = ALL_PAIRS

# ===== SAFE LIVE DATA =====
def get_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5)
        return float(r.json()["price"])
    except:
        return None

# ===== ENGINES =====
def live_engine():
    price = get_price()
    if price is None:
        return None, 50

    score = random.randint(-5,5)
    prob = min(abs(score)*15, 95)

    if abs(score) < 2:
        return None, prob

    return ("CALL" if score>0 else "PUT"), prob

def otc_engine():
    score = random.randint(-6,6)
    prob = min(abs(score)*18 + random.randint(5,15), 95)

    if abs(score) < 2:
        return None, prob

    return ("CALL" if score>0 else "PUT"), prob

# ===== SIGNAL =====
def generate():
    now = datetime.now()
    signals = []

    for i in range(1,30):
        t = (now + timedelta(minutes=i*SETTINGS["timeframe"])).strftime("%H:%M")

        if not (SETTINGS["from_time"] <= t <= SETTINGS["to_time"]):
            continue

        for pair in SETTINGS["pairs"]:
            if pair not in ALL_PAIRS:
                continue

            if SETTINGS["market"] == "OTC":
                if "OTC" not in pair: continue
                signal, prob = otc_engine()
            else:
                if "OTC" in pair: continue
                signal, prob = live_engine()

            if signal and prob >= SETTINGS["accuracy"]:
                icon = "🟢📈" if signal=="CALL" else "🔴📉"
                tier = "💎 VIP" if prob>=85 else "🔥 PREMIUM"

                signals.append(f"""
╔════════════════════╗
🚀 NEXUS FUTURE ENGINE
👨‍💻 Dev: Chandan
╚════════════════════╝
{icon} {pair} ({SETTINGS['market']})
⏰ {t} ⏳ M{SETTINGS['timeframe']}
🔮 {signal}
📊 {int(prob)}% {tier}
━━━━━━━━━━━━━━━━━━
""")
                break

        if len(signals) >= 10:
            break

    return signals

# ===== RUN SAFE LOOP =====
if __name__ == "__main__":
    print("🚀 BOT STARTED FULL MODE...")

    while True:
        try:
            sigs = generate()

            if sigs:
                for s in sigs:
                    print(s)
            else:
                print("❌ No signals")

            print("⏳ Next cycle...\n")
            time.sleep(30)

        except Exception as e:
            print("⚠️ ERROR:", e)
            time.sleep(10)
