# run.py
import os
from dotenv import load_dotenv

# explicitly point to .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

from app.__init__ import create_app


print("Hello World! (Remove later just to test if we can get anything to print)")
app = create_app()
print("App Created")

if __name__ == '__main__':
    app.run(debug=True)

