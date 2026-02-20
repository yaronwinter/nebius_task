FRAMEWORK_SIGNATURES = {
    "react": ["package.json", "src/App.tsx", "next.config.js"],
    "django": ["manage.py", "settings.py"],
    "flask": ["app.py", "wsgi.py"],
    "pytorch": ["torch", "model.py"],
    "tensorflow": ["tensorflow"],
    "fastapi": ["fastapi", "uvicorn"]
}


def detect_frameworks(files, readme):
    detected = []
    text = readme.lower()

    for name, signatures in FRAMEWORK_SIGNATURES.items():
        for sig in signatures:
            if sig in text or any(sig in f for f in files):
                detected.append(name)
                break

    return list(set(detected))