"""Новый проект мультика из озвучки.
Запуск из корня репозитория:
    python3 .claude/skills/mult-2d/lib/new_project.py in/voice.mp3 projects/my-mult [--lang ru] [--model small]
Делает: копирует шаблон, переводит звук в assets/audio/vo.wav, расшифровывает по словам в transcript.json.
"""
import argparse, pathlib, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "template"

ap = argparse.ArgumentParser()
ap.add_argument("audio"); ap.add_argument("project")
ap.add_argument("--lang", default="ru"); ap.add_argument("--model", default="small")
a = ap.parse_args()

proj = pathlib.Path(a.project)
if proj.exists() and any(proj.iterdir()):
    sys.exit(f"папка {proj} уже есть и не пустая, выбери другое имя")
shutil.copytree(TEMPLATE, proj, dirs_exist_ok=True)
vo = proj / "assets" / "audio" / "vo.wav"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a.audio, "-ar", "48000", "-ac", "1", str(vo)], check=True)
subprocess.run(["npx", "--yes", "hyperframes@0.9.45", "transcribe", "assets/audio/vo.wav", "--language", a.lang,
                "--model", a.model, "--json"], cwd=proj, check=True)
for cand in (proj / "assets" / "audio" / "transcript.json", proj / "transcript.json"):
    if cand.exists() and cand != proj / "transcript.json":
        cand.replace(proj / "transcript.json")
dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(vo)],
                     capture_output=True, text=True).stdout.strip()
print(f"проект готов: {proj}  длительность {float(dur):.1f} с  слова: {proj / 'transcript.json'}")
