"""
Claims Efficiency Analysis - Chart Generation
Generates professional dark-theme visualizations for claims processing KPIs.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────
OUTPUT_DIR = Path(__file__).parent
DATA_PATH = OUTPUT_DIR.parent / "data" / "processed" / "claims_efficiency_clean.csv"

BG = "#1a1a2e"
CARD_BG = "#16213e"
TEXT = "#e0e0e0"
ACCENT = ["#00b4d8", "#90e0ef", "#f72585", "#7209b7", "#4cc9f0", "#fca311"]

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": CARD_BG,
    "axes.edgecolor": "#334155",
    "axes.labelcolor": TEXT,
    "xtick.color": TEXT,
    "ytick.color": TEXT,
    "text.color": TEXT,
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "grid.color": "#334155",
    "grid.alpha": 0.4,
})

# ── Load data ───────────────────────────────────────────────────────────
df = pd.read_csv(DATA_PATH, parse_dates=["service_date", "submitted_date", "decision_date"])
df["month"] = df["service_date"].dt.to_period("M")

# ═══════════════════════════════════════════════════════════════════════
# Chart 1 — Processing Turnaround Time by Service Line
# ═══════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 6))
tat = df.groupby("service_line")["processing_days"].agg(["mean", "median"]).sort_values("mean", ascending=True)

y = np.arange(len(tat))
bar_h = 0.35
ax.barh(y + bar_h / 2, tat["mean"], bar_h, color=ACCENT[0], label="Mean", zorder=3)
ax.barh(y - bar_h / 2, tat["median"], bar_h, color=ACCENT[1], label="Median", zorder=3)

for i, (m, md) in enumerate(zip(tat["mean"], tat["median"])):
    ax.text(m + 0.5, i + bar_h / 2, f"{m:.1f}d", va="center", fontsize=9, color=TEXT)
    ax.text(md + 0.5, i - bar_h / 2, f"{md:.0f}d", va="center", fontsize=9, color=TEXT)

ax.set_yticks(y)
ax.set_yticklabels(tat.index)
ax.set_xlabel("Processing Days")
ax.set_title("Claims Processing Turnaround Time by Service Line")
ax.legend(loc="lower right", framealpha=0.3)
ax.grid(axis="x", linestyle="--")
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "turnaround_time_by_service_line.png", dpi=180)
plt.close(fig)
print("  [1/4] turnaround_time_by_service_line.png")

# ═══════════════════════════════════════════════════════════════════════
# Chart 2 — Denial Rate by Reason
# ═══════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 6))
denied = df[df["is_denied"] == 1]
reason_counts = denied["denial_reason"].value_counts()
total_claims = len(df)

colors = [ACCENT[i % len(ACCENT)] for i in range(len(reason_counts))]
bars = ax.bar(range(len(reason_counts)), reason_counts.values, color=colors, zorder=3)

for bar, val in zip(bars, reason_counts.values):
    pct = val / total_claims * 100
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 8,
            f"{val:,}\n({pct:.1f}%)", ha="center", va="bottom", fontsize=9, color=TEXT)

ax.set_xticks(range(len(reason_counts)))
ax.set_xticklabels(reason_counts.index, rotation=30, ha="right", fontsize=9)
ax.set_ylabel("Denied Claims Count")
ax.set_title("Denial Volume and Rate by Reason Category")
ax.grid(axis="y", linestyle="--")
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "denial_rates_by_reason.png", dpi=180)
plt.close(fig)
print("  [2/4] denial_rates_by_reason.png")

# ═══════════════════════════════════════════════════════════════════════
# Chart 3 — Monthly Claims Volume Trends
# ═══════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(12, 5))
monthly = df.groupby("month").agg(
    total=("claim_id", "count"),
    approved=("is_approved", "sum"),
    denied=("is_denied", "sum"),
    reworked=("is_reworked", "sum"),
).sort_index()

x = range(len(monthly))
labels = [str(p) for p in monthly.index]

ax.fill_between(x, monthly["total"], alpha=0.15, color=ACCENT[0])
ax.plot(x, monthly["total"], "-o", color=ACCENT[0], label="Total", markersize=5, linewidth=2)
ax.plot(x, monthly["approved"], "-s", color=ACCENT[1], label="Approved", markersize=4, linewidth=1.5)
ax.plot(x, monthly["denied"], "-^", color=ACCENT[2], label="Denied", markersize=4, linewidth=1.5)
ax.plot(x, monthly["reworked"], "-D", color=ACCENT[3], label="Reworked", markersize=4, linewidth=1.5)

ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
ax.set_ylabel("Claims Count")
ax.set_title("Monthly Claims Volume Trends")
ax.legend(loc="upper left", framealpha=0.3)
ax.grid(axis="y", linestyle="--")
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "monthly_claims_volume.png", dpi=180)
plt.close(fig)
print("  [3/4] monthly_claims_volume.png")

# ═══════════════════════════════════════════════════════════════════════
# Chart 4 — KPI Dashboard Summary
# ═══════════════════════════════════════════════════════════════════════
total = len(df)
denial_rate = df["is_denied"].mean() * 100
clean_claim_rate = (df["touch_count"] == 1).mean() * 100
rework_rate = df["is_reworked"].mean() * 100
avg_tat = df["processing_days"].mean()
paid_to_billed = (df["paid_amount"].sum() / df["billed_amount"].sum()) * 100
allowed_to_billed = (df["allowed_amount"].sum() / df["billed_amount"].sum()) * 100

kpis = [
    ("Total Claims", f"{total:,}", None),
    ("Clean Claim Rate", f"{clean_claim_rate:.1f}%", clean_claim_rate),
    ("Denial Rate", f"{denial_rate:.1f}%", denial_rate),
    ("Rework Rate", f"{rework_rate:.1f}%", rework_rate),
    ("Avg Processing Days", f"{avg_tat:.1f}", None),
    ("Paid-to-Billed Ratio", f"{paid_to_billed:.1f}%", paid_to_billed),
]

fig, axes = plt.subplots(2, 3, figsize=(14, 6))
axes = axes.flatten()

card_colors = [ACCENT[0], ACCENT[4], ACCENT[2], ACCENT[3], ACCENT[1], ACCENT[5]]

for i, (title, value, pct) in enumerate(kpis):
    ax = axes[i]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])

    # accent bar at top
    ax.axhline(y=0.98, xmin=0.05, xmax=0.95, color=card_colors[i], linewidth=4)

    ax.text(0.5, 0.62, value, ha="center", va="center", fontsize=26, fontweight="bold", color=card_colors[i])
    ax.text(0.5, 0.28, title, ha="center", va="center", fontsize=11, color=TEXT)

fig.suptitle("Claims Efficiency KPI Dashboard", fontsize=16, fontweight="bold", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(OUTPUT_DIR / "kpi_dashboard.png", dpi=180)
plt.close(fig)
print("  [4/4] kpi_dashboard.png")

print("\nAll charts saved to:", OUTPUT_DIR)
