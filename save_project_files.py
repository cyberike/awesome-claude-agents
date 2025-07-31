import os

def save_project_files(files, project_path):
    os.makedirs(project_path, exist_ok=True)
    for file in files:
        filename = file.get("filename")
        content = file.get("content")
        if not filename or not content:
            print(f"⚠️ Invalid file skipped: {file}")
            continue
        full_path = os.path.join(project_path, filename)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"📄 Saved: {full_path}")
