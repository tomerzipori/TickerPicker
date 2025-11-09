#!/usr/bin/env bash

# Run backend
nohup uvicorn backend:app --reload --port 8000 &

# Waut for backend
sleep 2

# Run frontend
streamlit run frontend.py