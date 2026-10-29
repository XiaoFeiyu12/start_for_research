

import datetime
import time

import pandas as pd
import plotly.express as px
import streamlit as st

from database import Database, DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
from mqtt_subscriber import MqttSubscription

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "tcp/data"
CHECK_INTERVAL = 0.1  # 检查标志位的间隔，单位：秒


@st.cache_resource
def get_mqtt_client():
    state = {"new_data": False}

    def on_message_callback(msg):
        state["new_data"] = True

    sub = MqttSubscription(
        broker=MQTT_BROKER,
        port=MQTT_PORT,
        topic=MQTT_TOPIC,
        userdata=None,
        on_message_callback=on_message_callback,
    )
    sub.start_background()
    return sub, state


@st.cache_resource
def get_database():
    return Database(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)


@st.cache_data(ttl=10)  # 兜底过期时间；正常靠新数据到来时手动清缓存
def load_recent_data(limit: int):
    data = get_database().get_recent_data(limit)
    return pd.DataFrame(data=data, columns=["id", "timestamp", "value", "client"])


def show_metric(label, key, current):
    last = st.session_state.get(key)
    delta = None if last is None else float(round(current - last, 2))
    st.metric(label, current, delta)
    st.session_state[key] = current


def main():
    st.set_page_config(page_title="TCP数据实时看板", layout="wide")
    st.title("TCP 数据实时监控看板")

    _, state = get_mqtt_client()

    limit = st.sidebar.number_input("显示最近N条消息", 10, 500, 30)
    nbins = st.sidebar.number_input("直方图分布数量", 2, 100, 10)

    df = load_recent_data(limit)
    if df.empty:
        st.warning("数据库暂无数据")
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            show_metric("平均值", "last_mean", round(float(df["value"].mean()), 2))
        with col2:
            show_metric("最大值", "last_max", round(float(df["value"].max()), 2))
        with col3:
            show_metric("最小值", "last_min", round(float(df["value"].min()), 2))
        with col4:
            show_metric("标准差", "last_std", round(float(df["value"].std()), 2))

        st.divider()

        # 查库结果是新→旧，折线图要按时间升序画
        line = px.line(
            df.sort_values("timestamp"), x="timestamp", y="value", title="折线图示波器"
        )
        line.update_layout(xaxis_title="时间", yaxis_title="数值")
        st.plotly_chart(line, use_container_width=True)

        hist = px.histogram(df, x="value", title="数值分布直方图", nbins=nbins)
        hist.update_layout(xaxis_title="数据", yaxis_title="数量")
        st.plotly_chart(hist, use_container_width=True)

        st.divider()
        st.subheader("原始数据表格")
        st.dataframe(df, use_container_width=True)

    st.sidebar.info(f"最后更新：{datetime.datetime.now().strftime('%H:%M:%S')}")

    while True:
        if state["new_data"]:
            state["new_data"] = False  
            st.cache_data.clear()  
            st.rerun()
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
