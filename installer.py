import subprocess
import sys
import os

PYTHON = sys.executable

ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT, 'backend')
FRONTEND_DIR = os.path.join(ROOT, 'frontend')

def run(cmd, cwd=None):
    print(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=cwd)


def install_backend():
    req_file = os.path.join(BACKEND_DIR, 'requirements.txt')
    run([PYTHON, '-m', 'pip', 'install', '--user', '-r', req_file])
    # ensure pyinstaller is available
    run([PYTHON, '-m', 'pip', 'install', '--user', 'pyinstaller'])
    # build executable
    run([PYTHON, '-m', 'PyInstaller', '--onefile', 'run.py'], cwd=BACKEND_DIR)


def install_frontend():
    if os.path.exists(os.path.join(FRONTEND_DIR, 'package.json')):
        run(['npm', 'install'], cwd=FRONTEND_DIR)


def main():
    install_backend()
    install_frontend()
    print("Build complete. Backend executable is located in backend/dist/.")

if __name__ == '__main__':
    main()
