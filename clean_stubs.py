import os

# Folders where agents live
subdirs = ["agents/orchestrators", "agents/specialized", "agents/universal"]

# Optional: only delete files that contain "Stub handling task"
stub_identifier = "Stub handling task:"

deleted_files = []

for subdir in subdirs:
    if not os.path.exists(subdir):
        continue
    for filename in os.listdir(subdir):
        if filename.endswith(".py"):
            full_path = os.path.join(subdir, filename)
            with open(full_path, "r", encoding="utf-8") as f:
                contents = f.read()
            if stub_identifier in contents:
                os.remove(full_path)
                deleted_files.append(full_path)

if deleted_files:
    print("🧹 Deleted stub files:")
    for file in deleted_files:
        print(" -", file)
else:
    print("✅ No stubs found to delete.")
