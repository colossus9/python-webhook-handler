import json
from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/webhook-server', methods=['GET', 'POST'])
def webhookServer():

    # Let's go ahead and make GET requests happy. You could use it to test firewall rules
    if request.method == 'GET':
        return jsonify({'status':'success'}), 200

    # Webhooks will make POST requests
    elif request.method == 'POST':

        # Debugging output
        print '======= DEBUG: BEGIN REQUEST JSON ======='
        print(json.dumps(request.json))
        print '======= DEBUG: END REQUEST JSON ======='

        # Let's get the webhook event so we know what happened
        event = request.headers.get('X-GitHub-Event')

        # Perform actions based on the event that occurred. Events are defined at:
        # https://developer.github.com/v3/activity/events/types/
        #if event == "ping":
        #    return jsonify({'event':'ping','status':'success'}), 200
        #elif event == "repository":
        #    return jsonify({'event':'repository','status':'success'}), 200
        #elif event == "create":
        #    return jsonify({'event':'create','status':'success'}), 200

        try:
            getattr(sys.modules[__name__], str(event))()  # Call the method based on the event type
        except Exception as e:
            errMsg('Problem encountered while running ' + str(event) + '; ' + str(e))

    else:
        abort(400)

def ping():
    return jsonify({'event':'ping','status':'success'}), 200

if __name__ == '__main__':
    app.run(host= '0.0.0.0')  # Run on the machine's IP address and not just localhost
