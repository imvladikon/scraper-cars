from backend import app
import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
