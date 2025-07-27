from flask import Flask
import json

app = Flask(__name__)


@app.route('/api')
def api_req():
    with open("data_file.json", "r") as fp:
        data_dict = json.load(fp)
        return data_dict


if __name__ == "__main__":
    app.run(debug=True)
