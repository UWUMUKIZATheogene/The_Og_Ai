# The_Og AI 🎥🤖

Porogaramu ya Streamlit ifite logo yawe bwite, ifite:
- 💬 **Ikiganiro (Text Chat)**
- 🎙️ **Ijwi (Voice Chat)** — kuvuga, AI ikumva (Whisper) ikanasubiza mu ijwi (TTS)
- 🖼️ **Amashusho (Image Upload)** — gusesengura amashusho
- 📚 **Isomero (Library)** — amateka y'ibiganiro
- 🔌 **Plugins**
- 📊 **Latest Chart** — ikoreshwa rya porogaramu
- 👤 **Amakuru y'ukoresha**
- 🌐 Gusubiza mu **ndimi nyinshi**

## Ibiri muri iyi paki (files)

```
the_og_ai_streamlit/
├── app.py                          <- porogaramu nyamukuru
├── requirements.txt                <- ibikoresho bya Python bikenewe
├── .gitignore                      <- kubuza secrets.toml kujya kuri Git
├── assets/
│   └── logo.png                    <- logo yawe (The_OGEN)
└── .streamlit/
    └── secrets.toml.example        <- template y'aho ushyira API key
```

## Intambwe 1: Shiraho ibikoresho

```bash
pip install -r requirements.txt
```

## Intambwe 2: Shyiramo API Key YAWE muri Streamlit Secrets

**Iyi ni yo ntambwe y'ingenzi**: API key ntabwo yinjizwa kuri interface
(nta text_input yabigenewe kuri uru rupapuro na rimwe) — yinjizwa gusa
muri dosiye ya "secrets" ya Streamlit.

### Ku mudasobwa wawe (locally)

1. Kopera `.streamlit/secrets.toml.example` uyite `.streamlit/secrets.toml`
   (siba `.example` ku izina).
2. Fungura `secrets.toml`, usimbuze umurongo:
   ```toml
   OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   ```
   na key yawe nyayo iva kuri platform.openai.com.
3. Bika dosiye. Iyi dosiye ntabwo igomba kujya kuri GitHub cyangwa
   ahandi hantu rusange (`.gitignore` yayikingiye).

### Ku Streamlit Community Cloud (niba uhasize porogaramu)

1. Injira kuri [share.streamlit.io](https://share.streamlit.io) kuri
   app yawe.
2. Kanda **"⋮" → Settings → Secrets**.
3. Wandikemo:
   ```toml
   OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   ```
4. Bika ("Save"). Streamlit izahita ihindura app yawe kugira ngo
   ikoreshe iyo key nshya.

## Intambwe 3: Tangiza porogaramu

```bash
streamlit run app.py
```

Porogaramu izafungura kuri browser yawe (urugero: http://localhost:8501),
igaragaze logo yawe muri sidebar, kandi niba `secrets.toml` yujuje neza
key, uzabona akadomo k'icyatsi "✅ API key iraboneka" muri sidebar.

## Icyitonderwa

- Iyi porogaramu ikoresha `openai` Python SDK. Ushobora no gukoresha
  izindi seriveri "OpenAI-compatible" uhinduye gato muri `get_client()`
  muri `app.py` (urugero: Groq, OpenRouter, n'izindi).
- Amakuru y'ibiganiro (chat history, library, usage log) abikwa gusa
  muri `st.session_state` -- bivuze ko igihe wongeye gufungura porogaramu
  bisubira ku ntangiriro (nta database ikoreshwa muri iyi verisiyo).
- Ku ijwi (Voice Chat), dukoresha `st.audio_input` (kuvuga mu
  microphone) hamwe na Whisper (kumva) na TTS (kuvuga).
- Ku mashusho, dukoresha model ifite ubushobozi bwo kureba amashusho
  (vision), urugero `gpt-4o-mini`.

## Niba ubonye ikosa rya "429 - insufficient_quota"

Ibi ntabwo ari ikosa rya code -- bivuze ko konti yawe ya OpenAI nta
credits isigaje. Jya kuri
https://platform.openai.com/settings/organization/billing/ maze
wongereho amafaranga make, hanyuma ugerageze nanone.

## Kwiyongeraho (Next steps)

- Ongeramo indi model (Anthropic, Google Gemini, n'ibindi) niba ushaka
  guhitamo hagati ya providers nyinshi.
- Ongeramo "Plugins" nyazo (urugero: gushakisha kuri internet, kubara
  imibare, gukora summary y'inyandiko ndende).
- Ongeramo database (urugero: SQLite cyangwa Supabase) kugira ngo
  Isomero ribikwe burundu, ntabwo ryonyine mu gihe cy'imikoreshereze.
