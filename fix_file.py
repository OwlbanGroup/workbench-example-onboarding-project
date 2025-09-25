import re

with open("src/tutorial_app/tests/test_performance.py", "r") as f:
    content = f.read()

# Fix ::.4f to :.4f
content = content.replace("::.4f", ":.4f")

# Fix ":.4f" to :.4f
content = re.sub(r'":\.4f"', ":.4f", content)

with open("src/tutorial_app/tests/test_performance.py", "w") as f:
    f.write(content)

print("Fixed")
