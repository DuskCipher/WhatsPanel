import streamlit as st
import pandas as pd
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def scrape_google_maps(keyword, max_results, delay_time):
    try:
        options = Options()
        # options.add_argument('--headless')  # Aktifkan untuk mode tanpa GUI
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--window-size=1920x1080')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        wait = WebDriverWait(driver, 15)

        driver.get("https://www.google.com/maps")
        search_box = wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)

        time.sleep(5)

        scrollable_div = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]')))
        last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)

        results = []
        while len(results) < max_results:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            time.sleep(2)
            new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
            if new_height == last_height:
                break
            last_height = new_height
            results = driver.find_elements(By.CLASS_NAME, "hfpxzc")

        st.info(f"🔎 Total ditemukan: {len(results)} tempat")
        data = []

        for idx, r in enumerate(results[:max_results]):
            try:
                driver.execute_script("arguments[0].click();", r)
                time.sleep(delay_time)

                name = driver.find_element(By.CSS_SELECTOR, 'h1.DUwDvf').text

                # Rating
                try:
                    rating = driver.find_element(By.CLASS_NAME, 'F7nice').text
                except:
                    try:
                        rating = driver.find_element(By.CLASS_NAME, 'MW4etd').text
                    except:
                        try:
                            rating = driver.find_element(By.XPATH, '//span[contains(text(),"★")]').text
                        except:
                            rating = "-"

                # Alamat
                try:
                    address = driver.find_element(By.CSS_SELECTOR, '[data-item-id="address"]').text
                except:
                    address = "-"

                # Telepon
                try:
                    phone = driver.find_element(By.CSS_SELECTOR, '[data-tooltip="Salin nomor telepon"]').text
                except:
                    phone = "-"

                # Kategori / Jenis Usaha
                try:
                    category = driver.find_element(By.XPATH, '//button[contains(@jsaction, "pane.rating.category")]').text
                except:
                    try:
                        category = driver.find_element(By.XPATH, '//div[contains(@aria-label, "Kategori") or contains(@class,"fontBodyMedium")]').text
                    except:
                        category = "-"

                # Website
                try:
                    website = driver.find_element(By.XPATH, '//a[contains(@href, "http") and @data-item-id="authority"]').get_attribute('href')
                except:
                    try:
                        website = driver.find_element(By.XPATH, '//a[contains(@href, "http") and contains(text(), "Website")]').get_attribute('href')
                    except:
                        website = "-"

                data.append({
                    "Nama": name,
                    "Rating": rating,
                    "Alamat": address,
                    "Telepon": phone,
                    "Kategori": category,
                    "Website": website
                })

                st.success(f"✅ {idx+1}. {name}")

            except Exception as e:
                st.warning(f"❗ Gagal mengambil detail tempat ke-{idx+1}: {e}")
                continue

        driver.quit()
        return data

    except Exception as e:
        return f"❌ Error scraping:\n{e}\n\n{traceback.format_exc()}"

def maps_scraper_app():
    st.markdown("""
    <h1 style='text-align: center;'>📍 Scraper Google Maps Lengkap</h1>
    <p>Masukkan kata kunci pencarian, jumlah hasil, dan delay scraping untuk hasil terbaik.</p>
    """, unsafe_allow_html=True)

    kata_kunci = st.text_input("🔍 Kata Kunci", "Bengkel mobil Purwokerto")
    max_data = st.slider("📊 Jumlah hasil", 1, 30, 10)
    delay_time = st.number_input("⏱️ Jeda antar scraping (detik)", min_value=1.0, max_value=10.0, value=4.0, step=0.5)

    if st.button("🚀 Mulai Scraping"):
        st.info("🕐 Memulai scraping, mohon tunggu...")
        data = scrape_google_maps(kata_kunci, max_data, delay_time)

        if isinstance(data, str):
            st.error(data)
        elif not data:
            st.warning("⚠ Tidak ada data yang ditemukan.")
        else:
            st.success(f"✅ Berhasil mendapatkan {len(data)} data!")
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.download_button("⬇️ Download sebagai CSV", df.to_csv(index=False), file_name="maps_data.csv", mime="text/csv")

if __name__ == "__main__":
    maps_scraper_app()