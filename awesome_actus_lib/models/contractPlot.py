from collections import defaultdict

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def initialize_graph(*dfs, contract_type, title, y1_label="Notional/Principal", y2_label="Interest Payments"):
    if contract_type.lower() in ["swap", "future", "option"]:
        return initialize_combined_graph(*dfs)
    else:
        return initialize_basic_graph(dfs[0], title=title, y1_label=y1_label, y2_label=y2_label)

def initialize_basic_graph(df, title="Contract Events", x_label="Date", y1_label="Notional/Principal", y2_label="Interest Payments"):
    """
    Initialize the graph structure for a basic (single) ACTUS contract.

    Parameters:
        df (pd.DataFrame): Event DataFrame with at least 'time', 'type', 'payoff', 'NominalValue'
        title (str): Title of the plot
        x_label (str): Label for x-axis
        y1_label (str): Label for y1-axis
        y2_label (str): Label for y2-axis (right-side)

    Returns:
        dict: Graph blueprint containing axis configs and empty layers
    """
    df = df.copy()
    df["Date"] = pd.to_datetime(df["time"])
    df = df.sort_values("Date")

    # Use only event dates for x-axis ticks
    xaxis_dates = df["Date"].unique()
    xaxis = sorted(pd.to_datetime(xaxis_dates).tolist())
    xlabels = [{"at": dt, "label": dt.strftime("%Y-%m-%d")} for dt in xaxis]

    # Define x-axis limits with a buffer
    start_date = df["Date"].min()
    end_date = df["Date"].max()
    date_range_days = (end_date - start_date).days
    padding = int(date_range_days * 0.05)  # 5% of total range
    xlim = (start_date - pd.Timedelta(days=padding), end_date + pd.Timedelta(days=padding))


    # Y1 (Notional-related) axis
    notional_events = df[df["type"].isin(["CDD", "IED", "PRD", "TD", "MD", "OPS", "DPR", "RES", "ETA", "ITF"])]
    y1_data = notional_events["payoff"].abs().tolist()
    if "NominalValue" in df.columns:
        y1_data += df["NominalValue"].dropna().abs().tolist()
    y1_max = 10 * np.ceil(max(y1_data + [1]) / 10) + np.ceil(max(y1_data))*0.035
    y1_min = 0
    y1_ticks = np.linspace(0, y1_max-np.ceil(max(y1_data))*0.035, 5)
    y1_labels = [{"at": val, "label": f"{val:.0f}"} for val in y1_ticks]

    # Y2 (Cashflow-related) axis with stacking awareness and fallback
    y2_events = df[df["type"].isin(["IP", "IPCI", "PR", "DV", "MR", "STD", "DPR"])]
    y2_data = y2_events["payoff"].abs().tolist()

    # Try stack-aware scaling using IP + PR
    stacked_events = df[df["type"].isin(["IP", "PR"])].copy()
    stacked_events["Date"] = pd.to_datetime(stacked_events["time"])

    if not stacked_events.empty:
        stacked_y2 = stacked_events.groupby("Date")["payoff"].apply(lambda x: sum(abs(v) for v in x))
        y2_max = 10 * np.ceil(stacked_y2.max() / 10)
    else:
        y2_max = 10 * np.ceil(max(y2_data + [1]) / 10)

    y2_scale = 0.5 * y1_max / y2_max if y2_max != 0 else 1
    y2_ticks = np.linspace(0, y2_max, 5)
    y2_labels = [{"at": val * y2_scale, "label": f"{val:.0f}"} for val in y2_ticks]


    # Construct the graph object
    graph = {
        "title": title,
        "x.lab": x_label,
        "y1.lab": y1_label,
        "y2.lab": y2_label,

        "xaxis": xaxis,
        "xlabels": xlabels,
        "x.lim": xlim,

        "y.lim": (y1_min, y1_max),
        "ylabels": y1_labels,
        "y2labels": y2_labels,
        "y2.scale": y2_scale,

        "text": [],
        "arrows": [],
        "lines": [],
        "cycles": [],
        "events": []
    }

    return graph

def initialize_combined_graph(df_parent, df_child1, df_child2=None, title="Combined Contract Events"):
    """
    Initialize the graph structure for a combined ACTUS contract (e.g., SWAP, OPTION, FUTURE).

    Parameters:
        df_parent (pd.DataFrame): Event data for parent contract (Level == 'P')
        df_child1 (pd.DataFrame): Event data for first child contract (Level == 'C1')
        df_child2 (pd.DataFrame or None): Optional second child contract (Level == 'C2')
        title (str): Title of the plot

    Returns:
        dict: Graph blueprint with multi-axis support
    """
    # # Combine all dates for shared x-axis
    # df_all = pd.concat([df_parent, df_child1] + ([df_child2] if df_child2 is not None else []))
    # df_all["Date"] = pd.to_datetime(df_all["Date"])
    # df_all = df_all.sort_values("Date")

    # start_date = df_all["Date"].min()
    # end_date = df_all["Date"].max()
    # xaxis = pd.date_range(start=start_date, end=end_date, freq='D').to_pydatetime().tolist()
    # xlabels = [{"at": dt, "label": dt.strftime("%Y-%m-%d")} for dt in pd.date_range(start=start_date, end=end_date, freq='MS')]

    # # --- Parent Axis (Primary Y) ---
    # parent_y_data = df_parent[df_parent["Type"].isin(["CDD", "IED", "PRD", "TD", "MD", "STD", "OPPD", "OPXED"])]["Value"].abs().tolist()
    # if "NominalValue" in df_parent.columns:
    #     parent_y_data += df_parent["NominalValue"].dropna().abs().tolist()
    # parent_max = 10 * np.ceil(max(parent_y_data + [1]) / 10)
    # parent_min = -parent_max
    # parent_ticks = np.linspace(0, parent_max, 5)
    # y11_labels = [{"at": val, "label": f"{val:.0f}"} for val in parent_ticks]

    # # Margining Layer (Y12) — Optional
    # y12_max = 0
    # margining = df_parent[df_parent["Type"] == "MR"]
    # if not margining.empty:
    #     y12_max = 10 * np.ceil(margining["Value"].abs().max() / 10)
    # y12_labels = [{"at": val, "label": f"{val:.0f}"} for val in np.linspace(0, y12_max, 5)] if y12_max > 0 else []

    # # --- Child 1 Axes (Secondary Y) ---
    # def extract_child_axes(df, y_max_ref):
    #     notional_vals = df[df["Type"].isin(["CDD", "IED", "PRD", "TD", "MD"])]["Value"].abs().tolist()
    #     if "NominalValue" in df.columns:
    #         notional_vals += df["NominalValue"].dropna().abs().tolist()
    #     notional_max = 10 * np.ceil(max(notional_vals + [1]) / 10)
    #     notional_scale = 0.6 * y_max_ref / notional_max if notional_max else 1
    #     notional_ticks = np.linspace(0, notional_max, 5)
    #     notional_labels = [{"at": val * notional_scale, "label": f"{val:.0f}"} for val in notional_ticks]

    #     cf_vals = df[df["Type"].isin(["IP", "PR", "IPCI", "DV"])]["Value"].abs().tolist()
    #     cf_max = 10 * np.ceil(max(cf_vals + [1]) / 10)
    #     cf_scale = 0.5 * notional_scale * y_max_ref / cf_max if cf_max else 1
    #     cf_ticks = np.linspace(0, cf_max, 5)
    #     cf_labels = [{"at": val * cf_scale, "label": f"{val:.0f}"} for val in cf_ticks]

    #     return {
    #         "notional": {"max": notional_max, "scale": notional_scale, "labels": notional_labels},
    #         "cashflow": {"max": cf_max, "scale": cf_scale, "labels": cf_labels}
    #     }

    # child1_axes = extract_child_axes(df_child1, parent_max)
    # child2_axes = extract_child_axes(df_child2, parent_max) if df_child2 is not None else None

    # # Assemble final graph object
    # graph = {
    #     "title": title,
    #     "x.lab": "",
    #     "y11.lab": "P: Notional/Principal",
    #     "y12.lab": "P: Margining" if y12_max > 0 else None,
    #     "y21.lab": "C1: Notional/Principal",
    #     "y22.lab": "C1: Cashflows",
    #     "y31.lab": "C2: Notional/Principal" if child2_axes else None,
    #     "y32.lab": "C2: Cashflows" if child2_axes else None,

    #     "xaxis": xaxis,
    #     "xlabels": xlabels,
    #     "x.lim": (start_date - pd.Timedelta(days=10), end_date + pd.Timedelta(days=10)),

    #     "y11.lim": (parent_min, parent_max),
    #     "y11labels": y11_labels,
    #     "y12.lim": (parent_min, y12_max),
    #     "y12labels": y12_labels,
    #     "y12.scale": parent_max / y12_max if y12_max else 1,

    #     "y21.lim": (parent_min, child1_axes["notional"]["max"]),
    #     "y21labels": child1_axes["notional"]["labels"],
    #     "y21.scale": child1_axes["notional"]["scale"],
    #     "y22.lim": (parent_min, child1_axes["cashflow"]["max"]),
    #     "y22labels": child1_axes["cashflow"]["labels"],
    #     "y22.scale": child1_axes["cashflow"]["scale"],

    #     "y31.lim": (parent_min, child2_axes["notional"]["max"]) if child2_axes else None,
    #     "y31labels": child2_axes["notional"]["labels"] if child2_axes else None,
    #     "y31.scale": child2_axes["notional"]["scale"] if child2_axes else None,
    #     "y32.lim": (parent_min, child2_axes["cashflow"]["max"]) if child2_axes else None,
    #     "y32labels": child2_axes["cashflow"]["labels"] if child2_axes else None,
    #     "y32.scale": child2_axes["cashflow"]["scale"] if child2_axes else None,

    #     "text": [],
    #     "arrows": [],
    #     "lines": [],
    #     "cycles": [],
    #     "events": []
    # }

    # return graph
    raise NotImplementedError("Combined contract graphing not yet implemented.")


def add_notional_payment_layer(graph, df):
    """
    Adds principal-related cash flow arrows (IED, PR, MD) to the graph.
    Draws arrows based on absolute value and direction, within a positive Y scale.

    Parameters:
        graph (dict): Plot blueprint object
        df (pd.DataFrame): Contract event data
    """
    df = df.copy()
    df["Date"] = pd.to_datetime(df["time"])

    for _, row in df[df["type"].isin(["IED", "MD"])].iterrows():
        event_type = row["type"]
        date = row["Date"]
        value = row["payoff"]

        y_base = 0
        y_tip = abs(value)
        if value < 0:
            y_start, y_end = y_tip, y_base  # arrow down
        else:
            y_start, y_end = y_base, y_tip  # arrow up

        graph["arrows"].append({
            "x0": date, 
            "y0": y_start, 
            "x1": date, 
            "y1": y_end,
            "color": "red", 
            "linetype": "-", 
            "linewidth": 1.5
        })
        date_range_days = (graph["x.lim"][1] - graph["x.lim"][0]).days
        horizontal_shift = pd.Timedelta(days=int(date_range_days * 0.01))  # ~1% of range

        graph["text"].append({
            "x": date + horizontal_shift, 
            "y": y_end + 0.05*(abs(value) if event_type == "IED" else -abs(value)),
            "label": event_type, 
            "size": 8
        })
        graph["events"].append(event_type)

    return graph

def add_interest_layer(graph, df):
    """
    Adds the base interest layer:
    - Solid green arrows for interest payments (IP events only), scaled using y2.scale.
    This layer does NOT include accrual lines or rate resets.

    Parameters:
        graph (dict): Plot blueprint object
        df (pd.DataFrame): Contract event data
    """
    df = df.copy()
    df["Date"] = pd.to_datetime(df["time"])
    scale = graph.get("y2.scale", 1)

    for _, row in df[df["type"] == "IP"].iterrows():
        date = row["Date"]
        value = row["payoff"]

        y_base = 0
        y_tip = abs(value) * scale
        if value < 0:
            y_start, y_end = y_tip, y_base  # arrow down
        else:
            y_start, y_end = y_base, y_tip  # arrow up
        # print(f"[DEBUG] Adding IP arrow on {date} from {y_start} to {y_end} with value {value}")
        graph["arrows"].append({
            "x0": date,
            "y0": y_start,
            "x1": date,
            "y1": y_end,
            "color": "green",
            "linetype": "-",  # solid line
            "linewidth": 1.5
        })
        date_range_days = (graph["x.lim"][1] - graph["x.lim"][0]).days
        horizontal_shift = pd.Timedelta(days=int(date_range_days * 0.01))  # ~1% of range

        graph["text"].append({
            "x": date + horizontal_shift,
            "y": y_end + (10 if value >= 0 else -10),
            "label": "IP",
            "size": 8
        })
        graph["events"].append("IP")

    return graph

def add_redemption_layer(graph, df):
    """
    Adds principal redemption (PR) events as stacked green arrows on Y2, scaled using y2.scale.

    Parameters:
        graph (dict): Plot blueprint object
        df (pd.DataFrame): Contract event data
    """
    df = df.copy()
    df["Date"] = pd.to_datetime(df["time"])
    scale = graph.get("y2.scale", 1)
    stack = defaultdict(float)  # date → cumulative arrow height
    ip_by_date = df[df["type"] == "IP"].groupby("Date")["payoff"].sum().to_dict()
    for date, ip in ip_by_date.items():
        stack[date] = abs(ip) * scale

    for _, row in df[df["type"] == "PR"].iterrows():
        date = row["Date"]
        value = row["payoff"]
        height = abs(value) * scale

        y_base = stack[date]
        if value >= 0:
            y_start, y_end = y_base, y_base + height
        else:
            y_start, y_end = y_base + height, y_base  # flipped arrow

        stack[date] = y_end  # always store the upper tip for next stacking

        # print(f"[DEBUG] Adding PR arrow on {date} from {y_start} to {y_end} with value {value}")
        graph["arrows"].append({
            "x0": date,
            "y0": y_start,
            "x1": date,
            "y1": y_end,
            "color": "red",
            "linetype": "-",
            "linewidth": 1.5
        })
        date_range_days = (graph["x.lim"][1] - graph["x.lim"][0]).days
        horizontal_shift = pd.Timedelta(days=int(date_range_days * 0.01))  # ~1% of range
        graph["text"].append({
            "x": date + horizontal_shift,
            "y": y_end + (10 if value >= 0 else -10),
            "label": "PR",
            "size": 8
        })
        graph["events"].append("PR")

    return graph

def add_outstanding_nominal_layer(graph, df):
    """
    Adds the outstanding nominal layer as a stepwise line on Y1, matching the R notionalStateLayer.

    Parameters:
        graph (dict): Plot blueprint
        df (pd.DataFrame): Contract event data
    """
    df = df.copy()
    df["Date"] = pd.to_datetime(df["time"])

    # Filter rows with nominalValue present and drop exact duplicates
    df = df[["Date", "nominalValue"]].dropna().drop_duplicates().sort_values("Date")

    if df.empty or len(df) < 2:
        return graph

    # Construct stepwise line
    points = []
    prev_date, prev_val = None, None
    for date, val in zip(df["Date"], abs(df["nominalValue"])):
        if prev_date is not None:
            # Horizontal segment
            points.append({"x": date, "y": prev_val, "scale": 1})
        points.append({"x": date, "y": val, "scale": 1})
        prev_date, prev_val = date, val

    graph["lines"].append({
        "points": points,
        "color": "red",
        "linetype": "--",
        "linewidth": 1.5
    })

    graph["events"].append("nominalState")

    return graph

def add_interest_accrual_layer(graph, df):
    """
    Adds interest accrual as a green dashed line on Y2, segmented at each IP and RR event.
    The line starts at 0 on IP, builds to nominalAccrued at RR, and ends at IP payoff before resetting.

    Parameters:
        graph (dict): Plot blueprint
        df (pd.DataFrame): Contract event data
    """

    df = df.copy()
    df["Date"] = pd.to_datetime(df["time"])

    # Filter and retain essential columns
    df = df[df["type"].isin(["IP", "RR"]) & df["nominalAccrued"].notna()]
    df = df[["Date", "type", "payoff", "nominalAccrued"]].drop_duplicates().sort_values("Date")

    if df.empty or len(df) < 2:
        return graph

    scale = graph.get("y2.scale", 1)
    segments = []
    pending_segment = []

    for _, row in df.iterrows():
        date = row["Date"]
        typ = row["type"]

        if typ == "IP":
            val = abs(row["payoff"])  # Ending at IP payoff
            if pending_segment:
                # Add final segment to IP
                prev_date, prev_val = pending_segment[-1]
                segments.append({
                    "points": [
                        {"x": prev_date, "y": prev_val, "scale": scale},
                        {"x": date, "y": val, "scale": scale}
                    ],
                    "color": "green",
                    "linetype": "--",
                    "linewidth": 1.2
                })
                pending_segment = []

            # Start new accrual from 0 after IP
            pending_segment = [(date, 0)]

        elif typ == "RR":
            val = row["nominalAccrued"]
            if pending_segment:
                prev_date, prev_val = pending_segment[-1]
                segments.append({
                    "points": [
                        {"x": prev_date, "y": prev_val, "scale": scale},
                        {"x": date, "y": val, "scale": scale}
                    ],
                    "color": "green",
                    "linetype": "--",
                    "linewidth": 1.2
                })
                pending_segment.append((date, val))

    graph["lines"].extend(segments)
    graph["events"].append("interestAccrued")

    return graph

def add_rr_cycle_wave_layer(graph, df):
    """
    Adds upward-bending sinusoidal wave curves between RR events (like R plot).
    Dynamically scales amplitude based on Y1 range (e.g., 5% of max Y1 value).

    Parameters:
        graph (dict): Plot blueprint
        df (pd.DataFrame): Contract event data
    """

    def annotate_rr_event_labels(graph, df):
        """
        Adds text labels ("RR") above each Rate Reset (RR) event on the plot.

        Parameters:
            graph (dict): Plot blueprint
            df (pd.DataFrame): Contract event data
        """
        df = df.copy()
        df["Date"] = pd.to_datetime(df["time"])
        rr_events = df[df["type"] == "RR"].sort_values("Date")

        if rr_events.empty:
            return graph

        y1_max = graph.get("y.lim", (0, 100))[1]
        label_height = 0.03 * y1_max * -1  # slightly above max amplitude

        date_range_days = (graph["x.lim"][1] - graph["x.lim"][0]).days
        horizontal_shift = pd.Timedelta(days=int(date_range_days * 0.01))  # ~1% x-range

        for _, row in rr_events.iterrows():
            graph["text"].append({
                "x": row["Date"] + horizontal_shift,
                "y": label_height,
                "label": "RR",
                "size": 8
            })

        graph["events"].append("RR")

        return graph


    df = df.copy()
    df["Date"] = pd.to_datetime(df["time"])
    rr_events = df[df["type"] == "RR"].sort_values("Date")

    if len(rr_events) < 2:
        return graph  # Need at least two RR events to form a wave

    y1_max = graph.get("y.lim", (0, 100))[1]
    amplitude = 0.05 * y1_max  # 5% of y1 height
    samples = 40

    wave_lines = []

    for i in range(len(rr_events) - 1):
        start_date = rr_events.iloc[i]["Date"]
        end_date = rr_events.iloc[i + 1]["Date"]

        total_seconds = (end_date - start_date).total_seconds()
        times = [start_date + pd.Timedelta(seconds=total_seconds * t / (samples - 1))
                 for t in range(samples)]

        # Only use positive half of sine wave (0 → π)
        ys = [amplitude * np.sin(np.pi * t / (samples - 1)) for t in range(samples)]
        points = [{"x": t, "y": y, "scale": 1} for t, y in zip(times, ys)]

        wave_lines.append({
            "points": points,
            "color": "lightgreen",
            "linetype": "--",
            "linewidth": 1.5
        })

    graph["lines"].extend(wave_lines)
    graph["events"].append("rrCycleWave")
    graph = annotate_rr_event_labels(graph, df)

    return graph

def render_graph(graph, return_fig):
    """
    Renders the given graph blueprint using matplotlib, with dual y-axes (Y1 for notional, Y2 for interest/cashflow).

    Parameters:
        graph (dict): Graph structure with arrows, text, and axis config
    """
    fig, ax1 = plt.subplots(figsize=(14, 6))
    ax2 = ax1.twinx()  # secondary Y axis for interest/cashflows

    # Baseline
    ax1.axhline(0, color='black', linewidth=1)
    for line in graph.get("lines", []):
        xs = [p["x"] for p in line["points"]]
        ys = [p["y"] * p.get("scale", 1) for p in line["points"]]
        ax1.plot(xs, ys, color=line["color"], linestyle=line["linetype"], linewidth=line["linewidth"])

    # Draw arrows
    for arrow in graph["arrows"]:
        color = arrow["color"]
        event_type = arrow.get("label", "")  # optional
        is_interest = color == "green"  # heuristic for now

        axis = ax2 if is_interest else ax1
        axis.annotate("",
                    xy=(arrow["x1"], arrow["y1"]),
                    xytext=(arrow["x0"], arrow["y0"]),
                    arrowprops=dict(
                        arrowstyle="->",
                        color=color,
                        lw=arrow["linewidth"],
                        linestyle=arrow["linetype"]
                    ))

    # Draw text
    for label in graph["text"]:
        label_type = label["label"]
        is_interest = label_type == "IP"
        axis = ax2 if is_interest else ax1
        axis.text(label["x"], label["y"], label["label"],
                ha="center", va="bottom", fontsize=label["size"])

    # Axes setup
    ax1.set_xlim(graph["x.lim"])
    ax1.set_ylim(graph["y.lim"])
    ax2.set_ylim(graph["y.lim"])  # keep same visual height, labels will differ

    ax1.set_xlabel(graph["x.lab"])
    ax1.set_ylabel(graph["y1.lab"])
    ax2.set_ylabel(graph["y2.lab"])
    ax1.set_title(graph["title"])

    # Format x-axis ticks
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    fig.autofmt_xdate()

    # Y1 ticks
    ax1.set_yticks([yt["at"] for yt in graph["ylabels"]])
    ax1.set_yticklabels([yt["label"] for yt in graph["ylabels"]])

    # Y2 ticks: use same positions but label using raw values
    if "y2labels" in graph:
        ax2.set_yticks([yt["at"] for yt in graph["y2labels"]])
        ax2.set_yticklabels([yt["label"] for yt in graph["y2labels"]])

    # X ticks
    ax1.set_xticks([xt["at"] for xt in graph["xlabels"]])
    ax1.set_xticklabels([xt["label"] for xt in graph["xlabels"]], rotation=45, ha='right')

    plt.tight_layout()
    if return_fig:
        return fig
    else:
        plt.show()
# final plot now for testing: 
def contractPlot(df, contract_type, title=None, y1_label="Notional/Principal", y2_label="Interest Payments", return_fig=False):
    graph = initialize_graph(df, contract_type=contract_type, title=title, y1_label=y1_label, y2_label=y2_label)

    # Add layers
    graph = add_notional_payment_layer(graph, df)
    graph = add_interest_layer(graph, df)
    graph = add_redemption_layer(graph, df)
    graph = add_outstanding_nominal_layer(graph, df)
    graph = add_interest_accrual_layer(graph, df)
    graph = add_rr_cycle_wave_layer(graph, df)
    # Render the graph using matplotlib
    return render_graph(graph, return_fig)



