from flask import Flask, request, abort

app = Flask(__name__)


@app.route('/webhook-server', methods=['GET', 'POST'])
def webhookServer():
    if request.method == 'GET':
        return jsonify({'status':'success'}), 200

    elif request.method == 'POST':
        print ' '
        print(request.json)
        print ' '

        return '', 200

    else:
        abort(400)


if __name__ == '__main__':
    app.run(host= '0.0.0.0')  # Run on the machine's IP address and not just localhost
