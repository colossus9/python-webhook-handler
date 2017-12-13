import json, sys
from flask import Flask, request, abort, jsonify

app = Flask(__name__)

@app.route('/webhook-server', methods=['GET', 'POST'])
def webhookServer():

    # Define vars
    GHE_ADDRESS = os.environ.get('GHE_ADDRESS', None)  # The address of the GitHub Enterprise server

    # Let's go ahead and make GET requests happy. You could use it to test firewall rules
    if request.method == 'GET':
        return jsonify({'method':'GET','status':'success'}), 200

    # Webhooks will make POST requests
    elif request.method == 'POST':

        # Debugging output
        print ' '
        print '======= DEBUG: ENVIRONMENT ======='
        print 'url=' + request.url
        print 'base_url=' + request.base_url
        print 'url_root=' + request.url_root
        print 'data=' + request.data
        print 'headers=' + json.dumps(request.url)
        print '======= DEBUG: BEGIN REQUEST JSON ======='
        print(json.dumps(request.json))
        print '======= DEBUG: END REQUEST JSON ======='
        print ' '

        # Let's get the webhook event so we know what happened
        event = request.headers.get('X-GitHub-Event')

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
