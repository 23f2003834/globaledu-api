---
title: GlobalEdu Country Outline API
emoji: 🌍
colorFrom: blue
colorTo: green
sdk: docker                 # use "python" for a plain Python app, "gradio" for Gradio, etc.
sdk_version: "3.11"         # optional – only needed for the python SDK
app_file: main.py           # the file that contains `app = FastAPI()` and is run by uvicorn
pinned: false
---

# GlobalEdu Country Outline API

A **FastAPI** service that returns a **Markdown outline** of any country’s Wikipedia page.

## Quick test

```bash
curl "https://{{hf_username}}-globaledu-api.hf.space/api/outline?country=Japan"