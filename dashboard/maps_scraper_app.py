# dashboard/maps_scraper_app.py

import streamlit as st
import pandas as pd
import requests

def scrape_maps_serpapi(query, api_key, max_results):
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_maps",
        "q": query,
        "type": "search",
        "api_key": api_key
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return pd.DataFrame(), f"Gagal mengambil data dari SerpAPI: {response.status_code}"

        results = response.json().get("local_results", [])
        data = []
        for r in results[:max_results]:
            data.append({
                "Nama": r.get("title"),
                "Rating": r.get("rating"),
                "Ulasan": r.get("reviews"),
                "Alamat": r.get("address"),
                "Telepon": r.get("phone"),
                "Kategori": r.get("type"),
                "Website": r.get("website")
            })

        return pd.DataFrame(data), None

    except Exception as e:
        return pd.DataFrame(), f"Terjadi error: {str(e)}"


def scrape_search_serpapi(query, api_key, max_results):
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return pd.DataFrame(), f"Gagal mengambil data dari SerpAPI: {response.status_code}"

        results = response.json().get("organic_results", [])
        data = []
        for r in results[:max_results]:
            data.append({
                "Judul": r.get("title"),
                "Link": r.get("link"),
                "Deskripsi": r.get("snippet")
            })

        return pd.DataFrame(data), None

    except Exception as e:
        return pd.DataFrame(), f"Terjadi error: {str(e)}"


def maps_scraper_app():
    st.title("🧭 SerpAPI Scraper: Maps & Search")

    with st.expander("🔐 Masukkan API Key SerpAPI"):
        api_key = st.text_input("API Key", type="password", placeholder="Masukkan API Key SerpAPI kamu")

    search_type = st.radio("Pilih Jenis Scraping", ["📍 Google Maps", "🔍 Google Search"], horizontal=True)
    query = st.text_input("🔎 Kata Kunci", "Bengkel mobil Purwokerto")
    max_results = st.slider("📊 Jumlah hasil", 1, 90, 10)

    if st.button("🚀 Mulai Scraping"):
        if not api_key:
            st.error("❌ Mohon masukkan API Key terlebih dahulu.")
        else:
            with st.spinner("⏳ Mengambil data dari SerpAPI..."):
                if "Maps" in search_type:
                    df, error = scrape_maps_serpapi(query, api_key, max_results)
                else:
                    df, error = scrape_search_serpapi(query, api_key, max_results)

            if error:
                st.error(error)
            elif df.empty:
                st.warning("⚠️ Tidak ada hasil ditemukan.")
            else:
                st.success(f"✅ Berhasil mendapatkan {len(df)} data.")
                st.dataframe(df)
                st.download_button("⬇️ Download CSV", df.to_csv(index=False), file_name="hasil_scraper.csv")
