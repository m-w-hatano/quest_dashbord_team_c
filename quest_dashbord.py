import numpy as np
import pandas as pd
import streamlit as st
import pydeck as pdk
import plotly.express as px


st.set_page_config(layout="wide")
st.title('わんだーゲーム：集計ダッシュボード')

df_cate_names = pd.read_csv('./quest22_data/category_names.csv')
# df_cate_names
df_item_cate = pd.read_csv('./quest22_data/item_categories.csv')
# df_item_cate
df_item_cate_name =  pd.merge(df_item_cate, df_cate_names, on='商品カテゴリID')
# df_item_cate_name
df_sales1 = pd.read_csv('./quest22_data/sales_history1.csv', encoding='shift_jis')
df_sales2 = pd.read_csv('./quest22_data/sales_history2.csv', encoding='shift_jis')
df_sales1_2 = pd.concat([df_sales1, df_sales2])
df_sales1_2 = pd.merge(df_sales1_2, df_item_cate_name, on='商品ID')
# df_sales1_2

#--------------------------
# date型に変換DatetimeIndexに変換して集計しやすく
df_sales1_2['日付'] = pd.to_datetime(df_sales1_2['日付'])
df_sales1_2 = df_sales1_2.set_index(df_sales1_2["日付"])

#売上金額をカラムに追加
df_sales1_2['売上金額'] = df_sales1_2['商品価格'] * df_sales1_2['売上個数']
#全データの確認用
df_sales1_2


#フィルタリング機能---------------------------
shop_list = list(df_sales1_2['店舗ID'].unique())
select_shop = st.sidebar.multiselect("店舗IDでフィルタ",shop_list,7)
df_sales1_2 = df_sales1_2[(df_sales1_2['店舗ID'].isin(select_shop))]


category_list =  df_sales1_2['商品カテゴリ名'].unique()
select_category = st.sidebar.multiselect("カテゴリでフィルタ",category_list,'PCゲーム - 通常版')
df_sales1_2 = df_sales1_2[(df_sales1_2['商品カテゴリ名'].isin(select_category))]

# 集計時間単位の切り替え
date_span = st.sidebar.radio("集計範囲切り替え　※W=週 M=月 Q=四半期", ("W","M", "Q","Y"))

#  -------------------------

#集計表示

# st.header("Filter")
shukei = df_sales1_2.resample(date_span).sum()
# shukei

title_name =  "売上合計　　店舗ID : " + str(select_shop) +  "      カテゴリー名 : " + str(select_category)
st.header(title_name)
df_value_line = shukei[['売上個数', '売上金額']]
st.line_chart(df_value_line)

st.header("売上個数合計") 
df_quant_line = shukei['売上個数']
st.line_chart(df_quant_line)
df_sales1_2


st.header("商品ID別売上推移") 
productID_list =  df_sales1_2['商品ID'].unique()
select_productID = st.sidebar.multiselect("商品IDでフィルタ",productID_list)
df_product_sales = df_sales1_2[(df_sales1_2['商品ID'].isin(select_productID))]
productID_shukei = df_product_sales.resample(date_span).sum()
productID_Quant_line = productID_shukei['売上個数']
st.line_chart(productID_Quant_line)
df_product_sales 
productID_shukei[['売上個数','売上金額']]