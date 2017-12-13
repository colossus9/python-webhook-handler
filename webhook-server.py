import json, os, sys
from flask import Flask, request, abort, jsonify
from urlparse import urlparse

app = Flask(__name__)
credFile = str('/tmp/creds.json')

@app.route('/webhook-server', methods=['GET', 'POST'])
def webhookServer():

    # Define some vars
    EVENT = None
    GHE_URL = None
    GHE_HOST = None
    TOKEN = None

    # Let's go ahead and make GET requests happy. You could use it to test firewall rules
    if request.method == 'GET':
        return jsonify({'method':'GET','status':'success'}), 200

    # Webhooks will make POST requests
    elif request.method == 'POST':

        # Debugging output
        print ' '
        print '======= DEBUG: BEGIN REQUEST JSON ======='
        print(json.dumps(request.json))
        print '======= DEBUG: END REQUEST JSON ======='
        print ' '

        # Let's get the webhook event so we know what happened
        print 'Getting webhook event...'
        EVENT = request.headers.get('X-GitHub-Event')
        print '  ' + EVENT
        print ' '

        # Getting the source hostname
        print 'Getting hostname...'
        GHE_URL = urlparse(json.loads(request.data)['hook']['url'])
        GHE_HOST = GHE_URL.hostname
        print '  ' + GHE_HOST
        print ' '

        # Grab the credential for the source GitHub Enterprise server
        print 'Getting credential...'

        if os.path.isfile(credFile):
            creds = json.load(open(credFile))
            for server in creds["servers"]:
                #for key, value in creds["servers"][0].iteritems():
                if server.url == GHE_HOST:
                    TOKEN = value

            if TOKEN == None:
                print 'WARN: Credential not found in ' + credFile + '. Unable to authenticate to API endpoint.'

            else:
                print TOKEN


            #print creds["servers"][0]["token"]

        else:
            print 'Error: The file ' + credFile + ' does not exist.'
            abort(400)

        # Perform actions based on the event that occurred. Events are defined at:
        # https://developer.github.com/v3/activity/events/types/
        if EVENT == "ping":
            return jsonify({'event':'ping','status':'success'}), 200

        elif EVENT == "repository":
            return jsonify({'event':'repository','status':'success'}), 200

        elif EVENT == "create":
            return jsonify({'event':'create','status':'success'}), 200

        else:
            return jsonify({'event':'other','status':'success'}), 200

    else:
        abort(400)

if __name__ == '__main__':
    app.run(host= '0.0.0.0')  # Run on the machine's IP address and not just localhost
