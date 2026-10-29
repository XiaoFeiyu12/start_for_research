"""
Task6: Streamlit 数据可视化看板
从 MySQL 数据库读取数据，做统计分析，以图表形式展示

运行方式：streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from database import Database, DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
import numpy as np
# ── 页面配置 ──────────────────────────────────────────────────────────────────
# 提示：st.set_page_config() 必须是整个脚本里第一个调用的 st 函数，否则会报错
# 常用参数：
#   page_title  : 浏览器标签页标题，字符串
#   page_icon   : emoji 或图片路径，例如 "📊"
#   layout      : "centered"（默认）或 "wide"（更适合看板，推荐用 wide）
#
# TODO: 调用 st.set_page_config()，设置标题、图标、布局为 wide
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="TCP数据库实时看板", layout="wide")


# ── 数据库连接（全局，只创建一次）────────────────────────────────────────────
# 提示：@st.cache_resource 让 Streamlit 把这个函数的返回值缓存起来
#       只在应用首次启动时创建一次连接，后续调用直接返回同一个对象
#       适合数据库连接、模型加载等重量级资源
#
# TODO: 用 @st.cache_resource 装饰器定义 get_database() 函数，返回 Database 对象
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_database():
    return Database(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)


# ── 数据查询（带缓存，定期过期）─────────────────────────────────────────────
# 提示：@st.cache_data(ttl=5) 让查询结果缓存 5 秒
#       5 秒后下一次调用会重新查库，实现"近实时"刷新
#       ttl 单位是秒，可以根据需要调整
#
# TODO: 定义 load_recent_data(limit: int) 函数
#       - 用 @st.cache_data(ttl=5) 装饰
#       - 调用 get_database().get_recent_data(limit) 查询
#       - 把结果转成 pd.DataFrame，列名为 ["id", "timestamp", "value", "client"]
#       - 按 timestamp 升序排列（查库结果是降序的），用 df.sort_values() 或 df.iloc[::-1]
#       - 返回 DataFrame
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=5)
def load_recent_data(limit: int):
    data = get_database().get_recent_data(limit)
    pd_data = pd.DataFrame(data=data, columns=["id", "timestamp", "value", "client"])
    # pd_data = pd_data.sort_values(by="timestamp")
    return pd_data


# ── 主函数 ────────────────────────────────────────────────────────────────────
def main():
    st.title("TCP数据库实时看板")

    # ── 侧边栏：查询条件 ──────────────────────────────────────────────────────
    # 提示：st.sidebar 下的控件会渲染在左侧侧边栏
    # 常用控件：
    #   st.sidebar.number_input(label, min_value, max_value, value)  数字输入
    #   st.sidebar.slider(label, min_value, max_value, value)        滑动条
    #   st.sidebar.selectbox(label, options)                         下拉选择
    #
    # TODO: 在侧边栏加一个 number_input，让用户选择"显示最近 N 条"
    #       范围建议 10~500，默认值 100，赋值给变量 limit
    # ─────────────────────────────────────────────────────────────────────────
    limit = st.sidebar.number_input("显示最近N条消息", 10, 500, 100)
    # ── 查询数据 ──────────────────────────────────────────────────────────────
    # TODO: 调用 load_recent_data(limit)，拿到 df
    #       如果 df 为空（用 df.empty 判断），用 st.warning() 提示"暂无数据"并 return
    # ─────────────────────────────────────────────────────────────────────────
    df = load_recent_data(limit)
    if df.empty:
        st.warning("数据库暂无数据")
        return
    # ── 统计指标卡片 ──────────────────────────────────────────────────────────
    # 提示：st.columns(n) 创建 n 列，返回列对象列表
    #       with col:  进入列上下文后，里面的 st.xxx 就渲染在该列
    #       st.metric(label, value, delta) 显示一个 KPI 卡片，delta 是变化量（可选）
    #       pandas 统计：df["value"].mean()  .max()  .min()  .std()
    #
    # TODO: 创建 4 列，分别显示：均值、最大值、最小值、标准差
    #       数值保留 2 位小数（round(x, 2) 或 f"{x:.2f}"）
    # ─────────────────────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)


    with col1:
        mean = round(df["value"].mean(),2)
        if "last_mean" not in st.session_state:
            st.session_state.last_mean = None

        if st.session_state.last_mean is not None:
            delta = float(round(mean - st.session_state.last_mean, 2))
        else:
            delta = None
    
        st.metric("平均值",mean,delta)
        st.session_state.last_mean = mean

    with col2:
        max = round(df["value"].max(),2)
        if "last_max" not in st.session_state:
            st.session_state.last_max = None

        if st.session_state.last_max is not None:
            delta = float(round(max - st.session_state.last_max, 2))
        else:
            delta = None
    
        st.metric("最大值",max,delta)
        st.session_state.last_max = max

    with col3:
        min = round(df["value"].min(),2)
        if "last_min" not in st.session_state:
            st.session_state.last_min = None

        if st.session_state.last_min is not None:
            delta = float(round(min - st.session_state.last_min, 2))
        else:
            delta = None
    
        st.metric("最小值",min,delta)
        st.session_state.last_min = min

    with col4:
        std = round(df["value"].std(),2)
        if "last_std" not in st.session_state:
            st.session_state.last_std = None

        if st.session_state.last_std is not None:
            delta = float(round(std - st.session_state.last_std, 2))
        else:
            delta = None
    
        st.metric("标准差",std,delta)
        st.session_state.last_std = std

    st.divider()  # 分隔线

    # ── 折线图：数值随时间变化趋势 ───────────────────────────────────────────
    # 提示：
    #   fig = px.line(df, x="timestamp", y="value", title="数值趋势")
    #   st.plotly_chart(fig, use_container_width=True)
    #
    # 可选美化：
    #   fig.update_layout(xaxis_title="时间", yaxis_title="数值")
    #
    # TODO: 画折线图
    # ─────────────────────────────────────────────────────────────────────────
    fig = px.line(df,x="timestamp",y="value",title="折线图示波器")
    fig.update_layout(xaxis_title="时间", yaxis_title="数值")
    st.plotly_chart(fig,use_container_width=True)

    # ── 直方图：数值分布 ──────────────────────────────────────────────────────
    # 提示：
    #   fig = px.histogram(df, x="value", nbins=30, title="数值分布")
    #   nbins 是分桶数量，可以让用户通过侧边栏调整（进阶）
    #
    # TODO: 画直方图
    # ─────────────────────────────────────────────────────────────────────────
    nbins = st.sidebar.number_input("直方图分布数量",2,100,10)
    fig = px.histogram(df,x="value",title="数值分布直方图",nbins=nbins)
    fig.update_layout(xaxis_title="数据", yaxis_title="数量")
    st.plotly_chart(fig,use_container_width=True)
    st.divider()

    # ── 原始数据表格 ──────────────────────────────────────────────────────────
    # 提示：
    #   st.subheader("原始数据")
    #   st.dataframe(df, use_container_width=True)
    #
    # TODO: 展示原始数据表格
    # ─────────────────────────────────────────────────────────────────────────
    st.subheader("原始数据表格")
    st.dataframe(df, use_container_width=True)

    # ── 自动刷新（可选，进阶）────────────────────────────────────────────────
    # 方案 A（推荐）：安装 streamlit-autorefresh 包
    #   from streamlit_autorefresh import st_autorefresh
    #   st_autorefresh(interval=5000, key="refresh")   # 每 5000ms 刷新一次
    #
    # 方案 B：用 st.rerun()（在按钮点击时手动触发）
    #   if st.sidebar.button("🔄 手动刷新"):
    #       st.rerun()
    #
    # TODO: 至少实现方案 B（手动刷新按钮），方案 A 为进阶
    # ─────────────────────────────────────────────────────────────────────────
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=2000,key="refresh")

    if st.sidebar.button("手动刷新"):
        st.rerun()

if __name__ == "__main__":
    main()
