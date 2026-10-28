# This is the GItbub streamlink Cloud app altered to show only one event 14 April 2026 event and logo change
#%%writefile app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# ---------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------

st.set_page_config(
    page_title="PMU Data Science Dashboard",
    page_icon="⚡",
    layout="wide"
)

# ---------------------------------------------------
# DASHBOARD HEADER
# ---------------------------------------------------

logo1 = "data/logo1.png"
logo2 = "data/logo2.png"
logo3 = "data/logo3.png"
logo4 = "data/logo4.png"

c1, c2, c3, c4, title_col = st.columns(
    [0.45, 0.45, 0.45, 0.45, 6],
    vertical_alignment="center"
)

with c1:
    st.image(logo1, width=45)

with c2:
    st.image(logo2, width=45)

with c3:
    st.image(logo3, width=45)

with c4:
    st.image(logo4, width=45)

with title_col:
    st.title("PMU Data Science Dashboard")
    st.caption("Multi-PMU - Grid Frequency Event Analysis")





# ---------------------------------------------------
# PMU FEEDER MAPPING
# ---------------------------------------------------

pmu_feeder_maps = {
    "PMU 1": {
        "Feeder 1": "1_7",
        "Feeder 2": "1_8",
        "Feeder 3": "1_9",
        "Feeder 4": "1_10",
        "Feeder 5": "1_11",
        "Feeder 6": "1_12",
        "Feeder 7": "1_13"
    },

    "PMU 2": {
        "Feeder 1": "2_14",
        "Feeder 2": "2_15",
        "Feeder 3": "2_16",
        "Feeder 4": "2_17",
        "Feeder 5": "2_18",
        "Feeder 6": "2_19",
        "Feeder 7": "2_20"
    },

    "PMU 3": {
        "Feeder 1": "3_21",
        "Feeder 2": "3_22",
        "Feeder 3": "3_15",
        "Feeder 4": "3_23",
        "Feeder 5": "3_6",

    },

    "PMU 4": {
         "Feeder 1": "4_15",
        "Feeder 2": "4_24",
        "Feeder 3": "4_21",
        "Feeder 4": "4_25",
        "Feeder 5": "4_6",
        "Feeder 6": "4_26",
    },

    "PMU 5": {
        "Feeder 1": "5_27",
        "Feeder 2": "5_20",
        "Feeder 3": "5_28",
    },

    "PMU 6": {
        "Feeder 1": "6_3",
        "Feeder 2": "6_4",
        "Feeder 3": "6_29",
        "Feeder 4": "4_6",

    }
}

# ---------------------------------------------------
# PMU DATA FILES
# ---------------------------------------------------

pmu_files = {
    "PMU 1": "data/PMU_1_t_2026-04-14_10-10-18.csv",

    "PMU 2": "data/PMU_2_t_2026-04-14_10-10-18.csv",

    "PMU 3": "data/PMU_3_t_2026-04-14_10-10-18.csv",

    "PMU 4": "data/PMU_4_t_2026-04-14_10-10-18.csv",

    "PMU 5": "data/PMU_5_t_2026-04-14_10-10-18.csv",

    "PMU 6": "data/PMU_6_t_2026-04-14_10-10-18.csv"
}


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header("Dashboard Controls")

selected_pmu = st.sidebar.selectbox(
    "Select PMU",
    list(pmu_files.keys())
)



feeder_map = pmu_feeder_maps[selected_pmu]

if not feeder_map:
    st.warning(
        f"No feeder mappings have been configured for {selected_pmu}."
    )
    st.stop()

selected_feeder = st.sidebar.selectbox(
    "Select Feeder",
    list(feeder_map.keys())
)



channel = feeder_map[selected_feeder]

st.sidebar.divider()

st.sidebar.write(f"**Selected PMU:** {selected_pmu}")

st.sidebar.write(f"**Selected feeder:** {selected_feeder}")


# ---------------------------------------------------
# LOAD PMU 1 FREQUENCY EVENT
# ---------------------------------------------------

CSV_FILE = pmu_files[selected_pmu]

df = pd.read_csv(CSV_FILE)

df["Date_Time"] = pd.to_datetime(
    df["Date_Time"]
)

df = df.sort_values(
    "Date_Time"
).reset_index(drop=True)

# ---------------------------------------------------
# CURRENT DASHBOARD SELECTION
# ---------------------------------------------------

st.info(
    f"Viewing {selected_pmu} | "

    f"{selected_feeder}"
)




required_system_columns = [
    "Date_Time",
    "Frequency",
    "Dfrequency"
]

missing_system_columns = [
    column
    for column in required_system_columns
    if column not in df.columns
]

if missing_system_columns:
    st.error(
        "The selected file is missing required columns: "
        + ", ".join(missing_system_columns)
    )
    st.stop()



# ---------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------

min_frequency = df["Frequency"].min()
mean_frequency = df["Frequency"].mean()

min_dfreq = df["Dfrequency"].min()
max_dfreq = df["Dfrequency"].max()

nadir_time = df.loc[
    df["Frequency"].idxmin(),
    "Date_Time"
]


# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

st.subheader("System Overview")

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Minimum Frequency",
    f"{min_frequency:.3f} Hz"
)

k2.metric(
    "Mean Frequency",
    f"{mean_frequency:.3f} Hz"
)

k3.metric(
    "Minimum ROCOF",
    f"{min_dfreq:.3f} Hz/s"
)

k4.metric(
    "Maximum ROCOF",
    f"{max_dfreq:.3f} Hz/s"
)

st.caption(
    f"Frequency nadir occurred at {nadir_time}"
)


# ---------------------------------------------------
# FREQUENCY AND ROCOF
# ---------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    fig_freq = px.line(
        df,
        x="Date_Time",
        y="Frequency",
        title="System Frequency"
    )

    fig_freq.add_hline(
        y=50,
        line_dash="dash",
        line_color="red"
    )

    fig_freq.update_layout(
        xaxis_title="Time",
        yaxis_title="Frequency (Hz)"
    )

    st.plotly_chart(
        fig_freq,
        use_container_width=True
    )


with col2:

    fig_dfreq = px.line(
        df,
        x="Date_Time",
        y="Dfrequency",
        title="Rate of Change of Frequency (ROCOF)"
    )

    fig_dfreq.add_hline(
        y=0,
        line_dash="dash",
        line_color="black"
    )

    fig_dfreq.update_layout(
        xaxis_title="Time",
        yaxis_title="ROCOF (Hz/s)"
    )

    st.plotly_chart(
        fig_dfreq,
        use_container_width=True
    )


# ---------------------------------------------------
# VOLTAGE MAGNITUDE
# ---------------------------------------------------

st.subheader(
    f"{selected_pmu} | "
    f"{selected_feeder} - Three-Phase Measurements"
)

fig_voltage = go.Figure()

colors = {
    "A": "blue",
    "B": "red",
    "C": "green"
}

for phase in ["A", "B", "C"]:

    fig_voltage.add_trace(
        go.Scatter(
            x=df["Date_Time"],
            y=df[f"Mag_V{phase}_{channel}"],
            mode="lines",
            name=f"Phase {phase}",
            line=dict(
                color=colors[phase]
            )
        )
    )


fig_voltage.update_layout(
    title=f"{selected_feeder} - Voltage Magnitude",
    xaxis_title="Time",
    yaxis_title="Voltage Magnitude",
    hovermode="x unified"
)

st.plotly_chart(
    fig_voltage,
    use_container_width=True
)


# ---------------------------------------------------
# CURRENT MAGNITUDE
# ---------------------------------------------------

fig_current = go.Figure()

for phase in ["A", "B", "C"]:

    fig_current.add_trace(
        go.Scatter(
            x=df["Date_Time"],
            y=df[f"Mag_I{phase}_{channel}"],
            mode="lines",
            name=f"Phase {phase}",
            line=dict(
                color=colors[phase]
            )
        )
    )


fig_current.update_layout(
    title=f"{selected_feeder} - Current Magnitude",
    xaxis_title="Time",
    yaxis_title="Current Magnitude",
    hovermode="x unified"
)

st.plotly_chart(
    fig_current,
    use_container_width=True
)


# ---------------------------------------------------
# PHASOR TIMESTAMP SELECTOR
# ---------------------------------------------------

st.divider()
st.header("Phasor Diagram")

timestamp_options = df["Date_Time"].dt.strftime(
    "%Y-%m-%d %H:%M:%S.%f"
).str[:-3]

default_index = int(
    df["Dfrequency"].abs().idxmax()
)

selected_timestamp_text = st.select_slider(
    "Select measurement timestamp",
    options=timestamp_options.tolist(),
    value=timestamp_options.iloc[default_index]
)

selected_index = timestamp_options[
    timestamp_options == selected_timestamp_text
].index[0]

phasor_row = df.loc[selected_index]


# ---------------------------------------------------
# POLAR PHASOR DIAGRAM
# ---------------------------------------------------

phase_colors = {
    "A": "#EF553B",
    "B": "#00CC96",
    "C": "#636EFA"
}

voltage_values = {
    phase: {
        "magnitude": phasor_row[
            f"Mag_V{phase}_{channel}"
        ],
        "angle": phasor_row[
            f"Angle_V{phase}_{channel}"
        ]
    }
    for phase in ["A", "B", "C"]
}

current_values = {
    phase: {
        "magnitude": phasor_row[
            f"Mag_I{phase}_{channel}"
        ],
        "angle": phasor_row[
            f"Angle_I{phase}_{channel}"
        ]
    }
    for phase in ["A", "B", "C"]
}

max_voltage = max(
    item["magnitude"]
    for item in voltage_values.values()
)

max_current = max(
    item["magnitude"]
    for item in current_values.values()
)

fig_phasor = go.Figure()

for phase in ["A", "B", "C"]:

    voltage_radius = (
        voltage_values[phase]["magnitude"]
        / max_voltage
    )

    current_radius = (
        current_values[phase]["magnitude"]
        / max_current
    )

    voltage_angle = voltage_values[phase]["angle"]
    current_angle = current_values[phase]["angle"]

    # Voltage phasor
    fig_phasor.add_trace(
        go.Scatterpolar(
            r=[0, voltage_radius],
            theta=[voltage_angle, voltage_angle],
            mode="lines+markers+text",
            name=f"V{phase}",
            text=["", f"V{phase}"],
            textposition="top center",
            line=dict(
                color=phase_colors[phase],
                width=4
            ),
            marker=dict(
                color=phase_colors[phase],
                size=[1, 10],
                symbol="circle"
            ),
            customdata=[
                ["", ""],
                [
                    voltage_values[phase]["magnitude"],
                    voltage_angle
                ]
            ],
hovertemplate=(
    f"<b>V{phase}</b><br>"
    "Magnitude: %{customdata[0]:.3f}<br>"
    "Angle: %{customdata[1]:.3f}°"
    "<extra></extra>"
)

        )
    )

    # Current phasor
    fig_phasor.add_trace(
        go.Scatterpolar(
            r=[0, current_radius],
            theta=[current_angle, current_angle],
            mode="lines+markers+text",
            name=f"I{phase}",
            text=["", f"I{phase}"],
            textposition="bottom center",
            line=dict(
                color=phase_colors[phase],
                width=3,
                dash="dash"
            ),
            marker=dict(
                color=phase_colors[phase],
                size=[1, 9],
                symbol="diamond"
            ),
            customdata=[
                ["", ""],
                [
                    current_values[phase]["magnitude"],
                    current_angle
                ]
            ],
hovertemplate=(
    f"<b>I{phase}</b><br>"
    "Magnitude: %{customdata[0]:.3f}<br>"
    "Angle: %{customdata[1]:.3f}°"
    "<extra></extra>"
)
        )
    )


fig_phasor.update_layout(
    title=(
        f"{selected_pmu} | {selected_feeder} Phasor Diagram"
        f"<br><sup>{selected_timestamp_text}</sup>"
    ),
    height=700,
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1.15],
            tickvals=[0.25, 0.50, 0.75, 1.00],
            ticktext=["0.25", "0.50", "0.75", "1.00"]
        ),
        angularaxis=dict(
            direction="counterclockwise",
            rotation=0,
            tickmode="array",
            tickvals=[
                -180, -150, -120, -90, -60, -30,
                0, 30, 60, 90, 120, 150, 180
            ],
            ticktext=[
                "±180°", "-150°", "-120°", "-90°",
                "-60°", "-30°", "0°", "+30°",
                "+60°", "+90°", "+120°", "+150°",
                "±180°"
            ]
        )
    ),
    legend=dict(
        orientation="h",
        y=-0.12,
        x=0.5,
        xanchor="center"
    ),
    margin=dict(
        l=70,
        r=70,
        t=100,
        b=100
    )
)

st.plotly_chart(
    fig_phasor,
    use_container_width=True
)



# ---------------------------------------------------
# ALL-FEEDER EVENT COMPARISON
# ---------------------------------------------------

st.divider()
st.header("All-Feeder Event Comparison")

st.caption(
    f"Comparison of voltage dip and current change across "
    f"all feeders recorded by {selected_pmu} during the "
    f"main ROCOF transient."
)


# ---------------------------------------------------
# DEFINE EVENT WINDOWS
# ---------------------------------------------------

event_time = df.loc[
    df["Dfrequency"].idxmin(),
    "Date_Time"
]

pre_event = df[
    (df["Date_Time"] >= event_time - pd.Timedelta(seconds=2)) &
    (df["Date_Time"] < event_time - pd.Timedelta(seconds=0.5))
]

during_event = df[
    (df["Date_Time"] >= event_time - pd.Timedelta(seconds=0.5)) &
    (df["Date_Time"] <= event_time + pd.Timedelta(seconds=0.5))
]

post_event = df[
    (df["Date_Time"] > event_time + pd.Timedelta(seconds=0.5)) &
    (df["Date_Time"] <= event_time + pd.Timedelta(seconds=2))
]


# ---------------------------------------------------
# EVENT SUMMARY CARDS
# ---------------------------------------------------

event_col1, event_col2, event_col3, event_col4 = st.columns(4)

event_col1.metric(
    "Event Centre",
    event_time.strftime("%H:%M:%S.%f")[:-3]
)

event_col2.metric(
    "Pre-event Samples",
    f"{len(pre_event)}"
)

event_col3.metric(
    "Event Samples",
    f"{len(during_event)}"
)

event_col4.metric(
    "Post-event Samples",
    f"{len(post_event)}"
)


# ---------------------------------------------------
# VOLTAGE-DIP CALCULATIONS
# ---------------------------------------------------

all_feeder_dips = []

for feeder_name, feeder_channel in feeder_map.items():

    for phase in ["A", "B", "C"]:

        voltage_column = (
            f"Mag_V{phase}_{feeder_channel}"
        )

        pre_voltage_mean = (
            pre_event[voltage_column].mean()
        )

        event_voltage_minimum = (
            during_event[voltage_column].min()
        )

        voltage_dip = (
            pre_voltage_mean
            - event_voltage_minimum
        )

        voltage_dip_percent = (
            voltage_dip
            / pre_voltage_mean
        ) * 100

        all_feeder_dips.append({
            "Feeder": feeder_name,
            "Phase": phase,
            "Pre-event voltage": pre_voltage_mean,
            "Event minimum": event_voltage_minimum,
            "Voltage dip": voltage_dip,
            "Voltage dip (%)": voltage_dip_percent
        })


feeder_dip_df = pd.DataFrame(
    all_feeder_dips
)


# ---------------------------------------------------
# CURRENT-CHANGE CALCULATIONS
# ---------------------------------------------------

all_current_changes = []

for feeder_name, feeder_channel in feeder_map.items():

    for phase in ["A", "B", "C"]:

        current_column = (
            f"Mag_I{phase}_{feeder_channel}"
        )

        pre_current_mean = (
            pre_event[current_column].mean()
        )

        event_current_mean = (
            during_event[current_column].mean()
        )

        current_change = (
            event_current_mean
            - pre_current_mean
        )

        current_change_percent = (
            current_change
            / pre_current_mean
        ) * 100

        all_current_changes.append({
            "Feeder": feeder_name,
            "Phase": phase,
            "Pre-event current": pre_current_mean,
            "Event current": event_current_mean,
            "Current change": current_change,
            "Current change (%)": current_change_percent
        })


current_change_df = pd.DataFrame(
    all_current_changes
)


# ---------------------------------------------------
# ALL-FEEDER COMPARISON CHARTS
# ---------------------------------------------------

comparison_col1, comparison_col2 = st.columns(2)


with comparison_col1:

    voltage_dip_fig = px.bar(
        feeder_dip_df,
        x="Feeder",
        y="Voltage dip (%)",
        color="Phase",
        barmode="group",
        title="Voltage Dip by Feeder and Phase",
        color_discrete_map={
            "A": "#636EFA",
            "B": "#EF553B",
            "C": "#00CC96"
        }
    )

    voltage_dip_fig.update_layout(
        xaxis_title="Feeder",
        yaxis_title="Voltage Dip (%)",
        legend_title="Phase",
        hovermode="x unified"
    )

    st.plotly_chart(
        voltage_dip_fig,
        use_container_width=True
    )


with comparison_col2:

    current_change_fig = px.bar(
        current_change_df,
        x="Feeder",
        y="Current change (%)",
        color="Phase",
        barmode="group",
        title="Current Change by Feeder and Phase",
        color_discrete_map={
            "A": "#636EFA",
            "B": "#EF553B",
            "C": "#00CC96"
        }
    )

    current_change_fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="white"
    )

    current_change_fig.update_layout(
        xaxis_title="Feeder",
        yaxis_title="Current Change (%)",
        legend_title="Phase",
        hovermode="x unified"
    )

    st.plotly_chart(
        current_change_fig,
        use_container_width=True
    )


# ---------------------------------------------------
# ALL-FEEDER DATA TABLES
# ---------------------------------------------------

with st.expander(
    "View detailed all-feeder event results"
):

    table_col1, table_col2 = st.columns(2)

    with table_col1:

        st.subheader("Voltage-Dip Results")

        voltage_display = feeder_dip_df.copy()

        voltage_display[
            "Voltage dip (%)"
        ] = voltage_display[
            "Voltage dip (%)"
        ].round(3)

        voltage_display[
            "Pre-event voltage"
        ] = voltage_display[
            "Pre-event voltage"
        ].round(2)

        voltage_display[
            "Event minimum"
        ] = voltage_display[
            "Event minimum"
        ].round(2)

        voltage_display[
            "Voltage dip"
        ] = voltage_display[
            "Voltage dip"
        ].round(2)

        st.dataframe(
            voltage_display,
            use_container_width=True,
            hide_index=True
        )


    with table_col2:

        st.subheader("Current-Change Results")

        current_display = current_change_df.copy()

        current_display[
            "Current change (%)"
        ] = current_display[
            "Current change (%)"
        ].round(3)

        current_display[
            "Pre-event current"
        ] = current_display[
            "Pre-event current"
        ].round(3)

        current_display[
            "Event current"
        ] = current_display[
            "Event current"
        ].round(3)

        current_display[
            "Current change"
        ] = current_display[
            "Current change"
        ].round(3)

        st.dataframe(
            current_display,
            use_container_width=True,
            hide_index=True
        )



# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.caption(
    f"GridGnosis PMU Data | "
    f"{selected_pmu}"
)
