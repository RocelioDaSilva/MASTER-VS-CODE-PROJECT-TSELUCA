import os, sys

print("CWD:", os.getcwd())
print("PYTHON:", sys.executable)
print("sys.path[0]:", sys.path[0])
print("Files in project root:", sorted(os.listdir("."))[:50])
print("Files in scripts/:", sorted(os.listdir("scripts")))
