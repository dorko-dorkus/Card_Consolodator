import subprocess
import sys
import os

PYTHON = sys.executable

ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT, "backend")
FRONTEND_DIR = os.path.join(ROOT, "frontend")


def ensure_backend_env():
    """Ensure backend/.env exists; copy from example if missing."""
    env_file = os.path.join(BACKEND_DIR, ".env")
    example_file = os.path.join(BACKEND_DIR, ".env.example")
    if not os.path.exists(env_file) and os.path.exists(example_file):
        print(f"Creating default environment file: {env_file}")
        import shutil

        shutil.copy(example_file, env_file)
    return env_file, example_file


def load_env(path):
    """Load a simple KEY=VALUE env file into a dict."""
    env = {}
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                env[key] = val
    return env


def prompt_missing_env(env_file, example_file):
    """Prompt user for any missing or placeholder values and update the file."""
    env = load_env(env_file)
    example_env = load_env(example_file)

    # include keys present in the example but missing in env
    for key, val in example_env.items():
        env.setdefault(key, val)

    updated = False
    for key, val in env.items():
        placeholder = (
            not val
            or val.upper().startswith("REPLACE_WITH")
            or "CHANGE_ME" in val
        )
        if placeholder:
            user_val = input(f"Enter value for {key}: ").strip()
            if user_val:
                env[key] = user_val
                updated = True

    if updated:
        with open(env_file, "w") as f:
            for k, v in env.items():
                f.write(f"{k}={v}\n")
        print(f"Updated {env_file} with provided values.\n")


def run(cmd, cwd=None):
    print(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=cwd)


def install_backend():
    req_file = os.path.join(BACKEND_DIR, "requirements.txt")
    run([PYTHON, "-m", "pip", "install", "--user", "-r", req_file])
    # ensure pyinstaller is available
    run([PYTHON, "-m", "pip", "install", "--user", "pyinstaller"])
    # build executable
    run([PYTHON, "-m", "PyInstaller", "--onefile", "run.py"], cwd=BACKEND_DIR)


def install_frontend():
    if os.path.exists(os.path.join(FRONTEND_DIR, "package.json")):
        run(["npm", "install"], cwd=FRONTEND_DIR)


def main():
    env_file, example_file = ensure_backend_env()
    prompt_missing_env(env_file, example_file)
    install_backend()
    install_frontend()
    print("Build complete. Backend executable is located in backend/dist/.")


if __name__ == "__main__":
    main()
