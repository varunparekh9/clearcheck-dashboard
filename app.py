
# ============================================================
# CLEARCHECK TECHNOLOGIES
# PROFESSIONAL MANAGEMENT ANALYTICS DASHBOARD
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ClearCheck Approval Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DESIGN SYSTEM
# ============================================================

NAVY = "#102A43"
BLUE = "#2563EB"
TEAL = "#0F766E"
ORANGE = "#F59E0B"
AMBER = "#D97706"
TEXT = "#172033"
TEXT_2 = "#475569"
MUTED = "#64748B"
CARD_BG = "#FFFFFF"
BORDER = "#E2E8F0"
GRID = "#EDF2F7"
FAST_BENCHMARK = 10

TECH_COLORS = {
    "Gary Arnold": BLUE,
    "Juan Mendez": TEAL,
    "Matt Shawn": ORANGE,
}


# ============================================================
# PROFESSIONAL CSS
# ============================================================

st.markdown(
    """
<style>

html, body, [data-testid="stAppViewContainer"] {
    background-color: #F5F7FB !important;
    color: #172033 !important;
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        "Helvetica Neue",
        Arial,
        sans-serif !important;
}

[data-testid="stHeader"] {
    background-color: #F5F7FB !important;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}


/* =========================================================
   SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #E2E8F0;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #172033 !important;
}


/* =========================================================
   SELECT BOXES
========================================================= */

[data-baseweb="select"] > div {
    background-color: #0E131A !important;
    border-color: #0E131A !important;
}

[data-baseweb="select"] span {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}


/* =========================================================
   SLIDERS
========================================================= */

[data-testid="stSlider"] p,
[data-testid="stSlider"] label,
[data-testid="stSlider"] span {
    color: #334155 !important;
    -webkit-text-fill-color: #334155 !important;
}


/* =========================================================
   NAVIGATION BUTTONS
   replaces Streamlit tabs completely
========================================================= */

div[data-testid="stRadio"] > div {
    display: flex !important;
    gap: 10px !important;
    flex-wrap: wrap !important;
}

div[data-testid="stRadio"] label {
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
    padding: 8px 15px !important;
    opacity: 1 !important;
}

div[data-testid="stRadio"] label p,
div[data-testid="stRadio"] label span,
div[data-testid="stRadio"] label div {
    color: #173B5E !important;
    -webkit-text-fill-color: #173B5E !important;
    opacity: 1 !important;
    font-weight: 650 !important;
}

div[data-testid="stRadio"] label:has(input:checked) {
    background: #EFF6FF !important;
    border-color: #2563EB !important;
}

div[data-testid="stRadio"] label:has(input:checked) p,
div[data-testid="stRadio"] label:has(input:checked) span,
div[data-testid="stRadio"] label:has(input:checked) div {
    color: #1D4ED8 !important;
    -webkit-text-fill-color: #1D4ED8 !important;
    font-weight: 750 !important;
}

div[data-testid="stRadio"] label > div:first-child {
    display: none !important;
}


/* =========================================================
   KPI CARDS
========================================================= */

[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 15px 16px;
    box-shadow: 0 4px 14px rgba(16, 42, 67, 0.05);
}

[data-testid="stMetricLabel"] p {
    color: #64748B !important;
    font-size: 12px !important;
    font-weight: 650 !important;
}

[data-testid="stMetricValue"] {
    color: #102A43 !important;
    font-weight: 800 !important;
}


/* =========================================================
   CHART CARDS
========================================================= */

[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF;
    border-color: #E2E8F0 !important;
    border-radius: 15px !important;
    box-shadow: 0 4px 15px rgba(16, 42, 67, 0.045);
}


/* =========================================================
   HEADINGS
========================================================= */

h1, h2, h3 {
    color: #173B5E !important;
}

.stMarkdown p {
    color: #475569;
}


/* =========================================================
   EXPANDERS / ALERTS / CAPTIONS
========================================================= */

[data-testid="stExpander"] {
    background: #FFFFFF;
    border-color: #E2E8F0 !important;
    border-radius: 11px !important;
}

[data-testid="stExpander"] summary p {
    color: #173B5E !important;
    font-weight: 650 !important;
}

[data-testid="stAlert"] {
    border-radius: 11px !important;
}

[data-testid="stAlert"] p {
    color: #334155 !important;
}

[data-testid="stCaptionContainer"] p {
    color: #64748B !important;
}

footer {
    visibility: hidden;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_int(value):
    if value is None or pd.isna(value):
        return "N/A"

    return f"{int(round(float(value))):,}"


def safe_number(
    value,
    decimals=1,
    suffix="",
):
    if value is None or pd.isna(value):
        return "N/A"

    return f"{float(value):.{decimals}f}{suffix}"


def style_chart(
    fig,
    height=390,
    legend=False,
):

    fig.update_layout(
        template="plotly_white",
        height=height,

        margin=dict(
            l=45,
            r=35,
            t=25,
            b=45,
        ),

        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,

        font=dict(
            family="Helvetica Neue, Arial",
            size=12,
            color=TEXT_2,
        ),

        showlegend=legend,

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(
                color=TEXT_2,
                size=12,
            ),
        ),

        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor=BORDER,
            font=dict(
                color=TEXT,
                size=12,
            ),
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#D7DEE7",
        tickfont=dict(
            color=MUTED,
        ),
        title_font=dict(
            color=TEXT_2,
        ),
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        linecolor="#D7DEE7",
        tickfont=dict(
            color=MUTED,
        ),
        title_font=dict(
            color=TEXT_2,
        ),
    )

    return fig


def show_chart(
    fig,
    height,
    legend=False,
):

    st.plotly_chart(
        style_chart(
            fig,
            height=height,
            legend=legend,
        ),

        use_container_width=True,

        config={
            "displayModeBar": False,
            "displaylogo": False,
            "scrollZoom": False,
            "responsive": True,
        },
    )


def add_block_key(frame):

    frame = frame.copy()

    if "BLOCK_ID" in frame.columns:

        frame["_BLOCK_KEY"] = (
            frame["BLOCK_ID"]
            .astype(str)
        )

    elif all(
        column in frame.columns
        for column in [
            "TECHNICIAN",
            "SOURCE_FILE",
            "BLOCK_NUMBER",
        ]
    ):

        frame["_BLOCK_KEY"] = (
            frame["TECHNICIAN"].astype(str)
            + "|"
            + frame["SOURCE_FILE"].astype(str)
            + "|"
            + frame["BLOCK_NUMBER"].astype(str)
        )

    elif all(
        column in frame.columns
        for column in [
            "TECHNICIAN",
            "BLOCK_NUMBER",
        ]
    ):

        frame["_BLOCK_KEY"] = (
            frame["TECHNICIAN"].astype(str)
            + "|"
            + frame["BLOCK_NUMBER"].astype(str)
        )

    else:

        frame["_BLOCK_KEY"] = np.nan

    return frame


# ============================================================
# LOAD DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


@st.cache_data
def load_data():

    approvals = pd.read_csv(
        DATA_DIR / "approval_data.csv"
    )

    blocks = pd.read_csv(
        DATA_DIR / "block_summary.csv"
    )

    batches = pd.read_csv(
        DATA_DIR / "batch_claim_blocks.csv"
    )

    tests = pd.read_csv(
        DATA_DIR / "one_sample_ttests.csv"
    )

    payout_summary = pd.read_csv(
        DATA_DIR / "payout_summary.csv"
    )

    payout_test = pd.read_csv(
        DATA_DIR / "payout_ttest_result.csv"
    )


    approvals["APPROVAL_DATE"] = pd.to_datetime(
        approvals["APPROVAL_DATE"],
        errors="coerce",
    )

    blocks["BLOCK_START"] = pd.to_datetime(
        blocks["BLOCK_START"],
        errors="coerce",
    )

    blocks["BLOCK_END"] = pd.to_datetime(
        blocks["BLOCK_END"],
        errors="coerce",
    )

    batches["BLOCK_START"] = pd.to_datetime(
        batches["BLOCK_START"],
        errors="coerce",
    )


    if "HOUR" not in approvals.columns:

        approvals["HOUR"] = (
            approvals["APPROVAL_DATE"]
            .dt.hour
        )


    if "WEEKDAY" not in approvals.columns:

        approvals["WEEKDAY"] = (
            approvals["APPROVAL_DATE"]
            .dt.day_name()
        )


    if "YEAR_MONTH" not in approvals.columns:

        approvals["YEAR_MONTH"] = (
            approvals["APPROVAL_DATE"]
            .dt.to_period("M")
            .astype(str)
        )


    if "PAYOUT_PERIOD" not in approvals.columns:

        approvals["PAYOUT_PERIOD"] = np.where(
            approvals["APPROVAL_DATE"]
            < pd.Timestamp("2020-06-01"),

            "Before June 2020",

            "After June 2020",
        )


    approvals = add_block_key(
        approvals
    )

    blocks = add_block_key(
        blocks
    )

    batches = add_block_key(
        batches
    )


    return (
        approvals,
        blocks,
        batches,
        tests,
        payout_summary,
        payout_test,
    )


(
    approvals,
    blocks,
    batches,
    tests,
    payout_summary,
    payout_test,
) = load_data()


# ============================================================
# HEADER
# ============================================================

with st.container(
    border=True
):

    st.caption(
        "MANAGEMENT ANALYTICS  •  APPROVAL REVIEW"
    )

    st.title(
        "ClearCheck Technologies"
    )

    st.write(
        "Technician approval behavior, workflow intensity "
        "and review-time analytics."
    )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    "## Dashboard Controls"
)

st.sidebar.caption(
    "Every control below updates "
    "all interactive dashboard visuals."
)


technicians = sorted(
    approvals[
        "TECHNICIAN"
    ]
    .dropna()
    .unique()
    .tolist()
)


selected_technician = st.sidebar.selectbox(
    "Technician",
    [
        "All Technicians"
    ]
    + technicians,
)


minimum_date = (
    approvals["APPROVAL_DATE"]
    .min()
    .date()
)


maximum_date = (
    approvals["APPROVAL_DATE"]
    .max()
    .date()
)


selected_dates = st.sidebar.slider(
    "Approval Date Range",

    min_value=minimum_date,
    max_value=maximum_date,

    value=(
        minimum_date,
        maximum_date,
    ),
)


start_date = pd.Timestamp(
    selected_dates[0]
)


last_date = pd.Timestamp(
    selected_dates[1]
)


end_date = (
    last_date
    + pd.Timedelta(
        days=1
    )
)


analysis_lens = st.sidebar.selectbox(
    "Analysis Lens",

    [
        "All Approvals",
        "Under 10 Seconds",
        "Under 30 Seconds",
        "Under 60 Seconds",
    ],

    index=0,
)


lens_threshold_map = {
    "All Approvals": None,
    "Under 10 Seconds": 10,
    "Under 30 Seconds": 30,
    "Under 60 Seconds": 60,
}


lens_threshold = (
    lens_threshold_map[
        analysis_lens
    ]
)


st.sidebar.divider()


st.sidebar.markdown(
    "## Display"
)


chart_size = st.sidebar.selectbox(
    "Chart Size",

    [
        "Compact",
        "Standard",
        "Large",
    ],

    index=1,
)


chart_height_map = {
    "Compact": 320,
    "Standard": 390,
    "Large": 470,
}


CHART_HEIGHT = (
    chart_height_map[
        chart_size
    ]
)


st.sidebar.info(
    "Technician, date range, analysis lens "
    "and chart size are global controls."
)


# ============================================================
# GLOBAL FILTERING
# ============================================================

filtered_approvals = approvals[
    (
        approvals["APPROVAL_DATE"]
        >= start_date
    )
    &
    (
        approvals["APPROVAL_DATE"]
        < end_date
    )
].copy()


filtered_blocks = blocks[
    (
        blocks["BLOCK_START"]
        < end_date
    )
    &
    (
        blocks["BLOCK_END"]
        >= start_date
    )
].copy()


filtered_batches = batches[
    (
        batches["BLOCK_START"]
        >= start_date
    )
    &
    (
        batches["BLOCK_START"]
        < end_date
    )
].copy()


if (
    selected_technician
    != "All Technicians"
):

    filtered_approvals = (
        filtered_approvals[
            filtered_approvals["TECHNICIAN"]
            == selected_technician
        ]
        .copy()
    )

    filtered_blocks = (
        filtered_blocks[
            filtered_blocks["TECHNICIAN"]
            == selected_technician
        ]
        .copy()
    )

    filtered_batches = (
        filtered_batches[
            filtered_batches["TECHNICIAN"]
            == selected_technician
        ]
        .copy()
    )


if (
    lens_threshold
    is not None
):

    filtered_approvals = (
        filtered_approvals[
            filtered_approvals[
                "APPROVAL_GAP_SECONDS"
            ]
            .notna()
            &
            (
                filtered_approvals[
                    "APPROVAL_GAP_SECONDS"
                ]
                < lens_threshold
            )
        ]
        .copy()
    )


    active_keys = (
        filtered_approvals[
            "_BLOCK_KEY"
        ]
        .dropna()
        .astype(str)
        .unique()
    )


    if len(active_keys) > 0:

        filtered_blocks = (
            filtered_blocks[
                filtered_blocks[
                    "_BLOCK_KEY"
                ]
                .astype(str)
                .isin(
                    active_keys
                )
            ]
            .copy()
        )

        filtered_batches = (
            filtered_batches[
                filtered_batches[
                    "_BLOCK_KEY"
                ]
                .astype(str)
                .isin(
                    active_keys
                )
            ]
            .copy()
        )

    else:

        filtered_blocks = (
            filtered_blocks
            .iloc[0:0]
            .copy()
        )

        filtered_batches = (
            filtered_batches
            .iloc[0:0]
            .copy()
        )


gap_data = (
    filtered_approvals
    .dropna(
        subset=[
            "APPROVAL_GAP_SECONDS"
        ]
    )
    .copy()
)


# ============================================================
# CURRENT VIEW
# ============================================================

st.caption(
    f"Current view  •  "
    f"{selected_technician}  •  "
    f"{start_date.strftime('%b %d, %Y')} to "
    f"{last_date.strftime('%b %d, %Y')}  •  "
    f"{analysis_lens}  •  "
    f"{len(filtered_approvals):,} approval records"
)


# ============================================================
# MAIN NAVIGATION
# ============================================================

main_page = st.radio(
    "Main Navigation",

    [
        "Executive Dashboard",
        "Additional Analysis",
    ],

    horizontal=True,

    label_visibility="collapsed",

    key="main_navigation",
)


# ============================================================
# EXECUTIVE DASHBOARD
# ============================================================

if (
    main_page
    == "Executive Dashboard"
):


    st.subheader(
        "Executive Snapshot"
    )


    st.caption(
        "Key approval-behavior indicators "
        "for the current dashboard view."
    )


    median_gap = (
        gap_data[
            "APPROVAL_GAP_SECONDS"
        ]
        .median()

        if not gap_data.empty

        else np.nan
    )


    fast_pct = (
        gap_data[
            "APPROVAL_GAP_SECONDS"
        ]
        .lt(
            FAST_BENCHMARK
        )
        .mean()
        * 100

        if not gap_data.empty

        else 0
    )


    median_block_size = (
        filtered_blocks[
            "APPROVALS_IN_BLOCK"
        ]
        .median()

        if not filtered_blocks.empty

        else np.nan
    )


    k1, k2, k3, k4, k5 = (
        st.columns(5)
    )


    k1.metric(
        "Total Approvals",

        safe_int(
            len(
                filtered_approvals
            )
        ),
    )


    k2.metric(
        "Median Approval Gap",

        safe_number(
            median_gap,
            1,
            " sec",
        ),
    )


    k3.metric(
        "Under 10 Seconds",

        safe_number(
            fast_pct,
            1,
            "%",
        ),
    )


    k4.metric(
        "Approval Blocks",

        safe_int(
            len(
                filtered_blocks
            )
        ),
    )


    k5.metric(
        "Median Block Size",

        safe_int(
            median_block_size
        ),
    )


    st.write("")


    # ========================================================
    # ROW 1
    # ========================================================

    left1, right1 = (
        st.columns(
            [
                1.25,
                1,
            ]
        )
    )


    with left1:

        with st.container(
            border=True
        ):

            st.markdown(
                "### Approval Gap Distribution"
            )

            st.caption(
                "Observed time between "
                "consecutive approvals."
            )


            histogram_limit = (
                lens_threshold

                if lens_threshold
                is not None

                else 600
            )


            hist_data = (
                gap_data[
                    gap_data[
                        "APPROVAL_GAP_SECONDS"
                    ]
                    <= histogram_limit
                ]
                .copy()
            )


            if not hist_data.empty:

                fig = go.Figure()

                fig.add_trace(
                    go.Histogram(
                        x=hist_data[
                            "APPROVAL_GAP_SECONDS"
                        ],

                        nbinsx=35,

                        marker=dict(
                            color=BLUE,

                            line=dict(
                                color="#FFFFFF",
                                width=0.4,
                            ),
                        ),

                        hovertemplate=(
                            "Approval gap: "
                            "%{x:.1f} sec"
                            "<br>Count: %{y:,}"
                            "<extra></extra>"
                        ),
                    )
                )


                benchmark_line = min(
                    FAST_BENCHMARK,
                    histogram_limit,
                )


                fig.add_vline(
                    x=benchmark_line,
                    line_dash="dash",
                    line_color=AMBER,
                    line_width=2,
                )


                fig.update_xaxes(
                    range=[
                        0,
                        histogram_limit,
                    ]
                )


                fig.update_layout(
                    xaxis_title=(
                        "Approval Gap (Seconds)"
                    ),

                    yaxis_title=(
                        "Number of Approval Gaps"
                    ),

                    bargap=0.03,
                )


                show_chart(
                    fig,
                    CHART_HEIGHT,
                )


            else:

                st.info(
                    "No approval-gap observations "
                    "match the current filters."
                )


    with right1:

        with st.container(
            border=True
        ):

            st.markdown(
                "### Fast Approval Rates"
            )

            st.caption(
                "Share of current approval gaps "
                "below each threshold."
            )


            thresholds = [
                2,
                5,
                10,
                30,
                60,
            ]


            rates = [
                (
                    gap_data[
                        "APPROVAL_GAP_SECONDS"
                    ]
                    .lt(
                        threshold
                    )
                    .mean()
                    * 100
                )

                if not gap_data.empty

                else 0

                for threshold
                in thresholds
            ]


            labels = [
                f"< {threshold} sec"

                for threshold
                in thresholds
            ]


            fig = go.Figure(
                go.Bar(
                    x=rates,
                    y=labels,

                    orientation="h",

                    text=[
                        f"{value:.1f}%"

                        for value
                        in rates
                    ],

                    textposition="outside",

                    marker=dict(
                        color=[
                            "#BFDBFE",
                            "#93C5FD",
                            "#60A5FA",
                            "#3B82F6",
                            "#1D4ED8",
                        ]
                    ),

                    hovertemplate=(
                        "%{y}"
                        "<br>%{x:.1f}%"
                        "<extra></extra>"
                    ),
                )
            )


            fig.update_xaxes(
                range=[
                    0,
                    105,
                ]
            )


            fig.update_layout(
                xaxis_title=(
                    "Percentage of Approval Gaps"
                ),

                yaxis_title="",
            )


            show_chart(
                fig,
                CHART_HEIGHT,
            )


    st.info(
        "Short approval gaps indicate rapid approval activity. "
        "They show observed workflow timing, not confirmed "
        "case-review time."
    )


    # ========================================================
    # ROW 2
    # ========================================================

    left2, right2 = (
        st.columns(
            [
                1.2,
                0.8,
            ]
        )
    )


    with left2:

        with st.container(
            border=True
        ):

            st.markdown(
                "### Highest-Volume Approval Days"
            )

            st.caption(
                "The ten highest-volume dates "
                "under the current global filters."
            )


            if not filtered_approvals.empty:

                top_days = (
                    filtered_approvals

                    .assign(
                        APPROVAL_DAY=
                        filtered_approvals[
                            "APPROVAL_DATE"
                        ]
                        .dt.normalize()
                    )

                    .groupby(
                        "APPROVAL_DAY"
                    )

                    .size()

                    .reset_index(
                        name="APPROVALS"
                    )

                    .nlargest(
                        10,
                        "APPROVALS"
                    )

                    .sort_values(
                        "APPROVALS"
                    )
                )


                top_days[
                    "DAY_LABEL"
                ] = (
                    top_days[
                        "APPROVAL_DAY"
                    ]
                    .dt.strftime(
                        "%b %d, %Y"
                    )
                )


                fig = go.Figure(
                    go.Bar(
                        x=top_days[
                            "APPROVALS"
                        ],

                        y=top_days[
                            "DAY_LABEL"
                        ],

                        orientation="h",

                        text=top_days[
                            "APPROVALS"
                        ],

                        textposition="outside",

                        marker=dict(
                            color=TEAL,
                        ),

                        hovertemplate=(
                            "%{y}"
                            "<br>%{x:,} approvals"
                            "<extra></extra>"
                        ),
                    )
                )


                fig.update_yaxes(
                    type="category"
                )


                fig.update_layout(
                    xaxis_title=(
                        "Number of Approvals"
                    ),

                    yaxis_title="",
                )


                show_chart(
                    fig,
                    CHART_HEIGHT,
                )


            else:

                st.info(
                    "No approval days match "
                    "the current filters."
                )


    with right2:

        with st.container(
            border=True
        ):

            st.markdown(
                "### Approval Speed Mix"
            )

            st.caption(
                "Composition of filtered "
                "approval gaps by speed band."
            )


            if not gap_data.empty:

                speed_band = pd.cut(
                    gap_data[
                        "APPROVAL_GAP_SECONDS"
                    ],

                    bins=[
                        -0.001,
                        5,
                        10,
                        30,
                        60,
                        np.inf,
                    ],

                    labels=[
                        "< 5 sec",
                        "5–10 sec",
                        "10–30 sec",
                        "30–60 sec",
                        "60+ sec",
                    ],

                    right=False,
                )


                speed_mix = (
                    speed_band
                    .value_counts(
                        sort=False
                    )
                    .reset_index()
                )


                speed_mix.columns = [
                    "Speed Band",
                    "Count",
                ]


                fig = go.Figure(
                    go.Pie(
                        labels=speed_mix[
                            "Speed Band"
                        ],

                        values=speed_mix[
                            "Count"
                        ],

                        hole=0.61,

                        textinfo="percent",

                        marker=dict(
                            colors=[
                                "#1D4ED8",
                                "#3B82F6",
                                "#60A5FA",
                                "#14B8A6",
                                "#CBD5E1",
                            ]
                        ),

                        hovertemplate=(
                            "%{label}"
                            "<br>%{value:,} gaps"
                            "<br>%{percent}"
                            "<extra></extra>"
                        ),
                    )
                )


                fig.update_layout(
                    annotations=[
                        dict(
                            text=(
                                "Approval"
                                "<br>"
                                "Speed"
                            ),

                            x=0.5,
                            y=0.5,

                            showarrow=False,

                            font=dict(
                                size=15,
                                color=NAVY,
                            ),
                        )
                    ]
                )


                show_chart(
                    fig,
                    CHART_HEIGHT,
                    legend=True,
                )


            else:

                st.info(
                    "No approval-gap observations "
                    "match the current filters."
                )


    # ========================================================
    # BLOCK ANALYSIS
    # ========================================================

    st.subheader(
        "Approval Block Analysis"
    )


    st.caption(
        "A new approval block begins when the gap "
        "between consecutive approvals reaches "
        "10 minutes or more."
    )


    multi_blocks = (
        filtered_blocks[
            filtered_blocks[
                "APPROVALS_IN_BLOCK"
            ]
            > 1
        ]
        .copy()
    )


    if not filtered_blocks.empty:

        largest_block = (
            filtered_blocks[
                "APPROVALS_IN_BLOCK"
            ]
            .max()
        )


        median_block = (
            filtered_blocks[
                "APPROVALS_IN_BLOCK"
            ]
            .median()
        )


        median_seconds = (
            multi_blocks[
                "AVAILABLE_SEC_PER_CASE"
            ]
            .replace(
                [
                    np.inf,
                    -np.inf,
                ],
                np.nan,
            )
            .median()

            if not multi_blocks.empty

            else np.nan
        )


        pct_under30 = (
            multi_blocks[
                "AVAILABLE_SEC_PER_CASE"
            ]
            .lt(30)
            .mean()
            * 100

            if not multi_blocks.empty

            else 0
        )


        b1, b2, b3, b4 = (
            st.columns(4)
        )


        b1.metric(
            "Largest Block",
            safe_int(
                largest_block
            ),
        )


        b2.metric(
            "Median Block Size",
            safe_int(
                median_block
            ),
        )


        b3.metric(
            "Median Time / Case",

            safe_number(
                median_seconds,
                1,
                " sec",
            ),
        )


        b4.metric(
            "Blocks < 30 Sec / Case",

            safe_number(
                pct_under30,
                1,
                "%",
            ),
        )


        st.write("")


        with st.container(
            border=True
        ):

            st.markdown(
                "### Approval Block Intensity"
            )

            st.caption(
                "Moving right means a larger block; moving down "
                "means less observed approval-window time "
                "available per case."
            )


            if not multi_blocks.empty:

                fig = px.scatter(
                    multi_blocks,

                    x="APPROVALS_IN_BLOCK",
                    y="AVAILABLE_SEC_PER_CASE",

                    color="TECHNICIAN",

                    color_discrete_map=(
                        TECH_COLORS
                    ),

                    size="APPROVALS_IN_BLOCK",

                    size_max=20,

                    opacity=0.68,

                    labels={
                        "APPROVALS_IN_BLOCK":
                        "Approvals in Block",

                        "AVAILABLE_SEC_PER_CASE":
                        "Observed Seconds per Case",

                        "TECHNICIAN":
                        "Technician",
                    },

                    hover_data={
                        "BLOCK_START":
                        True,

                        "APPROVALS_IN_BLOCK":
                        True,

                        "BLOCK_DURATION_MINUTES":
                        ":.2f",

                        "AVAILABLE_SEC_PER_CASE":
                        ":.2f",

                        "APPROVALS_PER_MINUTE":
                        ":.2f",
                    },
                )


                fig.update_traces(
                    marker=dict(
                        line=dict(
                            color="#FFFFFF",
                            width=0.6,
                        )
                    )
                )


                fig.add_hrect(
                    y0=0,
                    y1=30,

                    fillcolor=ORANGE,

                    opacity=0.06,

                    line_width=0,
                )


                fig.add_hline(
                    y=30,

                    line_dash="dot",

                    line_color=AMBER,

                    annotation_text=(
                        "30 sec / case"
                    ),
                )


                fig.add_hline(
                    y=60,

                    line_dash="dash",

                    line_color=MUTED,

                    annotation_text=(
                        "60 sec / case"
                    ),
                )


                show_chart(
                    fig,

                    CHART_HEIGHT
                    + 70,

                    legend=True,
                )


            else:

                st.info(
                    "No multi-case blocks match "
                    "the current global filters."
                )


        with st.expander(
            "View Largest Approval Blocks"
        ):

            table_columns = [
                "TECHNICIAN",
                "BLOCK_START",
                "APPROVALS_IN_BLOCK",
                "BLOCK_DURATION_MINUTES",
                "AVAILABLE_SEC_PER_CASE",
                "APPROVALS_PER_MINUTE",
            ]


            available_columns = [
                column

                for column
                in table_columns

                if column
                in filtered_blocks.columns
            ]


            largest_blocks = (
                filtered_blocks

                .sort_values(
                    "APPROVALS_IN_BLOCK",
                    ascending=False,
                )

                .head(10)[
                    available_columns
                ]

                .copy()
            )


            for column in [
                "BLOCK_DURATION_MINUTES",
                "AVAILABLE_SEC_PER_CASE",
                "APPROVALS_PER_MINUTE",
            ]:

                if (
                    column
                    in largest_blocks.columns
                ):

                    largest_blocks[
                        column
                    ] = (
                        pd.to_numeric(
                            largest_blocks[
                                column
                            ],

                            errors="coerce",
                        )
                        .round(2)
                    )


            st.dataframe(
                largest_blocks,

                hide_index=True,

                use_container_width=True,
            )


    else:

        st.info(
            "No approval blocks match "
            "the current global filters."
        )


# ============================================================
# ADDITIONAL ANALYSIS
# ============================================================

if (
    main_page
    == "Additional Analysis"
):

    st.subheader(
        "Additional Analysis"
    )


    st.caption(
        "Supporting behavioral and statistical evidence "
        "behind the executive dashboard."
    )


    analysis_page = st.radio(
        "Additional Analysis Navigation",

        [
            "Time Patterns",
            "Statistical Tests",
            "Payout Analysis",
            "Batch Claim Analysis",
        ],

        horizontal=True,

        label_visibility="collapsed",

        key="analysis_navigation",
    )


    # ========================================================
    # TIME PATTERNS
    # ========================================================

    if (
        analysis_page
        == "Time Patterns"
    ):

        time_left, time_right = (
            st.columns(2)
        )


        with time_left:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### Approval Activity by Hour"
                )

                st.caption(
                    "When approvals were recorded "
                    "during the day."
                )


                hourly = (
                    filtered_approvals

                    .groupby(
                        "HOUR"
                    )

                    .size()

                    .reindex(
                        range(24),
                        fill_value=0,
                    )

                    .reset_index(
                        name="APPROVALS"
                    )
                )


                fig = go.Figure(
                    go.Scatter(
                        x=hourly[
                            "HOUR"
                        ],

                        y=hourly[
                            "APPROVALS"
                        ],

                        mode=(
                            "lines+markers"
                        ),

                        line=dict(
                            color=BLUE,
                            width=3,
                        ),

                        marker=dict(
                            color=BLUE,
                            size=6,
                        ),

                        fill="tozeroy",

                        fillcolor=(
                            "rgba(37,99,235,0.10)"
                        ),

                        hovertemplate=(
                            "Hour %{x}:00"
                            "<br>%{y:,} approvals"
                            "<extra></extra>"
                        ),
                    )
                )


                if (
                    not hourly.empty

                    and

                    hourly[
                        "APPROVALS"
                    ]
                    .max()
                    > 0
                ):

                    peak_row = (
                        hourly.loc[
                            hourly[
                                "APPROVALS"
                            ]
                            .idxmax()
                        ]
                    )


                    fig.add_annotation(
                        x=int(
                            peak_row[
                                "HOUR"
                            ]
                        ),

                        y=float(
                            peak_row[
                                "APPROVALS"
                            ]
                        ),

                        text=(
                            "Peak hour"
                        ),

                        showarrow=True,

                        arrowhead=2,

                        font=dict(
                            color=NAVY,
                        ),
                    )


                fig.update_layout(
                    xaxis_title=(
                        "Hour of Day"
                    ),

                    yaxis_title=(
                        "Approvals"
                    ),
                )


                show_chart(
                    fig,
                    CHART_HEIGHT,
                )


        with time_right:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### Approval Activity by Weekday"
                )

                st.caption(
                    "Approval volume across "
                    "the days of the week."
                )


                weekday_order = [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ]


                weekday = (
                    filtered_approvals[
                        "WEEKDAY"
                    ]

                    .value_counts()

                    .reindex(
                        weekday_order,
                        fill_value=0,
                    )

                    .reset_index()
                )


                weekday.columns = [
                    "WEEKDAY",
                    "APPROVALS",
                ]


                fig = px.bar(
                    weekday,

                    x="WEEKDAY",
                    y="APPROVALS",

                    color="APPROVALS",

                    color_continuous_scale=[
                        "#D8E8FB",
                        BLUE,
                    ],

                    text="APPROVALS",
                )


                fig.update_traces(
                    textposition="outside"
                )


                fig.update_layout(
                    coloraxis_showscale=False,

                    xaxis_title="",

                    yaxis_title=(
                        "Approvals"
                    ),
                )


                show_chart(
                    fig,
                    CHART_HEIGHT,
                )


        with st.container(
            border=True
        ):

            st.markdown(
                "### Monthly Approval Volume"
            )

            st.caption(
                "Only months supplied in the dataset are shown. "
                "Missing months are not treated as zero activity."
            )


            if not filtered_approvals.empty:

                monthly = (
                    filtered_approvals

                    .assign(
                        MONTH_PERIOD=
                        filtered_approvals[
                            "APPROVAL_DATE"
                        ]
                        .dt.to_period("M")
                    )

                    .groupby(
                        "MONTH_PERIOD"
                    )

                    .size()

                    .reset_index(
                        name="APPROVALS"
                    )

                    .sort_values(
                        "MONTH_PERIOD"
                    )
                )


                monthly[
                    "MONTH_LABEL"
                ] = (
                    monthly[
                        "MONTH_PERIOD"
                    ]

                    .astype(str)

                    .apply(
                        lambda value:
                        pd.Period(
                            value,
                            freq="M",
                        )
                        .strftime(
                            "%b %Y"
                        )
                    )
                )


                fig = go.Figure(
                    go.Bar(
                        x=monthly[
                            "MONTH_LABEL"
                        ],

                        y=monthly[
                            "APPROVALS"
                        ],

                        text=monthly[
                            "APPROVALS"
                        ],

                        textposition="outside",

                        marker=dict(
                            color=TEAL,
                        ),

                        hovertemplate=(
                            "%{x}"
                            "<br>%{y:,} approvals"
                            "<extra></extra>"
                        ),
                    )
                )


                fig.update_xaxes(
                    type="category"
                )


                fig.update_layout(
                    xaxis_title=(
                        "Observed Month"
                    ),

                    yaxis_title=(
                        "Approvals"
                    ),
                )


                show_chart(
                    fig,
                    CHART_HEIGHT,
                )


            else:

                st.info(
                    "No monthly approval records "
                    "match the current filters."
                )


    # ========================================================
    # STATISTICAL TESTS
    # ========================================================

    elif (
        analysis_page
        == "Statistical Tests"
    ):

        st.markdown(
            "### Industry Benchmark Tests"
        )

        st.caption(
            "Formal one-sample tests "
            "from the analytical study."
        )


        test_view = (
            tests.copy()
        )


        if (
            selected_technician
            != "All Technicians"

            and

            "TECHNICIAN"
            in test_view.columns
        ):

            test_view = (
                test_view[
                    test_view[
                        "TECHNICIAN"
                    ]
                    == selected_technician
                ]

                .copy()
            )


        numeric_columns = (
            test_view

            .select_dtypes(
                include=np.number
            )

            .columns
        )


        test_view[
            numeric_columns
        ] = (
            test_view[
                numeric_columns
            ]
            .round(4)
        )


        st.dataframe(
            test_view,

            hide_index=True,

            use_container_width=True,
        )


        st.info(
            "These formal t-tests remain full-study results so they "
            "stay consistent with the written report. The interactive "
            "behavioral visuals respond to the dashboard filters."
        )


    # ========================================================
    # PAYOUT ANALYSIS
    # ========================================================

    elif (
        analysis_page
        == "Payout Analysis"
    ):

        st.markdown(
            "### Payout Policy Analysis"
        )

        st.caption(
            "Approval behavior before and after the payout "
            "changed from $50 to $17 per approval."
        )


        payout_source = (
            filtered_approvals

            .dropna(
                subset=[
                    "PAYOUT_PERIOD",
                    "APPROVAL_GAP_SECONDS",
                ]
            )

            .copy()
        )


        if not payout_source.empty:

            dynamic_payout = (
                payout_source

                .groupby(
                    "PAYOUT_PERIOD"
                )

                .agg(
                    SAMPLE_SIZE=(
                        "APPROVAL_GAP_SECONDS",
                        "size",
                    ),

                    MEAN_GAP_MINUTES=(
                        "APPROVAL_GAP_SECONDS",

                        lambda values:
                        float(
                            values.mean()
                        )
                        / 60,
                    ),

                    PCT_UNDER_10_SEC=(
                        "APPROVAL_GAP_SECONDS",

                        lambda values:
                        float(
                            (
                                values
                                < 10
                            )
                            .mean()
                            * 100
                        ),
                    ),

                    PCT_UNDER_30_SEC=(
                        "APPROVAL_GAP_SECONDS",

                        lambda values:
                        float(
                            (
                                values
                                < 30
                            )
                            .mean()
                            * 100
                        ),
                    ),

                    PCT_UNDER_60_SEC=(
                        "APPROVAL_GAP_SECONDS",

                        lambda values:
                        float(
                            (
                                values
                                < 60
                            )
                            .mean()
                            * 100
                        ),
                    ),
                )

                .reset_index()
            )


        else:

            dynamic_payout = (
                pd.DataFrame()
            )


        payout_left, payout_right = (
            st.columns(2)
        )


        with payout_left:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### Mean Approval Gap"
                )


                if not dynamic_payout.empty:

                    fig = go.Figure(
                        go.Bar(
                            x=dynamic_payout[
                                "PAYOUT_PERIOD"
                            ],

                            y=dynamic_payout[
                                "MEAN_GAP_MINUTES"
                            ],

                            text=[
                                f"{float(value):.2f}"

                                for value
                                in dynamic_payout[
                                    "MEAN_GAP_MINUTES"
                                ]
                            ],

                            textposition="outside",

                            marker=dict(
                                color=BLUE,
                            ),
                        )
                    )


                    fig.update_layout(
                        xaxis_title="",

                        yaxis_title=(
                            "Mean Gap (Minutes)"
                        ),
                    )


                    show_chart(
                        fig,
                        CHART_HEIGHT,
                    )


                else:

                    st.info(
                        "No payout-period observations "
                        "match the current filters."
                    )


        with payout_right:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### Fast Approval Behavior"
                )


                if not dynamic_payout.empty:

                    fig = go.Figure()


                    payout_series = [
                        (
                            "PCT_UNDER_10_SEC",
                            "< 10 sec",
                            BLUE,
                        ),
                        (
                            "PCT_UNDER_30_SEC",
                            "< 30 sec",
                            TEAL,
                        ),
                        (
                            "PCT_UNDER_60_SEC",
                            "< 60 sec",
                            ORANGE,
                        ),
                    ]


                    for (
                        column,
                        label,
                        color,
                    ) in payout_series:

                        if (
                            column
                            in dynamic_payout.columns
                        ):

                            fig.add_trace(
                                go.Bar(
                                    name=label,

                                    x=dynamic_payout[
                                        "PAYOUT_PERIOD"
                                    ],

                                    y=dynamic_payout[
                                        column
                                    ],

                                    marker_color=(
                                        color
                                    ),
                                )
                            )


                    fig.update_layout(
                        barmode="group",

                        yaxis_title=(
                            "Percentage"
                        ),
                    )


                    show_chart(
                        fig,
                        CHART_HEIGHT,
                        legend=True,
                    )


                else:

                    st.info(
                        "No payout-period observations "
                        "match the current filters."
                    )


        st.markdown(
            "#### Full-Study Welch Two-Sample T-Test"
        )


        st.dataframe(
            payout_test,

            hide_index=True,

            use_container_width=True,
        )


        st.warning(
            "Only Gary Arnold has supplied observations in both "
            "the before- and after-policy periods. The formal "
            "Welch test therefore reflects Gary's full-study comparison."
        )


    # ========================================================
    # BATCH CLAIM ANALYSIS
    # ========================================================

    elif (
        analysis_page
        == "Batch Claim Analysis"
    ):

        st.markdown(
            "### Pre-Block Review Capacity"
        )

        st.caption(
            "A generous upper-bound evaluation of the claim that "
            "cases may have been reviewed before being approved in batches."
        )


        batch_view = (
            filtered_batches
            .copy()
        )


        if not batch_view.empty:

            batch_values = (
                pd.to_numeric(
                    batch_view[
                        "PRE_BLOCK_SEC_PER_CASE"
                    ],

                    errors="coerce",
                )
            )


            median_pre = (
                batch_values
                .median()
            )


            under5 = (
                batch_values
                .lt(300)
                .mean()
                * 100
            )


            under10 = (
                batch_values
                .lt(600)
                .mean()
                * 100
            )


            q1, q2, q3 = (
                st.columns(3)
            )


            q1.metric(
                "Median Maximum Time / Case",

                safe_number(
                    median_pre
                    / 60,

                    2,

                    " min",
                ),
            )


            q2.metric(
                "Below 5 Min / Case",

                safe_number(
                    under5,
                    1,
                    "%",
                ),
            )


            q3.metric(
                "Below 10 Min / Case",

                safe_number(
                    under10,
                    1,
                    "%",
                ),
            )


            st.write("")


            positive_batch = (
                batch_view[
                    batch_values
                    > 0
                ]
                .copy()
            )


            if not positive_batch.empty:

                with st.container(
                    border=True
                ):

                    fig = px.scatter(
                        positive_batch,

                        x="APPROVALS_IN_BLOCK",

                        y="PRE_BLOCK_SEC_PER_CASE",

                        color="TECHNICIAN",

                        color_discrete_map=(
                            TECH_COLORS
                        ),

                        size="APPROVALS_IN_BLOCK",

                        size_max=20,

                        log_y=True,

                        opacity=0.68,

                        labels={
                            "APPROVALS_IN_BLOCK":
                            "Approvals in Block",

                            "PRE_BLOCK_SEC_PER_CASE":
                            "Maximum Pre-Block Seconds per Case",

                            "TECHNICIAN":
                            "Technician",
                        },
                    )


                    for (
                        seconds,
                        label,
                    ) in [
                        (
                            60,
                            "1 min",
                        ),
                        (
                            120,
                            "2 min",
                        ),
                        (
                            300,
                            "5 min",
                        ),
                        (
                            600,
                            "10 min",
                        ),
                    ]:

                        fig.add_hline(
                            y=seconds,

                            line_dash="dot",

                            line_color=MUTED,

                            annotation_text=(
                                label
                            ),
                        )


                    show_chart(
                        fig,

                        CHART_HEIGHT
                        + 60,

                        legend=True,
                    )


            else:

                st.info(
                    "No positive pre-block observations match "
                    "the current global filters."
                )


            st.warning(
                "This is not measured review time. The metric assumes "
                "the entire observed gap immediately before a block "
                "could have been used to review the upcoming cases, "
                "so it is a generous upper-bound estimate."
            )


        else:

            st.info(
                "No testable blocks match "
                "the current global filters."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "ClearCheck Technologies  •  "
    "Management Analytics  •  "
    "Technician Approval Behavior Analysis"
)
