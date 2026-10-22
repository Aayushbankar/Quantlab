from __future__ import annotations

from typing import Any


def generate_honesty_report_html(run_data: dict[str, Any]) -> str:
    """Generates a standalone, institutional, printable HTML honesty report for a backtest run."""
    run_id = run_data.get("run_id", "N/A")
    strategy = run_data.get("strategy", "N/A")
    served_from = run_data.get("served_from", "live")
    engine_ver = run_data.get("engine_version", "1.0.0")
    cost_profile = run_data.get("cost_profile", "standard_discount_2024")
    data_hash = run_data.get("data_hash", "N/A")
    dates = run_data.get("dates", [])
    start_date = dates[0] if dates else "N/A"
    end_date = dates[-1] if dates else "N/A"

    metrics = run_data.get("metrics", {})
    costs = run_data.get("costs", {})
    diag = run_data.get("diagnostics", {})
    trades = run_data.get("trades", [])

    total_return = metrics.get("total_return", 0.0) * 100.0
    cagr = metrics.get("cagr", 0.0) * 100.0
    sharpe = metrics.get("sharpe_ratio", 0.0)
    sortino = metrics.get("sortino_ratio", 0.0)
    max_dd = metrics.get("max_drawdown", 0.0) * 100.0
    calmar = metrics.get("calmar_ratio", 0.0)
    exposure = metrics.get("average_exposure", 1.0) * 100.0
    alpha = metrics.get("alpha", 0.0) * 100.0
    beta = metrics.get("beta", 1.0)
    exp_matched = metrics.get("exposure_matched_return", 0.0) * 100.0

    brokerage = costs.get("brokerage", 0.0)
    stt = costs.get("stt", 0.0)
    stamp_duty = costs.get("stamp_duty", 0.0)
    turnover_fees = costs.get("turnover_fees", 0.0)
    gst = costs.get("gst", 0.0)
    dp_charges = costs.get("dp_charges", 0.0)
    sebi_fees = costs.get("sebi_fees", 0.0)
    ipft = costs.get("ipft", 0.0)
    impact = costs.get("market_impact", 0.0)
    total_friction = costs.get("total_friction", 0.0)
    friction_drag = costs.get("friction_drag_pct", 0.0)

    dsr = diag.get("dsr_p_value")
    exp_max = diag.get("expected_max_sharpe")
    pbo = diag.get("pbo")
    n_trials = diag.get("n_trials", 1)

    dsr_badge = (
        f'<span class="badge {"badge-pass" if dsr and dsr >= 0.95 else "badge-fail"}">DSR p = {dsr:.4f} ({"PASS ≥ 0.95" if dsr and dsr >= 0.95 else "FAIL < 0.95"})</span>'
        if dsr is not None
        else '<span class="badge badge-neutral">DSR Not Computed</span>'
    )
    pbo_badge = (
        f'<span class="badge badge-neutral">CPCV PBO = {pbo*100:.1f}%</span>'
        if pbo is not None
        else '<span class="badge badge-neutral">PBO: Empirical Sweep Required</span>'
    )

    filled_trades = [t for t in trades if t.get("status") == "FILLED"]
    rejected_trades = [t for t in trades if t.get("status") == "REJECTED"]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pramaan Honesty Report — {run_id}</title>
    <style>
        @page {{ size: A4 portrait; margin: 1.5cm; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            color: #1a202c;
            line-height: 1.5;
            background: #fff;
            margin: 0;
            padding: 24px;
        }}
        .header {{
            border-bottom: 2px solid #28464B;
            padding-bottom: 16px;
            margin-bottom: 24px;
        }}
        .header h1 {{
            margin: 0 0 4px 0;
            color: #28464B;
            font-size: 26px;
            letter-spacing: -0.5px;
        }}
        .header .subtitle {{
            color: #4a5568;
            font-size: 14px;
            margin: 0;
        }}
        .provenance {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 16px 0 24px 0;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-family: monospace;
            background: #edf2f7;
            color: #2d3748;
            border: 1px solid #cbd5e0;
        }}
        .badge-pass {{ background: #c6f6d5; color: #22543d; border-color: #9ae6b4; }}
        .badge-fail {{ background: #fed7d7; color: #742a2a; border-color: #feb2b2; }}
        .badge-neutral {{ background: #edf2f7; color: #4a5568; border-color: #cbd5e0; }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin-bottom: 24px;
        }}
        .card {{
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 12px;
            background: #f7fafc;
        }}
        .card .label {{
            font-size: 11px;
            color: #718096;
            text-transform: uppercase;
            font-weight: 600;
            margin-bottom: 4px;
        }}
        .card .value {{
            font-size: 18px;
            font-weight: 700;
            color: #28464B;
        }}
        .section-title {{
            font-size: 16px;
            font-weight: 700;
            color: #28464B;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 6px;
            margin: 24px 0 12px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            margin-bottom: 16px;
        }}
        th, td {{
            text-align: left;
            padding: 8px 10px;
            border-bottom: 1px solid #e2e8f0;
        }}
        th {{
            background: #edf2f7;
            color: #4a5568;
            font-weight: 600;
        }}
        .disclaimer {{
            background: #fffaf0;
            border: 1px solid #feebc8;
            border-left: 4px solid #dd6b20;
            padding: 12px;
            font-size: 12px;
            color: #744210;
            margin-top: 32px;
            border-radius: 4px;
        }}
        @media print {{
            body {{ padding: 0; }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Pramaan Honesty Report</h1>
        <p class="subtitle">GTU DI05000341 Verified Backtest Audit &bull; <em>"Prove your edge before you deploy a rupee."</em></p>
    </div>

    <div class="provenance">
        <span class="badge">Run ID: {run_id}</span>
        <span class="badge">Strategy: {strategy}</span>
        <span class="badge">Period: {start_date} &rarr; {end_date}</span>
        <span class="badge">Engine: v{engine_ver}</span>
        <span class="badge">Cost Profile: {cost_profile}</span>
        <span class="badge">Data Hash: {data_hash}</span>
        <span class="badge">Served From: {served_from.upper()}</span>
    </div>

    <div class="section-title">1. Honest Performance Summary (Accounting for Statutory Drag & Exposure)</div>
    <div class="grid">
        <div class="card">
            <div class="label">Net Total Return</div>
            <div class="value">{total_return:+.2f}%</div>
        </div>
        <div class="card">
            <div class="label">Net CAGR</div>
            <div class="value">{cagr:+.2f}%</div>
        </div>
        <div class="card">
            <div class="label">Net Sharpe</div>
            <div class="value">{sharpe:.2f}</div>
        </div>
        <div class="card">
            <div class="label">Net Sortino</div>
            <div class="value">{sortino:.2f}</div>
        </div>
        <div class="card">
            <div class="label">Max Drawdown</div>
            <div class="value">{max_dd:.2f}%</div>
        </div>
        <div class="card">
            <div class="label">Calmar Ratio</div>
            <div class="value">{calmar:.2f}</div>
        </div>
        <div class="card">
            <div class="label">Average Exposure</div>
            <div class="value">{exposure:.1f}%</div>
        </div>
        <div class="card">
            <div class="label">Alpha vs B&amp;H</div>
            <div class="value">{alpha:+.2f}%</div>
        </div>
        <div class="card">
            <div class="label">Beta vs B&amp;H</div>
            <div class="value">{beta:.2f}</div>
        </div>
        <div class="card">
            <div class="label">Exposure-Matched B&amp;H</div>
            <div class="value">{exp_matched:+.2f}%</div>
        </div>
    </div>

    <div class="section-title">2. Statutory Friction Tollgate Waterfall</div>
    <table>
        <thead>
            <tr>
                <th>Cost Line Item</th>
                <th>Statutory Authority / Basis</th>
                <th>Levied On</th>
                <th>Amount (INR)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Brokerage</strong></td>
                <td>Broker Rate Card</td>
                <td>Buy &amp; Sell Orders</td>
                <td>&#8377;{brokerage:,.2f}</td>
            </tr>
            <tr>
                <td><strong>Securities Transaction Tax (STT)</strong></td>
                <td>Finance Act / CBDT Rule 5</td>
                <td>Buy (0.1%) &amp; Sell (0.1%) Delivery</td>
                <td>&#8377;{stt:,.2f}</td>
            </tr>
            <tr>
                <td><strong>Stamp Duty</strong></td>
                <td>Indian Stamp Act (Uniform 2020)</td>
                <td>Buy Delivery Only (0.015%)</td>
                <td>&#8377;{stamp_duty:,.2f}</td>
            </tr>
            <tr>
                <td><strong>Exchange Turnover</strong></td>
                <td>NSE Oct 2024 True-to-Label (0.00297%)</td>
                <td>Turnover (Both Sides)</td>
                <td>&#8377;{turnover_fees:,.2f}</td>
            </tr>
            <tr>
                <td><strong>SEBI Fee &amp; IPFT</strong></td>
                <td>SEBI (0.0001%) + NSE IPFT (0.0001%)</td>
                <td>Turnover (Both Sides)</td>
                <td>&#8377;{sebi_fees + ipft:,.2f}</td>
            </tr>
            <tr>
                <td><strong>DP Charges</strong></td>
                <td>CDSL Flat &#8377;13.50</td>
                <td>Sell Orders Only (Per ISIN Debit)</td>
                <td>&#8377;{dp_charges:,.2f}</td>
            </tr>
            <tr>
                <td><strong>GST</strong></td>
                <td>18% on (Brokerage + Turnover + DP Charges)</td>
                <td>Taxable Friction Base</td>
                <td>&#8377;{gst:,.2f}</td>
            </tr>
            <tr>
                <td><strong>Market Impact / Slippage</strong></td>
                <td>Almgren-Chriss Square Root Model</td>
                <td>Execution Price Variance</td>
                <td>&#8377;{impact:,.2f}</td>
            </tr>
            <tr style="background: #edf2f7; font-weight: 700;">
                <td colspan="3"><strong>Total Frictional Drag &amp; Tollgate Loss</strong></td>
                <td>&#8377;{total_friction:,.2f} ({friction_drag:.2f}% of capital)</td>
            </tr>
        </tbody>
    </table>

    <div class="section-title">3. Statistical Overfitting Diagnostics (Marcos L&oacute;pez de Prado)</div>
    <div style="margin-bottom: 16px;">
        {dsr_badge}
        {pbo_badge}
        <span class="badge badge-neutral">Trials Evaluated: N = {n_trials}</span>
        <span class="badge badge-neutral">Expected Max SR (Noise): {exp_max if exp_max is not None else "N/A"}</span>
    </div>
    <p style="font-size: 13px; color: #4a5568;">
        The Deflated Sharpe Ratio (DSR) computes the probability that the observed Sharpe ratio ({sharpe:.2f})
        exceeds the maximum Sharpe expected purely by chance under the null hypothesis of selection bias across {n_trials} trials.
        Values below 0.95 indicate that apparent performance cannot be statistically distinguished from multi-testing data snooping.
    </p>

    <div class="section-title">4. Execution Audit ({len(filled_trades)} Filled, {len(rejected_trades)} Rejected)</div>
    <p style="font-size: 13px; color: #4a5568;">
        Zero Look-Ahead Invariant: Signals generated at Day T Close are strictly executed at Day T+1 Open.
        Orders rejected due to cash constraints or minimum share sizing are permanently preserved in the audit log.
    </p>

    <div class="disclaimer">
        <strong>Academic &amp; Regulatory Disclaimer (GTU DI05000341 Sem-5 Minor Project):</strong><br>
        Pramaan is an honest academic backtesting platform for NSE cash equities. Historical simulations are subject to
        survivorship bias (current NIFTY-50 constituents) and market regime shifts. Past simulated performance does not guarantee
        future live trading returns. Not SEBI-registered investment advice.
    </div>
</body>
</html>
"""
    return html
