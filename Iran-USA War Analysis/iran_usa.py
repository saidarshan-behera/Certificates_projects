import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
import os

os.makedirs('charts', exist_ok=True)

# ── Colour palette ────────────────────────────────────────────
DARK_BG = '#1a1a1a'
RED     = '#8b1a1a'
RED2    = '#c0392b'
GOLD    = '#c8a96e'
BLUE    = '#3498db'
ORANGE  = '#e67e22'
GREEN   = '#27ae60'
PURPLE  = '#9b59b6'
LIGHT   = '#faf8f4'
MUTED   = '#555555'


def style_dark(ax, fig):
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor('#111111')
    ax.tick_params(colors='#aaaaaa', labelsize=9)
    for s in ['bottom', 'left']:
        ax.spines[s].set_color('#333333')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', color='#222222', linewidth=0.6)


def style_light(ax, fig):
    fig.patch.set_facecolor(LIGHT)
    ax.set_facecolor('#ffffff')
    ax.tick_params(colors=MUTED, labelsize=9)
    for s in ['bottom', 'left']:
        ax.spines[s].set_color('#e0d8cc')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', color='#f0ebe0', linewidth=0.8)


def title(ax, fig, t, sub, dark=False):
    tc = GOLD if dark else RED
    sc = '#aaaaaa' if dark else MUTED
    fig.text(0.05, 0.97, t,   fontsize=11, fontweight='bold', color=tc, va='top')
    fig.text(0.05, 0.91, sub, fontsize=8,  color=sc,          va='top', style='italic')


def save(fig, name):
    fig.savefig(f'charts/{name}.png', dpi=150, bbox_inches='tight', pad_inches=0.15)
    plt.close(fig)
    print(f'  ✔  charts/{name}.png')


# ── Chart 1 — Escalation severity ────────────────────────────
fig, ax = plt.subplots(figsize=(9, 3.8))
style_light(ax, fig)
labels = ['9/11\nEra','Axis of\nEvil','Iraq\nWar','Nuke\nReveal','JCPOA\n2015',
          'Trump\nExit','Soleimani\nKilled','Uranium\n83%','Oct 7\n/Gaza',
          'April\nExchange','12-Day\nWar','Open\nWar\n2026']
values = [4, 5, 5, 6, 2, 7, 8, 7, 9, 8, 9, 10]
colors = [RED if v >= 9 else RED2 if v >= 7 else ORANGE if v >= 5 else GOLD for v in values]
bars = ax.bar(labels, values, color=colors, width=0.65, zorder=3)
ax.set_ylim(0, 11)
ax.set_ylabel('Severity (1–10)', fontsize=9, color=MUTED)
for bar, v in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, v + 0.15, str(v),
            ha='center', va='bottom', fontsize=8.5, color=MUTED, fontweight='bold')
title(ax, fig, 'US–Iran Escalation Events: 2001–2026',
      'Severity score: 1 = diplomatic incident, 10 = open warfare')
plt.tight_layout(rect=[0, 0, 1, 0.88])
save(fig, 'chart1_escalation')


# ── Chart 2 — Uranium enrichment % ───────────────────────────
fig, ax = plt.subplots(figsize=(9, 3.8))
style_dark(ax, fig)
years   = [2013,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026]
enrich  = [20, 3.67,3.67,3.67,3.67,4.5, 20,  60,  60,  83.7,84,  89,  90]
ax.fill_between(years, enrich, alpha=0.15, color=GOLD)
ax.plot(years, enrich, color=GOLD, linewidth=2.5, zorder=3)
ax.scatter(years, enrich,
           color=[RED if v >= 89 else GOLD for v in enrich], s=40, zorder=4)
ax.axhline(3.67, color='#2ecc71', linestyle='--', linewidth=1.4, alpha=0.7,
           label='JCPOA Cap (3.67%)')
ax.axhline(90,   color='#e74c3c', linestyle='--', linewidth=1.4, alpha=0.6,
           label='Weapons-grade (90%)')
ax.set_ylim(0, 105)
ax.set_ylabel('Enrichment %', fontsize=9, color='#aaa')
ax.set_xticks(years)
ax.set_xticklabels([str(y) for y in years], rotation=35, ha='right')
ax.legend(fontsize=8, facecolor='#1a1a1a', edgecolor='#333', labelcolor='#ccc')
ax.annotate('JCPOA\nsigned', xy=(2015,3.67), xytext=(2015.3,18),
            color='#2ecc71', fontsize=7.5,
            arrowprops=dict(arrowstyle='->', color='#2ecc71', lw=1))
ax.annotate('Trump\nwithdraws', xy=(2018,3.67), xytext=(2018.3,18),
            color=GOLD, fontsize=7.5,
            arrowprops=dict(arrowstyle='->', color=GOLD, lw=1))
title(ax, fig, "Iran's Uranium Enrichment Level — 2013 to 2026",
      'IAEA quarterly reports. Red dot = weapons-grade threshold reached.', dark=True)
plt.tight_layout(rect=[0, 0, 1, 0.88])
save(fig, 'chart2_uranium')


# ── Chart 3 — Enriched uranium stockpile ─────────────────────
fig, ax = plt.subplots(figsize=(9, 3.8))
style_light(ax, fig)
xlabels = ['2016\nJCPOA','2018\nUS exits','2019','2020','2021',
           '2022','2023','2024','Post\nJun 2025','Feb\n2026']
low  = [202, 202, 372, 2105, 2105, 3760, 4700, 5525, 1200, 1800]
high = [0,   0,   0,   0,    17,   43,   121,   188,   60,  120]
x = np.arange(len(xlabels))
ax.bar(x, low,  0.55, label='Low-enriched uranium (kg)',    color=BLUE,  zorder=3)
ax.bar(x, high, 0.55, bottom=low, label='Highly-enriched uranium (kg)', color=RED, zorder=3)
ax.axhline(202, color=GREEN, linestyle='--', linewidth=1.5, alpha=0.8,
           label='JCPOA limit (202 kg)')
ax.set_xticks(x)
ax.set_xticklabels(xlabels, fontsize=8.5)
ax.set_ylabel('Kilograms', fontsize=9, color=MUTED)
ax.legend(fontsize=8)
title(ax, fig, "Iran's Enriched Uranium Stockpile — 2016 to 2026",
      'Dark red = highly enriched (60%+). JCPOA permitted only 202 kg total.')
plt.tight_layout(rect=[0, 0, 1, 0.88])
save(fig, 'chart3_stockpile')


# ── Chart 4 — Proxy network capability ───────────────────────
fig, ax = plt.subplots(figsize=(9, 3.8))
style_light(ax, fig)
proxies = ['Hezbollah\n(Lebanon)','Hamas\n(Gaza)','Houthis\n(Yemen)',
           'PMF Militias\n(Iraq)','Syria\nNetworks']
before = [88, 62, 55, 50, 44]
after  = [18,  9, 35, 28, 20]
y = np.arange(len(proxies))
h = 0.35
ax.barh(y + h/2, before, h, label='Before Oct 2023', color=RED2, zorder=3)
ax.barh(y - h/2, after,  h, label='February 2026',   color=GOLD, zorder=3)
ax.set_yticks(y)
ax.set_yticklabels(proxies, fontsize=9)
ax.set_xlabel('Capability Index (0–100)', fontsize=9, color=MUTED)
ax.set_xlim(0, 100)
ax.legend(fontsize=9)
ax.grid(axis='x', color='#f0ebe0', linewidth=0.8)
ax.grid(axis='y', visible=False)
title(ax, fig, "Iran's Proxy Network Capability — Before vs. Now",
      'Index based on manpower, weapons, and territorial control estimates.')
plt.tight_layout(rect=[0, 0, 1, 0.88])
save(fig, 'chart4_proxy')


# ── Chart 5 — Casualties ──────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 3.6))
style_dark(ax, fig)
cats = ['Protest deaths\n(Govt. figure)','Protest deaths\n(HR orgs. est.)',
        'War deaths\n(Day 10)','War wounded\n(Day 10)']
vals = [3000, 38000, 1300, 6200]
bars = ax.bar(cats, vals,
              color=[ORANGE, RED, RED2, GOLD], width=0.55, zorder=3)
for bar, v in zip(bars, vals):
    ax.text(bar.get_x() + bar.get_width()/2, v + 400,
            f'{v:,}', ha='center', va='bottom',
            fontsize=9, color='#ccc', fontweight='bold')
ax.set_ylabel('Number of people', fontsize=9, color='#aaa')
ax.yaxis.set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
title(ax, fig, 'Casualties: 2025–26 Protests & War (First 10 Days)',
      'HR org. figures differ significantly from Iranian government figures.', dark=True)
plt.tight_layout(rect=[0, 0, 1, 0.88])
save(fig, 'chart5_casualties')


# ── Chart 6 — Iran economy ────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 3.8))
style_light(ax, fig)
years    = list(range(2018, 2027))
inflation = [100,141,196,243,295,390,480,610,720]
rial      = [100, 45, 30, 28, 22, 15, 10,  5,  3]
unemp     = [ 14, 17, 18, 17, 16, 18, 21, 28, 34]
ax2 = ax.twinx()
ax.plot(years, inflation, color=RED2,   linewidth=2.5, marker='o', markersize=4,
        label='Inflation Index (2018=100)')
ax.plot(years, rial,      color=BLUE,   linewidth=2.5, marker='s', markersize=4,
        label='Rial Value Index (lower = worse)')
ax2.plot(years, unemp,   color=ORANGE, linewidth=2,   linestyle='--', marker='^',
         markersize=4, label='Unemployment % (RHS)')
ax.set_ylabel('Index (2018 = 100)', fontsize=9, color=MUTED)
ax2.set_ylabel('Unemployment %',    fontsize=9, color=ORANGE)
ax2.tick_params(colors=ORANGE, labelsize=9)
ax2.spines['right'].set_color(ORANGE)
ax2.spines['top'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.spines['left'].set_visible(False)
lines1, l1 = ax.get_legend_handles_labels()
lines2, l2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, l1 + l2, fontsize=8, loc='upper left')
title(ax, fig, "Iran's Economic Collapse: Key Indicators (2018–2026)",
      'Sanctions reimposed in 2018 after Trump JCPOA withdrawal.')
plt.tight_layout(rect=[0, 0, 1, 0.88])
save(fig, 'chart6_economy')


# ── Chart 7 — Oil price ───────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 3.6))
style_dark(ax, fig)
months = ["Jan\n'25",'Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct',
          'Nov','Dec',"Jan\n'26",'Mid\nFeb','Feb 28\nWar','Mar 3','Mar 7','Mar 10']
prices = [77,76,78,80,79,81,80,82,84,83,85,86,88,94,108,113,117,115]
x = np.arange(len(months))
ax.fill_between(x, prices, alpha=0.2, color=GOLD)
ax.plot(x, prices, color=GOLD, linewidth=2.5, zorder=3)
ax.scatter(x, prices, color=GOLD, s=25, zorder=4)
ax.axvline(14, color='#e74c3c', linestyle='--', linewidth=1.2, alpha=0.7)
ax.text(14.1, 80, 'War starts', color='#e74c3c', fontsize=8)
ax.set_xticks(x)
ax.set_xticklabels(months, fontsize=8)
ax.set_ylabel('USD per barrel', fontsize=9, color='#aaa')
title(ax, fig, 'Brent Crude Oil Price — Jan 2025 to Mar 10, 2026',
      'Strait of Hormuz closure triggered historic single-week price spike.', dark=True)
plt.tight_layout(rect=[0, 0, 1, 0.88])
save(fig, 'chart7_oil')


# ── Chart 8 — Global market reactions ────────────────────────
fig, ax = plt.subplots(figsize=(9, 3.8))
style_light(ax, fig)
days   = [f'Day {i}' for i in range(1, 11)]
gold_c = [3.2, 4.1, 4.8, 5.9, 6.2, 6.0, 5.8, 6.4, 7.1, 7.3]
oil_c  = [8.1,10.2,12.4,13.8,15.1,14.6,14.9,15.6,16.3,15.8]
eu_c   = [-3.4,-4.8,-3.2,-2.9,-3.8,-4.2,-3.9,-4.5,-4.1,-3.8]
asia_c = [-2.8,-4.1,-3.6,-3.3,-4.0,-3.7,-4.4,-4.1,-3.9,-4.2]
ax.plot(days, gold_c, color='#f1c40f', linewidth=2.2, marker='o', markersize=4, label='Gold %')
ax.plot(days, oil_c,  color=ORANGE,   linewidth=2.2, marker='s', markersize=4, label='Oil %')
ax.plot(days, eu_c,   color=BLUE,     linewidth=2.2, marker='^', markersize=4, label='European Equities %')
ax.plot(days, asia_c, color=PURPLE,   linewidth=2.2, marker='D', markersize=4, label='Asian Equities %')
ax.axhline(0, color='#ccc', linewidth=0.8)
ax.fill_between(range(10), 0, eu_c,   alpha=0.08, color=BLUE)
ax.fill_between(range(10), 0, asia_c, alpha=0.08, color=PURPLE)
ax.set_ylabel('% change from pre-war baseline', fontsize=9, color=MUTED)
ax.legend(fontsize=8.5)
title(ax, fig, 'Global Market Reactions — Days 1 to 10 of War',
      'All figures are % change from February 27, 2026 (day before strikes).')
plt.tight_layout(rect=[0, 0, 1, 0.88])
save(fig, 'chart8_markets')


# ── Chart 9 — International diplomatic reactions ──────────────
fig, ax = plt.subplots(figsize=(9, 4.0))
style_light(ax, fig)
nations = ['Israel','USA','Saudi Arabia','UAE','UK','France','Germany',
           'India','Turkey','China','Russia','Spain','UN Sec-Gen']
scores  = [5, 5, 3, 2.5, 2, 1, 0.5, -0.5, -2, -3.5, -4, -4.5, -3]
colors9 = [GREEN if s >= 2 else ORANGE if s >= 0 else RED2 if s >= -2 else RED
           for s in scores]
y = np.arange(len(nations))
bars = ax.barh(y, scores, color=colors9, height=0.6, zorder=3)
ax.set_yticks(y)
ax.set_yticklabels(nations, fontsize=9.5)
ax.set_xlim(-6, 6)
ax.axvline(0, color='#ccc', linewidth=1)
ax.set_xlabel('← Condemned       Neutral       Supported →', fontsize=9, color=MUTED)
ax.grid(axis='x', color='#f0ebe0', linewidth=0.8)
ax.grid(axis='y', visible=False)
for bar, s in zip(bars, scores):
    xp = s + (0.15 if s >= 0 else -0.15)
    ax.text(xp, bar.get_y() + bar.get_height()/2,
            f'{s:+.1f}', va='center',
            ha='left' if s >= 0 else 'right',
            fontsize=8, color=MUTED)
title(ax, fig, 'International Diplomatic Responses to US–Israel Strikes on Iran',
      'Scale: +5 = full support, 0 = neutral, -5 = strong condemnation.')
plt.tight_layout(rect=[0, 0, 1, 0.88])
save(fig, 'chart9_reactions')


# ── Chart 10 — Humanitarian impact ───────────────────────────
fig, ax = plt.subplots(figsize=(9, 3.6))
style_dark(ax, fig)
cats = ['Internally\nDisplaced (M)','Seeking\nAsylum (M)',
        'Food\nInsecure (M)','No Medicine\nAccess (M)','Medical\nFacilities Hit']
vals = [2.1, 0.4, 8.5, 12, 47]
bars = ax.bar(cats, vals,
              color=[RED, RED2, ORANGE, '#e74c3c', GOLD], width=0.55, zorder=3)
for bar, v in zip(bars, vals):
    label = f'{v}M' if v < 20 else str(int(v))
    ax.text(bar.get_x() + bar.get_width()/2, v + 0.4, label,
            ha='center', va='bottom', fontsize=9, color='#ccc', fontweight='bold')
ax.set_ylabel('Projected Count', fontsize=9, color='#aaa')
title(ax, fig, 'Projected Humanitarian Impact — First 30 Days',
      'UN & NGO projections. M = millions. Medical facilities = count of sites hit.', dark=True)
plt.tight_layout(rect=[0, 0, 1, 0.88])
save(fig, 'chart10_humanitarian')


print('\n  All 10 charts generated in the charts/ folder!')

"""
IAEA uranium enrichment reports: https://www.iaea.org/newscenter/reports
UN humanitarian data: https://data.unocha.org
World Bank / IMF Iran economic indicators: https://data.worldbank.org and https://imf.org/en/Data
EIA / Brent crude oil prices: https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx
UNHCR displacement data: https://www.unhcr.org/refugee-statistics
"""
