import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from PIL import Image
import os
import time
from io import StringIO

# Cargar datos desde string
@st.cache_data
def cargar_datos():
    datos = '''
Edad;A;B;C
18;0.7812;0.6273;0.4868
19;0.7723;0.6153;0.474
20;0.7648;0.6052;0.4635
21;0.7584;0.5968;0.4548
22;0.7531;0.5898;0.4476
23;0.7485;0.5838;0.4415
24;0.7444;0.5786;0.4362
25;0.7406;0.5737;0.4313
26;0.7367;0.5688;0.4265
27;0.7326;0.5636;0.4213
28;0.7278;0.5576;0.4154
29;0.7221;0.5506;0.4085
30;0.7152;0.5421;0.4002
31;0.7066;0.5317;0.3902
32;0.6961;0.5192;0.3783
33;0.6831;0.504;0.3642
34;0.6666;0.4852;0.3469
35;0.6449;0.4613;0.3255
36;0.6162;0.4308;0.299
37;0.5782;0.3926;0.267
38;0.5292;0.3464;0.23
39;0.4678;0.293;0.1894
40;0.3944;0.2349;0.1475
41;0.3123;0.1763;0.1077
42;0.2284;0.1224;0.0729
43;0.1519;0.0779;0.0454
44;0.0909;0.045;0.0259
45;0.0487;0.0236;0.0134
46;0.0233;0.0111;0.0063
47;0.01;0.0047;0.0027
'''
    return pd.read_csv(StringIO(datos), sep=';')

# Load data before login
df = cargar_datos()


# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "second" not in st.session_state:
    st.session_state.second = 0
if "playing" not in st.session_state:
    st.session_state.playing = False
if "speed" not in st.session_state:
    st.session_state.speed = 1

# Check if user is already logged in
if st.user and st.user.is_logged_in:
    st.session_state.logged_in = True

# Set page config as the first Streamlit command when logged in
if st.session_state.logged_in:
    st.set_page_config(page_title="Vitrification Viability via Osmotic Response", layout="wide")

# Force light mode, brighten button text, make text dark, and scale text with window size
st.markdown(
    """
    <style>
    /* Force light mode */
    body {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    .stApp {
        background-color: #ffffff !important;
    }
    /* Make login page header dark and scalable */
    h2, .stMarkdown h2 {
        color: #222222 !important;
        font-size: calc(1rem + 1vw) !important; /* Tighter header scaling */
    }
    /* Make login page write text dark and scalable */
    .stMarkdown p, .stText {
        color: #222222 !important;
        font-size: calc(0.6rem + 0.6vw) !important; /* Tighter write text scaling */
    }
    </style>

    """,
    unsafe_allow_html=True
)

# Login page
if not st.session_state.logged_in:
    st.title("Vitrification Viability via Osmotic Response Calculator")
    if st.button("Log in / Sign up"):
        st.login("auth0")
        if st.user and st.user.is_logged_in:
            st.session_state.logged_in = True
            time.sleep(0.5)  # Reduced delay
            st.rerun()

# Main app
else:
    
    # Logo de Fertilab más pequeño y centrado
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 0.5rem;">
            <a href="https://www.fertilab.com" target="_blank">
                <img src="https://fertilab.com/wp-content/uploads/2020/03/logo-fertilab-barcelona-oficial-2019.jpg" width="180">
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Título más compacto
    st.markdown(
        "<h2 style='text-align: center; margin-bottom: 1rem;'>At Least One Euploid Calculator</h2>",
        unsafe_allow_html=True
    )

    # Inputs
    edad = st.selectbox("Age", df['Edad'].tolist())
    nA = st.number_input("Grade A blastocysts", min_value=0, step=1)
    nB = st.number_input("Grade B blastocysts", min_value=0, step=1)
    nC = st.number_input("Grade C blastocysts", min_value=0, step=1)

    # Calcular probabilidad
    fila = df[df['Edad'] == edad].iloc[0]
    pA, pB, pC = fila['A'], fila['B'], fila['C']
    prob = 1 - (1 - pA)**nA * (1 - pB)**nB * (1 - pC)**nC

    # Resultado centrado y compacto
    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 1rem;">
            <div style="font-size: 40px; font-weight: bold; color: black;">
                {prob:.1%}
            </div>
            <div style="font-size: 14px; font-weight: 300; color: black;">
                Probability of at least one euploid blastocyst
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Logout button
    if st.button("Log out"):
        st.logout()
        st.session_state.logged_in = False
        logout_url = (
            "https://dev-47xxwxkuddgbl0fo.us.auth0.com/v2/logout?"
            "client_id=mTQf6FD1dPJm8SVz7sVaFh7LRlnQWMrI&"
            "returnTo=https://app-app0-app-hwq3xjpohg7cilzdu34ba8.streamlit.app"
        )
        components.html(
            f"""
            <script>
                window.location.href = "{logout_url}";
            </script>
            """,
            height=0,
        )
