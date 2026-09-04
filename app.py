"""
The_Og AI - Porogaramu ya Streamlit
------------------------------------
Ibice biri muri iyi porogaramu:
  1. Ikiganiro (Text Chat)      - kuvugana na AI mu nyandiko
  2. Ijwi (Voice Chat)          - kohereza / kumva ijwi
  3. Amashusho (Image Upload)   - kohereza ifoto AI ikayisesengura
  4. Isomero (Library)          - amateka y'ibiganiro byawe
  5. Plugins                    - uduce twiyongera
  6. Latest Chart                - igishushanyo cy'ikoreshwa rya porogaramu
  7. Amakuru y'ukoresha (User Info) - profile yawe

API KEY
-------
Iyi porogaramu ISOMA API key YAWE GUSA muri st.secrets (secret ya
Streamlit) cyangwa muri environment variable. NTA gace ko kuyandika
cyangwa kuyihindura kuri interface (nta text_input ya API key kuri
uru rupapuro na rimwe) -- nk'uko byasabwe.

Kugira ngo ikore, kora dosiye:  .streamlit/secrets.toml
hanyuma wandikemo:

    OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxx"

Reba README.md kuri buri ntambwe.
"""

import streamlit as st
import base64
import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# BASIC CONFIG
# ---------------------------------------------------------------------------
ASSETS_DIR = Path(__file__).parent / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"

st.set_page_config(
    page_title="The_Og AI",
    page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else "🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# API KEY -- ONLY from st.secrets / environment. Never from the UI.
# ---------------------------------------------------------------------------
def get_api_key() -> str:
    """
    Reads the API key strictly from Streamlit secrets or the environment.
    There is intentionally NO text_input anywhere in this app for the key --
    you set it once in .streamlit/secrets.toml (or your host's "Secrets"
    settings) and the app just uses it.
    """
    try:
        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass
    import os
    return os.environ.get("OPENAI_API_KEY", "")


def get_client():
    api_key = get_api_key()
    if not api_key:
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"Ikosa mu kuzana client: {e}")
        return None


API_KEY_SET = bool(get_api_key())

# ---------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------------------------------
def init_state():
    defaults = {
        "chat_history": [],
        "library": [],
        "language": "Auto",
        "username": "Umukoresha",
        "usage_log": [],
        "plugins_enabled": {
            "Web Summary Helper": False,
            "Code Explainer": False,
            "Translator Booster": False,
        },
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


init_state()

LANGUAGES = [
    "Auto (nk'uko ubajije)",
    "Ikinyarwanda",
    "English",
    "Français",
    "Kiswahili",
    "Kirundi",
    "العربية",
    "Español",
    "中文",
]

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
def log_usage(action: str):
    st.session_state["usage_log"].append(
        {"action": action, "time": datetime.datetime.now().isoformat()}
    )


def build_system_prompt():
    lang = st.session_state["language"]
    if lang.startswith("Auto"):
        lang_instruction = (
            "Always answer in the SAME language the user used in their "
            "latest message. Detect it automatically."
        )
    else:
        lang_instruction = f"Always answer in {lang}, regardless of the input language."
    return (
        "You are The_Og AI, a helpful, friendly, multilingual assistant. "
        f"{lang_instruction} Be clear, concise, and accurate."
    )


# ---------------------------------------------------------------------------
# SIDEBAR - LOGO + MAIN MENU
# ---------------------------------------------------------------------------
if LOGO_PATH.exists():
    st.sidebar.image(str(LOGO_PATH), use_container_width=True)
else:
    st.sidebar.markdown("## 🤖 The_Og AI")

st.sidebar.caption("Menu nyamukuru")

menu = st.sidebar.radio(
    "Hitamo icyo ushaka gukora:",
    [
        "💬 Ikiganiro (Chat)",
        "🎙️ Ijwi (Voice Chat)",
        "🖼️ Amashusho (Images)",
        "📚 Isomero (Library)",
        "🔌 Plugins",
        "📊 Latest Chart",
        "👤 Amakuru y'ukoresha",
    ],
)

st.sidebar.divider()
st.sidebar.selectbox("🌐 Ururimi rwo gusubiza", LANGUAGES, key="language")

st.sidebar.divider()
if API_KEY_SET:
    st.sidebar.success("✅ API key iraboneka (muri secrets)")
else:
    st.sidebar.error("⚠️ Nta API key ibonetse muri secrets.toml")
    st.sidebar.caption(
        "Ongeraho `OPENAI_API_KEY` muri `.streamlit/secrets.toml` "
        "(reba README.md)."
    )

# ---------------------------------------------------------------------------
# PAGE: TEXT CHAT
# ---------------------------------------------------------------------------
if menu.startswith("💬"):
    st.title("💬 Ikiganiro na The_Og AI")

    if not API_KEY_SET:
        st.warning(
            "⚠️ Nta API key ibonetse. Ongeraho `OPENAI_API_KEY` muri "
            "`.streamlit/secrets.toml` cyangwa muri 'Secrets' z'urubuga "
            "rukoresha (Streamlit Cloud), maze wongere ufungure app."
        )

    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input("Andika ikibazo cyawe hano...")
    if prompt:
        st.session_state["chat_history"].append(
            {"role": "user", "content": prompt, "time": str(datetime.datetime.now())}
        )
        with st.chat_message("user"):
            st.write(prompt)

        client = get_client()
        with st.chat_message("assistant"):
            if client is None:
                reply = (
                    "⚠️ Nta API key ibonetse muri secrets.toml. Reba "
                    "README.md kugira ngo umenye uko uyishyiramo."
                )
                st.warning(reply)
            else:
                try:
                    messages = [{"role": "system", "content": build_system_prompt()}]
                    messages += [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state["chat_history"]
                    ]
                    with st.spinner("The_Og AI iratekereza..."):
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=messages,
                        )
                    reply = response.choices[0].message.content
                    st.write(reply)
                    log_usage("text_chat")
                except Exception as e:
                    reply = f"Ikosa: {e}"
                    st.error(reply)

        st.session_state["chat_history"].append(
            {"role": "assistant", "content": reply, "time": str(datetime.datetime.now())}
        )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Siba ikiganiro"):
            st.session_state["chat_history"] = []
            st.rerun()
    with col2:
        if st.button("📥 Bika iki kiganiro mu Isomero"):
            if st.session_state["chat_history"]:
                st.session_state["library"].append(
                    {
                        "title": f"Ikiganiro - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
                        "messages": list(st.session_state["chat_history"]),
                    }
                )
                st.success("Ikiganiro cyabitswe mu Isomero!")

# ---------------------------------------------------------------------------
# PAGE: VOICE CHAT
# ---------------------------------------------------------------------------
elif menu.startswith("🎙️"):
    st.title("🎙️ Ijwi - Voice Chat")
    st.write(
        "Vuga ikibazo cyawe (record audio) cyangwa ukohereze dosiye y'ijwi, "
        "The_Og AI izakumva ikandika ibyo uvuze, hanyuma igusubize mu "
        "nyandiko no/cyangwa mu ijwi."
    )

    if not API_KEY_SET:
        st.warning(
            "⚠️ Nta API key ibonetse. Ongeraho `OPENAI_API_KEY` muri "
            "`.streamlit/secrets.toml`."
        )

    client = get_client()

    audio_value = st.audio_input("🎤 Kanda hano uvuge ikibazo cyawe")
    uploaded_audio = st.file_uploader(
        "Cyangwa ohereza dosiye y'ijwi (mp3, wav, m4a)",
        type=["mp3", "wav", "m4a", "ogg"],
    )

    audio_source = audio_value or uploaded_audio

    tts_on = st.checkbox("🔊 Nsubize mu ijwi (Text-to-Speech)", value=True)

    if audio_source is not None:
        st.audio(audio_source)
        if st.button("▶️ Ohereza kuri The_Og AI"):
            if client is None:
                st.warning("⚠️ Nta API key ibonetse muri secrets.toml.")
            else:
                try:
                    with st.spinner("Ndumva icyo uvuze..."):
                        tmp_path = "/tmp/voice_input.wav"
                        with open(tmp_path, "wb") as f:
                            f.write(audio_source.getvalue())
                        with open(tmp_path, "rb") as f:
                            transcript = client.audio.transcriptions.create(
                                model="whisper-1", file=f
                            )
                    user_text = transcript.text
                    st.markdown(f"**Icyo wavuze:** {user_text}")

                    with st.spinner("The_Og AI iratekereza..."):
                        messages = [
                            {"role": "system", "content": build_system_prompt()},
                            {"role": "user", "content": user_text},
                        ]
                        response = client.chat.completions.create(
                            model="gpt-4o-mini", messages=messages
                        )
                        reply_text = response.choices[0].message.content

                    st.markdown("**Igisubizo cya The_Og AI:**")
                    st.write(reply_text)
                    log_usage("voice_chat")

                    if tts_on:
                        with st.spinner("Ntegura ijwi ryo gusubiza..."):
                            speech_path = "/tmp/voice_reply.mp3"
                            with client.audio.speech.with_streaming_response.create(
                                model="tts-1", voice="alloy", input=reply_text
                            ) as tts_response:
                                tts_response.stream_to_file(speech_path)
                        st.audio(speech_path)

                    st.session_state["chat_history"].append(
                        {"role": "user", "content": user_text, "time": str(datetime.datetime.now())}
                    )
                    st.session_state["chat_history"].append(
                        {"role": "assistant", "content": reply_text, "time": str(datetime.datetime.now())}
                    )
                except Exception as e:
                    st.error(f"Ikosa: {e}")
    else:
        st.info("Tegereza cyangwa ohereza ijwi ryawe hejuru kugira ngo tubone gutangira.")

# ---------------------------------------------------------------------------
# PAGE: IMAGE UPLOAD
# ---------------------------------------------------------------------------
elif menu.startswith("🖼️"):
    st.title("🖼️ Amashusho - Image Analysis")
    st.write("Ohereza ifoto, The_Og AI izakwereka ibyo irimo cyangwa ikubwire ibyo uyibajije.")

    if not API_KEY_SET:
        st.warning(
            "⚠️ Nta API key ibonetse. Ongeraho `OPENAI_API_KEY` muri "
            "`.streamlit/secrets.toml`."
        )

    client = get_client()

    image_file = st.file_uploader(
        "Ohereza ifoto (jpg, jpeg, png, webp)", type=["jpg", "jpeg", "png", "webp"]
    )
    question = st.text_input(
        "Ikibazo ku ifoto (urugero: 'Ni iki kiri muri iyi foto?')",
        value="Sobanura neza ibiri muri iyi foto.",
    )

    if image_file is not None:
        st.image(image_file, caption="Ifoto wohereje", width=400)

        if st.button("🔍 Sesengura ifoto"):
            if client is None:
                st.warning("⚠️ Nta API key ibonetse muri secrets.toml.")
            else:
                try:
                    with st.spinner("Ndimo gusesengura ifoto..."):
                        b64_image = base64.b64encode(image_file.getvalue()).decode("utf-8")
                        mime = image_file.type or "image/png"
                        messages = [
                            {"role": "system", "content": build_system_prompt()},
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": question},
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": f"data:{mime};base64,{b64_image}"},
                                    },
                                ],
                            },
                        ]
                        response = client.chat.completions.create(
                            model="gpt-4o-mini", messages=messages
                        )
                        answer = response.choices[0].message.content
                    st.success("Byarangiye!")
                    st.write(answer)
                    log_usage("image_analysis")

                    st.session_state["chat_history"].append(
                        {"role": "user", "content": f"[Ifoto] {question}", "time": str(datetime.datetime.now())}
                    )
                    st.session_state["chat_history"].append(
                        {"role": "assistant", "content": answer, "time": str(datetime.datetime.now())}
                    )
                except Exception as e:
                    st.error(f"Ikosa: {e}")

# ---------------------------------------------------------------------------
# PAGE: LIBRARY
# ---------------------------------------------------------------------------
elif menu.startswith("📚"):
    st.title("📚 Isomero (Library)")
    st.write("Hano ni ho ibiganiro wabitse bigaragara.")

    if not st.session_state["library"]:
        st.info("Nta kiganiro cyabitswe kugeza ubu. Jya muri 'Ikiganiro' ukanda 'Bika mu Isomero'.")
    else:
        for entry in reversed(st.session_state["library"]):
            with st.expander(entry["title"]):
                for m in entry["messages"]:
                    st.markdown(f"**{m['role']}:** {m['content']}")

        if st.button("🗑️ Siba Isomero ryose"):
            st.session_state["library"] = []
            st.rerun()

# ---------------------------------------------------------------------------
# PAGE: PLUGINS
# ---------------------------------------------------------------------------
elif menu.startswith("🔌"):
    st.title("🔌 Plugins")
    st.write(
        "Fungura cyangwa uzimye ibikoresho by'inyongera. Wongeraho izindi "
        "'plugins' wifuza."
    )

    for name in list(st.session_state["plugins_enabled"].keys()):
        st.session_state["plugins_enabled"][name] = st.toggle(
            name, value=st.session_state["plugins_enabled"][name]
        )

    st.divider()
    st.subheader("➕ Ongeraho Plugin nshya (custom)")
    new_plugin = st.text_input("Izina rya plugin nshya")
    if st.button("Ongeraho") and new_plugin.strip():
        st.session_state["plugins_enabled"][new_plugin.strip()] = True
        st.success(f"Plugin '{new_plugin}' yongeyweho!")
        st.rerun()

# ---------------------------------------------------------------------------
# PAGE: LATEST CHART
# ---------------------------------------------------------------------------
elif menu.startswith("📊"):
    st.title("📊 Latest Chart - Ikoreshwa rya The_Og AI")

    log = st.session_state["usage_log"]
    if not log:
        st.info("Nta mibare iraboneka. Koresha porogaramu (chat, ijwi, ifoto) kugira ngo hagaragare ibipimo.")
    else:
        import pandas as pd

        df = pd.DataFrame(log)
        df["date"] = pd.to_datetime(df["time"]).dt.date
        counts = df.groupby(["date", "action"]).size().unstack(fill_value=0)
        st.bar_chart(counts)

        st.subheader("Incamake")
        st.dataframe(df[["action", "time"]].sort_values("time", ascending=False))

# ---------------------------------------------------------------------------
# PAGE: USER INFO
# ---------------------------------------------------------------------------
elif menu.startswith("👤"):
    st.title("👤 Amakuru y'ukoresha")

    st.session_state["username"] = st.text_input(
        "Izina ryawe", value=st.session_state["username"]
    )

    st.write("### Incamake y'ikoreshwa")
    st.metric("Ubutumwa mu kiganiro", len(st.session_state["chat_history"]))
    st.metric("Ibiganiro byabitswe mu Isomero", len(st.session_state["library"]))
    st.metric("Ibikorwa byose byakozwe", len(st.session_state["usage_log"]))

    st.write("### Igenamiterere ry'iyi app")
    st.json(
        {
            "username": st.session_state["username"],
            "language": st.session_state["language"],
            "api_key_source": "st.secrets['OPENAI_API_KEY']",
            "api_key_set": API_KEY_SET,
            "plugins_enabled": st.session_state["plugins_enabled"],
        }
    )
