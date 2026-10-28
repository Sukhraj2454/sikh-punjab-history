#!/usr/bin/env python3
"""Generate one chronological source-aware Virasat lesson per scheduled run.

Requires OPENAI_API_KEY in GitHub Actions repository secrets.
Never runs on an absent key, and never silently publishes duplicate IDs.
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

PATH = Path("lessons.json")
KEY = os.environ.get("OPENAI_API_KEY")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1")
if not KEY:
    raise SystemExit("OPENAI_API_KEY missing. Add the repository Actions secret to activate auto-publishing.")

data = json.loads(PATH.read_text(encoding="utf-8"))
if not isinstance(data, list) or not data:
    raise SystemExit("lessons.json must be a nonempty list.")
next_id = max(item["id"] for item in data) + 1
now = datetime.now(ZoneInfo("Asia/Kolkata"))
slot = "morning" if now.hour < 14 else "evening"
slot_key = now.strftime("%Y-%m-%d") + "-" + slot
if any(item.get("published_slot") == slot_key for item in data):
    print("This publication slot already exists; skipping.")
    raise SystemExit(0)

# Fixed chronology is a guide, not a claim that each item takes one lesson.
syllabus = [
    "Guru Nanak's southern Udasi traditions: Sri Lanka and Raja Shivnabh",
    "Guru Nanak's northern journeys and encounters with Siddhas",
    "Siddh Gosht: preserved Gurbani and the yogic dialogue",
    "Guru Nanak's western journeys: Mecca and Baghdad as Janamsakhi tradition",
    "Babur's invasions and Babarvani in Sri Guru Granth Sahib",
    "Kartarpur: farming, sangat and langar",
    "Bhai Lehna and the succession to Guru Angad Dev Ji",
    "Guru Angad Dev Ji: Gurmukhi, institutions, and succession",
    "Guru Amar Das Ji: Goindwal, manjis and langar",
    "Guru Ram Das Ji: Ramdaspur and early Amritsar",
    "Guru Arjan Dev Ji: Adi Granth, Harmandir Sahib and martyrdom",
    "Guru Hargobind Sahib: Miri Piri and Akal Takht",
    "Guru Har Rai Ji and Guru Har Krishan Ji",
    "Guru Tegh Bahadur Sahib: travels and martyrdom",
    "Guru Gobind Singh Ji: Anandpur, Khalsa and 1699",
    "Guru Gobind Singh Ji: conflicts, Zafarnama and 1708",
    "Banda Singh Bahadur and early Khalsa sovereignty",
    "Sikh persecution, the Ghallugharas, Dal Khalsa and Sikh misls",
    "Maharaja Ranjit Singh and the Sikh Empire",
    "Anglo-Sikh Wars and the annexation of Punjab",
    "Colonial Punjab, reform movements and Gurdwara reform",
    "Punjab in independence and Partition in 1947",
    "Post-independence Punjab, Punjabi Suba and subsequent history",
]
index = next_id - 7  # first six lessons already present
topic = syllabus[index] if index < len(syllabus) else "Next chronological topic in Sikh and Punjab history after: " + data[-1]["title"]
history = [f'{x["id"]}: {x["title"]}' for x in data[-12:]]
instructions = f"""Write ONE NEW source-conscious, chronological educational lesson for Virasat.
Topic: {topic}
Previously published: {'; '.join(history)}.
Avoid covering previous lessons again. For broad topics progress in smaller chronological steps.
Use directly verifiable scripture (Sri Guru Granth Sahib Ji, with real Ang numbers), Basics of Sikhi/WhyGuru, Encyclopaedia of Sikhism, and historical scholarship by J. S. Grewal or Khushwant Singh.
Clearly label Janamsakhi/traditional sakhis as tradition and differentiate from established historical records.
Do not invent direct quotations, exact dates, unverifiable claims, citations or URLs. If uncertain omit rather than guess.
Produce accessible rich text, aiming for a 7-10 minute study session. Return JSON ONLY with keys:
title (string), period (string), era (string), intro (2-3 substantial paragraphs separated by blank lines), record (2-3 substantial paragraphs with precise attribution to scripture/book and context), tradition (2-3 substantial paragraphs with named provenance and limitations), recap (6-10 concise sentences), questions (array of exactly 3 meaningful factual questions), references (array of 2-6 named reliable publications/Ang references; no fabricated links).
No personal interpretations, no first person, no promotional language. No other fields.
"""
payload = {
    "model": MODEL,
    "input": [
        {"role": "system", "content": "You are a careful historical learning editor. Output only valid JSON. Never claim you have independently checked a source you have not actually inspected."},
        {"role": "user", "content": instructions}
    ],
    "text": {"format": {"type": "json_object"}},
    "max_output_tokens": 5000,
}
request = Request("https://api.openai.com/v1/responses", data=json.dumps(payload).encode(),
    headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"}, method="POST")
with urlopen(request, timeout=120) as response:
    raw = json.load(response)
segments = [c.get("text", "") for output in raw.get("output", []) for c in output.get("content", []) if c.get("type") == "output_text"]
if not segments:
    raise SystemExit("Model response missing output_text; leaving lessons unchanged.")
lesson = json.loads("".join(segments))
required = ["title", "period", "era", "intro", "record", "tradition", "recap", "questions", "references"]
if any(k not in lesson for k in required):
    raise SystemExit("Lesson failed schema check; leaving lessons unchanged.")
if not all(isinstance(lesson[k], str) and len(lesson[k]) >= 25 for k in required[:7]):
    raise SystemExit("Lesson text incomplete; leaving lessons unchanged.")
if not isinstance(lesson["questions"], list) or len(lesson["questions"]) != 3:
    raise SystemExit("Expected exactly three recall questions.")
if not isinstance(lesson["references"], list) or len(lesson["references"]) < 2:
    raise SystemExit("Expected at least two reference descriptions.")
if lesson["title"].strip().casefold() in [x["title"].casefold() for x in data]:
    raise SystemExit("Duplicate title rejected.")
lesson["id"] = next_id
lesson["published_slot"] = slot_key
lesson["generated_at"] = now.isoformat()
lesson["editorial_status"] = "AI-generated draft — verify sources"
data.append(lesson)
PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Created lesson {next_id}: {lesson['title']} for {slot_key}.")
