# Legal Contract Intelligence Engine V2

## Quickstart

1. Install requirements:

```bash
pip install -r requirements.txt
```

2. Run FastAPI backend:

```bash
uvicorn app.main:app --reload --app-dir V2
```

3. POST a PDF or DOCX contract to `/parse`.

## Structure
See the project plan for phase/module details. To extend, add your logic in `core/` modules.