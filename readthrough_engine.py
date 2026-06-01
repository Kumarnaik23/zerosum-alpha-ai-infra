# =============================================================
# ZEROSUM ALPHA — Automated Read-Through Signal Engine
# Pulls revenue data, compares to prior quarter,
# generates signals for impacted stocks automatically
# =============================================================

import yfinance as yf
import json
from datetime import datetime

# =============================================================
# READ-THROUGH MATRIX — signal logic per reporter
# =============================================================
READ_THROUGH_RULES = {
    "NVDA": {
        "name": "Nvidia",
        "watch_metric": "revenue_growth",
        "impacts": ["SMCI", "DELL", "VRT", "ANET", "MU", "TSM", "HPE"],
        "signal_logic": {
            "strong":  "Blackwell demand confirmed. GPU server buildout accelerating. Bullish for entire AI supply chain.",
            "inline":  "Steady AI demand. Supply chain stable. No major read-through.",
            "weak":    "Data center softness. Risk-off for AI server, memory, and networking names."
        },
        "strong_threshold": 0.20,
        "weak_threshold":   0.05,
    },
    "AVGO": {
        "name": "Broadcom",
        "watch_metric": "revenue_growth",
        "impacts": ["ANET", "COHR", "LITE", "TSM", "MRVL"],
        "signal_logic": {
            "strong":  "Custom ASIC wins accelerating. Networking silicon demand strong. Bullish for optical and switching names.",
            "inline":  "Steady custom silicon demand. Neutral for optical and networking.",
            "weak":    "Custom ASIC cycle softening. Caution on optical connectivity names."
        },
        "strong_threshold": 0.15,
        "weak_threshold":   0.05,
    },
    "MSFT": {
        "name": "Microsoft",
        "watch_metric": "revenue_growth",
        "impacts": ["NVDA", "AVGO", "MRVL", "VRT", "SMCI", "ANET"],
        "signal_logic": {
            "strong":  "Azure AI growth above consensus. Hyperscaler capex cycle intact. Strong buy signal for AI silicon and infra.",
            "inline":  "Azure growing steadily. Capex on track. Neutral read-through.",
            "weak":    "Azure deceleration risk. Could signal capex pullback. Caution on GPU and data centre names."
        },
        "strong_threshold": 0.15,
        "weak_threshold":   0.08,
    },
    "GOOGL": {
        "name": "Alphabet",
        "watch_metric": "revenue_growth",
        "impacts": ["NVDA", "AVGO", "TSM", "VRT", "ANET"],
        "signal_logic": {
            "strong":  "GCP acceleration confirmed. AI capex guidance raised. Bullish for GPU and data centre infrastructure.",
            "inline":  "GCP growing in line. Capex maintained. Neutral.",
            "weak":    "GCP softness. Risk of capex reduction. Negative read-through for AI infra."
        },
        "strong_threshold": 0.15,
        "weak_threshold":   0.08,
    },
    "META": {
        "name": "Meta",
        "watch_metric": "revenue_growth",
        "impacts": ["NVDA", "AVGO", "ANET", "VRT", "ETN"],
        "signal_logic": {
            "strong":  "Meta raising AI capex. Top-3 GPU buyer globally increasing spend. Bullish for compute and power infra.",
            "inline":  "AI spend maintained. Neutral for supply chain.",
            "weak":    "Meta pulling back AI spend. Negative signal for GPU and power infrastructure."
        },
        "strong_threshold": 0.15,
        "weak_threshold":   0.05,
    },
    "AMZN": {
        "name": "Amazon",
        "watch_metric": "revenue_growth",
        "impacts": ["NVDA", "AVGO", "MU", "SMCI", "VRT"],
        "signal_logic": {
            "strong":  "AWS AI revenue accelerating. Trainium/custom silicon expanding. Strong demand signal for GPU supply chain.",
            "inline":  "AWS growing steadily. AI workload demand intact. Neutral.",
            "weak":    "AWS deceleration. Risk of capex cuts. Negative for AI silicon and server names."
        },
        "strong_threshold": 0.15,
        "weak_threshold":   0.08,
    },
    "DELL": {
        "name": "Dell Technologies",
        "watch_metric": "revenue_growth",
        "impacts": ["NVDA", "MU", "AVGO", "SMCI", "HPE"],
        "signal_logic": {
            "strong":  "PowerEdge AI server backlog building. Enterprise AI deployment accelerating. Bullish for GPU, memory, networking.",
            "inline":  "AI server demand stable. Supply chain neutral.",
            "weak":    "AI server demand softening. Negative signal for GPU and memory names."
        },
        "strong_threshold": 0.20,
        "weak_threshold":   0.05,
    },
    "TSM": {
        "name": "TSMC",
        "watch_metric": "revenue_growth",
        "impacts": ["NVDA", "AMD", "AVGO", "ASML", "AMAT", "MRVL"],
        "signal_logic": {
            "strong":  "Advanced node utilization high. CoWoS packaging at capacity. Confirms AI chip demand cycle intact.",
            "inline":  "Utilization steady. Demand cycle on track. Neutral.",
            "weak":    "Utilization softening. Could signal AI chip order slowdown. Negative for fabless designers."
        },
        "strong_threshold": 0.15,
        "weak_threshold":   0.05,
    },
    "MU": {
        "name": "Micron",
        "watch_metric": "revenue_growth",
        "impacts": ["NVDA", "SMCI", "DELL", "HPE", "WDC"],
        "signal_logic": {
            "strong":  "HBM demand exceeding supply. AI server memory content rising. Bullish for GPU server and data centre names.",
            "inline":  "HBM demand steady. Memory cycle neutral.",
            "weak":    "HBM pricing under pressure. Could signal AI server build rate slowing."
        },
        "strong_threshold": 0.25,
        "weak_threshold":   0.05,
    },
    "VRT": {
        "name": "Vertiv",
        "watch_metric": "revenue_growth",
        "impacts": ["ETN", "PWR", "HUBB", "CEG", "VST", "NRG"],
        "signal_logic": {
            "strong":  "Data centre power orders surging. Backlog building. Leading indicator for energy demand. Bullish for power and utilities.",
            "inline":  "Power infrastructure demand steady. Neutral for energy names.",
            "weak":    "Power order softness. Could signal data centre buildout pause. Negative for utilities."
        },
        "strong_threshold": 0.15,
        "weak_threshold":   0.05,
    },
    "SNOW": {
        "name": "Snowflake",
        "watch_metric": "revenue_growth",
        "impacts": ["AVGO", "ANET", "CSCO", "COHR", "CIEN"],
        "signal_logic": {
            "strong":  "Data cloud workloads accelerating. AI query volume rising. Bullish for networking and optical connectivity.",
            "inline":  "Data growth steady. Networking demand neutral.",
            "weak":    "Data workload slowdown. Could signal reduced networking demand."
        },
        "strong_threshold": 0.20,
        "weak_threshold":   0.08,
    },
    "ANET": {
        "name": "Arista Networks",
        "watch_metric": "revenue_growth",
        "impacts": ["COHR", "LITE", "CIEN", "CSCO", "VIAV"],
        "signal_logic": {
            "strong":  "Data centre switching demand strong. AI cluster networking spend accelerating. Bullish for optical names.",
            "inline":  "Networking demand intact. Neutral for optical.",
            "weak":    "Switching demand softening. Negative for optical connectivity."
        },
        "strong_threshold": 0.15,
        "weak_threshold":   0.05,
    },
    "CEG": {
        "name": "Constellation Energy",
        "watch_metric": "revenue_growth",
        "impacts": ["VST", "NRG", "NEE", "CCJ", "SO"],
        "signal_logic": {
            "strong":  "Nuclear PPA deals with hyperscalers confirmed. Long-term power demand locked in. Bullish for all clean energy names.",
            "inline":  "Power demand steady. Neutral for utilities.",
            "weak":    "PPA deal flow slowing. Could signal hyperscaler power demand moderation."
        },
        "strong_threshold": 0.10,
        "weak_threshold":   0.02,
    },
}

# =============================================================
# SIGNAL GENERATOR
# =============================================================
def generate_readthrough_signals():
    """
    For each stock in the read-through matrix:
    1. Pull current and prior quarter revenue
    2. Calculate QoQ and YoY growth
    3. Classify as strong / inline / weak
    4. Generate signals for impacted stocks
    """

    signals = []
    signal_map = {}  # ticker → list of signals pointing at it

    print("Generating read-through signals...")

    for ticker, rules in READ_THROUGH_RULES.items():
        try:
            t    = yf.Ticker(ticker)
            info = t.info

            # Current revenue growth YoY
            rev_growth = float(info.get("revenueGrowth", 0) or 0)

            # Classify signal strength
            if rev_growth >= rules["strong_threshold"]:
                strength  = "strong"
                direction = "BULLISH"
                color     = "green"
                arrow     = "▲"
            elif rev_growth <= rules["weak_threshold"]:
                strength  = "weak"
                direction = "BEARISH"
                color     = "red"
                arrow     = "▼"
            else:
                strength  = "inline"
                direction = "NEUTRAL"
                color     = "gray"
                arrow     = "→"

            signal_text = rules["signal_logic"][strength]
            impacted    = rules["impacts"]

            # Only generate actionable signals (not neutral)
            if strength != "inline":
                signal = {
                    "reporter":       ticker,
                    "reporter_name":  rules["name"],
                    "rev_growth_pct": round(rev_growth * 100, 1),
                    "strength":       strength,
                    "direction":      direction,
                    "color":          color,
                    "arrow":          arrow,
                    "signal_text":    signal_text,
                    "impacts":        impacted,
                    "generated":      datetime.today().strftime("%Y-%m-%d"),
                }
                signals.append(signal)

                # Map signals to impacted tickers
                for imp in impacted:
                    if imp not in signal_map:
                        signal_map[imp] = []
                    signal_map[imp].append({
                        "from":       ticker,
                        "from_name":  rules["name"],
                        "direction":  direction,
                        "signal":     signal_text,
                        "rev_growth": round(rev_growth * 100, 1),
                    })

            print(f"  {ticker}: {round(rev_growth*100,1)}% → {direction} → impacts {impacted}")

        except Exception as e:
            print(f"  ⚠️ Error {ticker}: {e}")
            continue

    # Sort: bullish first, then bearish
    signals_sorted = (
        [s for s in signals if s["direction"] == "BULLISH"] +
        [s for s in signals if s["direction"] == "BEARISH"]
    )

    return signals_sorted, signal_map


def get_stock_signal_summary(ticker, signal_map):
    """
    For a given stock, return all read-through signals pointing at it.
    Used in Company Detail tab.
    """
    return signal_map.get(ticker, [])


if __name__ == "__main__":
    signals, signal_map = generate_readthrough_signals()

    print(f"\n{'='*60}")
    print(f"  LIVE READ-THROUGH SIGNALS — {datetime.today().strftime('%Y-%m-%d')}")
    print(f"{'='*60}")

    print(f"\n  BULLISH SIGNALS:")
    for s in [x for x in signals if x["direction"] == "BULLISH"]:
        print(f"  {s['arrow']} {s['reporter']} ({s['rev_growth_pct']}% rev gr)")
        print(f"    → Impacts: {', '.join(s['impacts'])}")
        print(f"    → {s['signal_text'][:80]}...")
        print()

    print(f"\n  BEARISH SIGNALS:")
    for s in [x for x in signals if x["direction"] == "BEARISH"]:
        print(f"  {s['arrow']} {s['reporter']} ({s['rev_growth_pct']}% rev gr)")
        print(f"    → Impacts: {', '.join(s['impacts'])}")
        print(f"    → {s['signal_text'][:80]}...")
        print()

    print(f"\n  SIGNAL MAP (what signals point at each stock):")
    for ticker, sigs in sorted(signal_map.items()):
        directions = [s["direction"] for s in sigs]
        bull = directions.count("BULLISH")
        bear = directions.count("BEARISH")
        net  = "🟢 NET BULLISH" if bull > bear else ("🔴 NET BEARISH" if bear > bull else "⚪ MIXED")
        print(f"  {ticker:<6} {net}  ({bull} bullish, {bear} bearish signals)")
