from flask import Flask, jsonify, send_file,request
from flask_cors import CORS

from main import main
app = Flask(__name__)
CORS(app)

transcript =main()



@app.route("/api/data")
def get_data():
   data=transcript
   return jsonify(data)



if __name__ == "__main__":
    app.run(debug=True)


