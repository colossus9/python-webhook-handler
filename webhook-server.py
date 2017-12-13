import json, sys
from flask import Flask, request, abort, jsonify

app = Flask(__name__)

@app.route('/webhook-server', methods=['GET', 'POST'])
def webhookServer():

    # Let's go ahead and make GET requests happy. You could use it to test firewall rules
    if request.method == 'GET':
        return jsonify({'method':'GET','status':'success'}), 200

    # Webhooks will make POST requests
    elif request.method == 'POST':

        # Debugging output
        print ' '
        print '======= DEBUG: ENVIRONMENT ======='
        print 'GHE_ADDRESS=' + json.loads(request.data)['hook']['url']
        print '======= DEBUG: BEGIN REQUEST JSON ======='
        print(json.dumps(request.json))
        print '======= DEBUG: END REQUEST JSON ======='
        print ' '

        # Let's get the webhook event so we know what happened
        event = request.headers.get('X-GitHub-Event')
        creds = json.load(open('/tmp/creds.json'))
        print creds["servers"][0]["token"]

        # Perform actions based on the event that occurred. Events are defined at:
        # https://developer.github.com/v3/activity/events/types/
        if event == "ping":
            return jsonify({'event':'ping','status':'success'}), 200

        elif event == "repository":
            return jsonify({'event':'repository','status':'success'}), 200

        elif event == "create":
            return jsonify({'event':'create','status':'success'}), 200

    else:
        abort(400)

if __name__ == '__main__':
    app.run(host= '0.0.0.0')  # Run on the machine's IP address and not just localhost
