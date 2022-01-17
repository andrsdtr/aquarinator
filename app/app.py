from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def base_control():
    return render_template("base_control.html")

@app.route('/advanced')
def advanced():
    return render_template("advanced.html")


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')