from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

logs = []  # Store the logs here

@app.route('/')
def index():
    return render_template('index.html', logs=logs)  # Passing logs to the template


@app.route('/update_logs', methods=['POST'])
def update_logs():
    global logs
    if request.method == 'POST':
        data = request.json
        logs.append(data["logs"])  # Expecting logs as a list [name, timestamp]
        return jsonify({"status": "success", "logs": logs})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    app.run(host='0.0.0.0', port=port)
