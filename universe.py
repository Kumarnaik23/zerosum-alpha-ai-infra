# =============================================================
# ZEROSUM ALPHA — Full AI Infrastructure Universe v2
# 60+ stocks across 12 subsectors
# =============================================================

AI_INFRA_UNIVERSE = {

    # ==========================================================
    # 1. AI SILICON — Core GPU/CPU/ASIC designers
    # ==========================================================
    "NVDA":  {"name": "Nvidia",              "subsector": "AI Silicon",        "region": "US"},
    "AVGO":  {"name": "Broadcom",            "subsector": "AI Silicon",        "region": "US"},
    "AMD":   {"name": "AMD",                 "subsector": "AI Silicon",        "region": "US"},
    "MRVL":  {"name": "Marvell Technology",  "subsector": "AI Silicon",        "region": "US"},
    "QCOM":  {"name": "Qualcomm",            "subsector": "AI Silicon",        "region": "US"},
    "ARM":   {"name": "ARM Holdings",        "subsector": "AI Silicon",        "region": "US"},
    "INTC":  {"name": "Intel",               "subsector": "AI Silicon",        "region": "US"},
    "MPWR":  {"name": "Monolithic Power",    "subsector": "AI Silicon",        "region": "US"},

    # ==========================================================
    # 2. SEMICONDUCTOR EQUIPMENT — Tools to make AI chips
    # ==========================================================
    "ASML":  {"name": "ASML",                "subsector": "Semiconductor Equipment", "region": "EU"},
    "AMAT":  {"name": "Applied Materials",   "subsector": "Semiconductor Equipment", "region": "US"},
    "KLAC":  {"name": "KLA Corporation",     "subsector": "Semiconductor Equipment", "region": "US"},
    "LRCX":  {"name": "Lam Research",        "subsector": "Semiconductor Equipment", "region": "US"},
    "ONTO":  {"name": "Onto Innovation",     "subsector": "Semiconductor Equipment", "region": "US"},
    "UCTT":  {"name": "Ultra Clean Holdings","subsector": "Semiconductor Equipment", "region": "US"},

    # ==========================================================
    # 3. FOUNDRY — Manufacturing AI chips
    # ==========================================================
    "TSM":   {"name": "TSMC",               "subsector": "Foundry",           "region": "Asia"},
    "GFS":   {"name": "GlobalFoundries",    "subsector": "Foundry",           "region": "US"},

    # ==========================================================
    # 4. MEMORY & STORAGE — HBM, DRAM, NAND for AI
    # ==========================================================
    "MU":    {"name": "Micron Technology",  "subsector": "Memory & Storage",  "region": "US"},
    "WDC":   {"name": "Western Digital",    "subsector": "Memory & Storage",  "region": "US"},
    "STXS":  {"name": "Seagate Technology", "subsector": "Memory & Storage",  "region": "US"},

    # ==========================================================
    # 5. NETWORKING — Connecting AI clusters
    # ==========================================================
    "ANET":  {"name": "Arista Networks",    "subsector": "Networking",        "region": "US"},
    "CSCO":  {"name": "Cisco",              "subsector": "Networking",        "region": "US"},
    "VIAV":  {"name": "Viavi Solutions",    "subsector": "Networking",        "region": "US"},
    "CIEN":  {"name": "Ciena",              "subsector": "Networking",        "region": "US"},

    # ==========================================================
    # 6. AI SERVER & DATA CENTRE INFRASTRUCTURE
    # ==========================================================
    "SMCI":  {"name": "Super Micro Computer","subsector": "AI Server Systems", "region": "US"},
    "DELL":  {"name": "Dell Technologies",  "subsector": "AI Server Systems", "region": "US"},
    "HPE":   {"name": "HPE",               "subsector": "AI Server Systems", "region": "US"},
    "NTAP":  {"name": "NetApp",            "subsector": "AI Server Systems", "region": "US"},
    "PSTG":  {"name": "Pure Storage",      "subsector": "AI Server Systems", "region": "US"},

    # ==========================================================
    # 7. POWER & COOLING — Energy for AI data centres
    # ==========================================================
    "VRT":   {"name": "Vertiv Holdings",    "subsector": "Power & Cooling",   "region": "US"},
    "ETN":   {"name": "Eaton",             "subsector": "Power & Cooling",   "region": "US"},
    "PWR":   {"name": "Quanta Services",   "subsector": "Power & Cooling",   "region": "US"},
    "HUBB":  {"name": "Hubbell",           "subsector": "Power & Cooling",   "region": "US"},
    "AME":   {"name": "AMETEK",            "subsector": "Power & Cooling",   "region": "US"},
    "GNRC":  {"name": "Generac Holdings",  "subsector": "Power & Cooling",   "region": "US"},

    # ==========================================================
    # 8. ENERGY / POWER GENERATION — Powering data centres
    # ==========================================================
    "CEG":   {"name": "Constellation Energy","subsector": "Energy & Power",   "region": "US"},
    "VST":   {"name": "Vistra Energy",      "subsector": "Energy & Power",   "region": "US"},
    "NRG":   {"name": "NRG Energy",         "subsector": "Energy & Power",   "region": "US"},
    "NEE":   {"name": "NextEra Energy",     "subsector": "Energy & Power",   "region": "US"},
    "SO":    {"name": "Southern Company",   "subsector": "Energy & Power",   "region": "US"},
    "DUK":   {"name": "Duke Energy",        "subsector": "Energy & Power",   "region": "US"},
    "CCJ":   {"name": "Cameco",            "subsector": "Energy & Power",   "region": "US"},  # Uranium

    # ==========================================================
    # 9. CLOUD HYPERSCALERS — Building AI infrastructure
    # ==========================================================
    "MSFT":  {"name": "Microsoft",         "subsector": "Cloud Hyperscaler", "region": "US"},
    "AMZN":  {"name": "Amazon",            "subsector": "Cloud Hyperscaler", "region": "US"},
    "GOOGL": {"name": "Alphabet",          "subsector": "Cloud Hyperscaler", "region": "US"},
    "META":  {"name": "Meta",              "subsector": "Cloud Hyperscaler", "region": "US"},

    # ==========================================================
    # 10. SPECIALIZED AI CLOUD — Pure-play AI compute
    # ==========================================================
    "ORCL":  {"name": "Oracle",            "subsector": "Specialized AI Cloud", "region": "US"},
    "CRWV":  {"name": "CoreWeave",         "subsector": "Specialized AI Cloud", "region": "US"},
    "SNOW":  {"name": "Snowflake",         "subsector": "Specialized AI Cloud", "region": "US"},
    "PLTR":  {"name": "Palantir",          "subsector": "Specialized AI Cloud", "region": "US"},

    # ==========================================================
    # 11. OPTICAL CONNECTIVITY — High-speed data centre links
    # ==========================================================
    "LITE":  {"name": "Lumentum Holdings", "subsector": "Optical Connectivity", "region": "US"},
    "COHR":  {"name": "Coherent Corp",     "subsector": "Optical Connectivity", "region": "US"},
    "IIVI":  {"name": "II-VI / Coherent",  "subsector": "Optical Connectivity", "region": "US"},
    "FNSR":  {"name": "Finisar / II-VI",   "subsector": "Optical Connectivity", "region": "US"},
    "AAOI":  {"name": "Applied Optoelectronics","subsector": "Optical Connectivity","region": "US"},

    # ==========================================================
    # 12. AI SOFTWARE & OBSERVABILITY — Running AI infrastructure
    # ==========================================================
    "DDOG":  {"name": "Datadog",           "subsector": "AI Observability",  "region": "US"},
    "NET":   {"name": "Cloudflare",        "subsector": "AI Observability",  "region": "US"},
    "GTLB":  {"name": "GitLab",            "subsector": "AI Observability",  "region": "US"},
    "MDB":   {"name": "MongoDB",           "subsector": "AI Observability",  "region": "US"},
    "ESTC":  {"name": "Elastic",           "subsector": "AI Observability",  "region": "US"},

}

# ==========================================================
# AI EXPOSURE SCORES — manually curated, update quarterly
# Scale: 0-20, reflects % of revenue/growth tied to AI infra
# ==========================================================
AI_EXPOSURE_SCORES = {
    # AI Silicon
    "NVDA": 20, "AVGO": 19, "MRVL": 18, "AMD": 16, "ARM": 18,
    "QCOM": 13, "INTC": 10, "MPWR": 16,

    # Semiconductor Equipment
    "ASML": 16, "AMAT": 15, "KLAC": 14, "LRCX": 14,
    "ONTO": 13, "UCTT": 12,

    # Foundry
    "TSM": 18, "GFS": 11,

    # Memory & Storage
    "MU": 16, "WDC": 12, "STXS": 10,

    # Networking
    "ANET": 17, "CSCO": 12, "VIAV": 11, "CIEN": 13,

    # AI Server Systems
    "SMCI": 18, "DELL": 13, "HPE": 12, "NTAP": 11, "PSTG": 13,

    # Power & Cooling
    "VRT": 17, "ETN": 14, "PWR": 13, "HUBB": 12, "AME": 11, "GNRC": 10,

    # Energy & Power
    "CEG": 15, "VST": 14, "NRG": 12, "NEE": 11, "SO": 9, "DUK": 9, "CCJ": 13,

    # Cloud Hyperscaler
    "MSFT": 14, "AMZN": 13, "GOOGL": 13, "META": 14,

    # Specialized AI Cloud
    "ORCL": 15, "CRWV": 19, "SNOW": 15, "PLTR": 16,

    # Optical Connectivity
    "LITE": 15, "COHR": 14, "IIVI": 13, "FNSR": 12, "AAOI": 14,

    # AI Observability
    "DDOG": 16, "NET": 14, "GTLB": 13, "MDB": 13, "ESTC": 12,
}

# ==========================================================
# EARNINGS READ-THROUGH MATRIX
# When X reports → signals for Y
# ==========================================================
EARNINGS_READ_THROUGH = {
    "MSFT": {
        "signal": "Azure AI growth rate and capex guidance",
        "impacts": ["NVDA", "AVGO", "MRVL", "VRT", "SMCI", "ANET"],
        "logic": "Azure capex = GPU orders = networking demand"
    },
    "GOOGL": {
        "signal": "GCP growth and TPU/custom silicon commentary",
        "impacts": ["NVDA", "AVGO", "TSM", "VRT", "ANET"],
        "logic": "Google capex signals hyperscaler AI infra cycle health"
    },
    "AMZN": {
        "signal": "AWS revenue growth and Trainium/Inferentia commentary",
        "impacts": ["NVDA", "AVGO", "MU", "SMCI", "VRT"],
        "logic": "AWS custom silicon + GPU orders drive supply chain"
    },
    "META": {
        "signal": "AI infra capex guidance and Llama training compute",
        "impacts": ["NVDA", "AVGO", "ANET", "VRT", "ETN"],
        "logic": "Meta is top-3 GPU buyer globally"
    },
    "DELL": {
        "signal": "PowerEdge AI server backlog and ISG revenue",
        "impacts": ["NVDA", "MU", "AVGO", "SMCI"],
        "logic": "Dell AI server demand = GPU + memory + networking pull"
    },
    "SNOW": {
        "signal": "Data cloud growth and AI workload commentary",
        "impacts": ["AVGO", "ANET", "CSCO", "COHR"],
        "logic": "Data movement growth = networking and optical demand"
    },
    "TSM": {
        "signal": "Advanced node utilization and CoWoS packaging capacity",
        "impacts": ["NVDA", "AMD", "AVGO", "ASML", "AMAT"],
        "logic": "TSMC utilization = leading indicator for chip demand cycle"
    },
    "MU": {
        "signal": "HBM pricing, capacity, and hyperscaler demand",
        "impacts": ["NVDA", "SMCI", "DELL", "HPE"],
        "logic": "HBM demand = GPU server build rate"
    },
    "NVDA": {
        "signal": "Data center revenue, Blackwell shipments, guidance",
        "impacts": ["SMCI", "DELL", "VRT", "ANET", "MU", "TSM"],
        "logic": "NVDA is the master signal for the entire AI infra supply chain"
    },
    "AVGO": {
        "signal": "Custom ASIC revenue, AI networking, hyperscaler wins",
        "impacts": ["ANET", "COHR", "LITE", "TSM"],
        "logic": "Broadcom custom silicon wins = TSMC orders + optical demand"
    },
    "VRT": {
        "signal": "Data centre power orders and backlog",
        "impacts": ["ETN", "PWR", "HUBB", "CEG", "VST"],
        "logic": "Power infrastructure orders lead energy demand by 6-12 months"
    },
    "CEG": {
        "signal": "Nuclear PPA deals with hyperscalers",
        "impacts": ["VST", "NRG", "NEE", "CCJ"],
        "logic": "Nuclear PPA deals signal long-term hyperscaler power commitments"
    },
    "PLTR": {
        "signal": "US government AI contracts and enterprise AI revenue",
        "impacts": ["NVDA", "DDOG", "NET", "MSFT"],
        "logic": "Government AI spend = infrastructure procurement signal"
    },
    "DDOG": {
        "signal": "AI observability growth and GPU cluster monitoring",
        "impacts": ["NET", "SNOW", "MDB", "ESTC"],
        "logic": "AI workload monitoring growth = AI deployment acceleration"
    },
}

# ==========================================================
# MACRO SIGNALS TO TRACK
# ==========================================================
MACRO_TICKERS = {
    "^SOX":    "Philadelphia Semiconductor Index",
    "^VIX":    "VIX Volatility Index",
    "^TNX":    "US 10Y Treasury Yield",
    "^NDX":    "Nasdaq 100",
    "SPY":     "S&P 500 ETF",
    "SOXX":    "iShares Semiconductor ETF",
    "HG=F":    "Copper Futures",
    "DX-Y.NYB":"US Dollar Index",
    "GC=F":    "Gold Futures",
    "CL=F":    "Crude Oil Futures",
}

# ==========================================================
# AI INFRASTRUCTURE ETFs — for benchmarking
# ==========================================================
AI_ETFS = {
    "BOTZ":  "Global X Robotics & AI ETF",
    "ROBO":  "ROBO Global Robotics ETF",
    "SOXX":  "iShares Semiconductor ETF",
    "SMH":   "VanEck Semiconductor ETF",
    "FTEC":  "Fidelity MSCI IT ETF",
    "IGV":   "iShares Expanded Tech-Software ETF",
    "WCLD":  "WisdomTree Cloud Computing ETF",
}

if __name__ == "__main__":
    print("ZeroSum Alpha — AI Infrastructure Universe")
    print(f"Total stocks: {len(AI_INFRA_UNIVERSE)}")
    print("")
    
    # Count by subsector
    subsectors = {}
    for t, m in AI_INFRA_UNIVERSE.items():
        s = m["subsector"]
        subsectors[s] = subsectors.get(s, 0) + 1
    
    print("Subsector breakdown:")
    for s, count in sorted(subsectors.items(), key=lambda x: -x[1]):
        print(f"  {s:<30} {count} stocks")
    
    print("")
    print(f"Read-through relationships: {len(EARNINGS_READ_THROUGH)}")
    print(f"Macro signals: {len(MACRO_TICKERS)}")
    print(f"AI ETFs tracked: {len(AI_ETFS)}")
