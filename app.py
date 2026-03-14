import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from myapp import create_app

app = create_app(config_name='development')

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=5000, debug=True)
