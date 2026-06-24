import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from deep_translator import GoogleTranslator

st.set_page_config(page_title="Классификация статей", layout="centered")
st.title("Классификация текста статьи")
st.markdown("Введите текст статьи, и модель предскажет её категорию.")

API_URL = "http://backend:8080/classify"

user_text = st.text_area("Текст статьи:", height=200)

if st.button("Классифицировать"):
    if not user_text.strip():
        st.warning("Пожалуйста, введите текст.")
    else:
        with st.spinner("Отправка запроса к модели..."):
            try:
                en_text = GoogleTranslator(source='auto', target='en').translate(user_text)
                response = requests.post(API_URL, json={"text": en_text}, timeout=10)
                response.raise_for_status()
                data = response.json()

                st.success(f"**Категория:** {data['category']}")
                st.metric("Уверенность", f"{data['confidence']:.2%}")

                top3 = data["top3"]
                df = pd.DataFrame(top3)
                df = df.set_index("category")

                fig, ax = plt.subplots(figsize=(6, 4))
                bars = ax.bar(df.index, df["probability"], color=["#4CAF50", "#FFC107", "#F44336"])
                ax.set_ylim(0, 1)
                ax.set_ylabel("Вероятность")
                ax.set_title("Топ-3 категории")
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                            f"{height:.2%}", ha="center", va="bottom")
                st.pyplot(fig)

                st.caption("Детальные вероятности")
                st.dataframe(df.style.format("{:.2%}"))

            except requests.exceptions.ConnectionError:
                st.error("Не удалось подключиться к API. Убедитесь, что FastAPI запущен на порту 8080.")
            except requests.exceptions.Timeout:
                st.error("Превышено время ожидания ответа от сервера.")
            except requests.exceptions.HTTPError as e:
                st.error(f"Ошибка сервера: {e.response.status_code} - {e.response.text}")
            except Exception as e:
                st.error(f"Произошла ошибка: {e}")