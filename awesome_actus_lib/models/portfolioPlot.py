import matplotlib.pyplot as plt
import pandas as pd


def portfolioPlot(events_df, title="Portfolio Cashflows", y1_label="Payoff", return_fig=False):
    """
    Plots portfolio-level cashflows as a stacked bar chart aggregated by event type and adaptive time binning.

    Parameters:
        df (pd.DataFrame): Event DataFrame with columns 'time', 'type', 'payoff'
        title (str): Plot title
        y1_label (str): Label for y-axis
        y2_label (str): Ignored for now
    """
    df = events_df
    if df.empty or "payoff" not in df.columns:
        print("No valid payoff events to plot.")
        return

    df = df.copy()
    df["Date"] = pd.to_datetime(df["time"])
    df = df[["Date", "type", "payoff"]].dropna()
    df = df[df["payoff"] != 0]

    # Decide aggregation level dynamically
    def decide_frequency(date_series):
        daily = date_series.dt.date.nunique()
        if daily <= 50:
            return "D"
        weekly = date_series.dt.to_period("W").nunique()
        if weekly <= 50:
            return "W"
        monthly = date_series.dt.to_period("M").nunique()
        if monthly <= 50:
            return "M"
        return "Y"

    freq = decide_frequency(df["Date"])
    df["Period"] = df["Date"].dt.to_period(freq).dt.to_timestamp()

    # Aggregate payoffs by type and period
    grouped = df.groupby(["Period", "type"])["payoff"].sum().unstack(fill_value=0)

    # Plotting
    ax = grouped.plot(
        kind="bar",
        stacked=True,
        figsize=(14, 6),
        colormap="tab20",
        width=0.8
    )

    ax.set_title(title)
    ax.set_ylabel(y1_label)
    ax.set_xlabel("Date")
    ax.legend(title="Event Type")
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    fig = ax.get_figure()  # ✅ Extract the figure from the Axes

    if return_fig:
        return fig
    else:
        plt.show()
