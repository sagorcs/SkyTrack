import streamlit as st
import pymysql


def get_connection():
    return pymysql.connect(
        host=st.secrets["mysql"]["host"],
        port=int(st.secrets["mysql"]["port"]),
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
        ssl={"ssl": {}},
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )