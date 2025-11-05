# frontend/app.py
import os
import re
import requests
import streamlit as st
from datetime import date
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

API_URL = os.environ.get("API_URL", "http://localhost:8000").rstrip("/")

def _session():
    s = requests.Session()
    retries = Retry(
        total=3, backoff_factor=0.25,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    s.mount("http://", HTTPAdapter(max_retries=retries))
    s.mount("https://", HTTPAdapter(max_retries=retries))
    return s


@st.cache_data(show_spinner=False, ttl=30)
def fetch_log(date_str: str) -> str:
    r = _session().get(f"{API_URL}/log/{date_str}", timeout=10)
    r.raise_for_status()
    return r.text  # PlainTextResponse


def count_errors(text: str) -> int:
    return len(re.findall(r"\berror\b", text, flags=re.IGNORECASE))


def fmt(d: date) -> str:
    # matches backend filename pattern logs/log-YYYY-MM-DD.txt
    return d.strftime("%Y-%m-%d")


st.set_page_config(page_title="Log Viewer", layout="wide")

st.title("Log Viewer")
st.caption(f"Backend: {API_URL}")

# --- Inputs (no sidebar) ---
col1, col2 = st.columns([2,1], vertical_alignment="bottom")
with col1:
    date_pick = st.date_input("Date", value=date.today())
with col2:
    fetch = st.button("Fetch log", type="primary", use_container_width=True)

date_str = fmt(date_pick)

# --- Output ---
if fetch:
    with st.spinner("Fetching…"):
        try:
            txt = fetch_log(date_str)
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                st.warning(f"No log for {date_str}.")
            else:
                code = getattr(e.response, "status_code", "unknown")
                st.error(f"HTTP error {code}")
                if getattr(e.response, "text", ""):
                    st.code(e.response.text[:500], language="text")
        except requests.Timeout:
            st.error("Backend timed out. Is it running?")
        except requests.ConnectionError:
            st.error(f"Cannot connect to {API_URL}. Check host/port.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
        else:
            # Quick metrics
            lines = txt.splitlines()
            errors = count_errors(txt)
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Lines", f"{len(lines):,}")
            m2.metric("# Errors", f"{errors}")
            m3.metric("Bytes (UTF-8)", f"{len(txt.encode('utf-8')):,}")
            m4.metric("Date", date_str)

            st.download_button(
                f"Download log-{date_str}.txt",
                data=txt,
                file_name=f"log-{date_str}.txt",
                mime="text/plain",
                use_container_width=True,
            )

            # show content (no sidebar toggles)
            st.code(txt if txt else "(empty file)", language="text")