import json, os, requests, sys
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

        print ' '

        # Let's get the webhook event so we know what happened
        #print 'Getting webhook event...'
        EVENT = request.headers.get('X-GitHub-Event')
        print '----------> Received event: ' + EVENT
        #print '  ' + EVENT
        #print ' '

        # Getting the source hostname
        #print 'Getting hostname...'
        GHE_URL = urlparse(json.loads(request.data)['organization']['url'])
        GHE_HOST = GHE_URL.hostname
        #print '  ' + GHE_HOST
        #print ' '

        # Grab the credential for the source GitHub Enterprise server
        #print 'Getting credential...'
        if os.path.isfile(credFile):
            creds = json.load(open(credFile))
            for server in creds["servers"]:
                if server["url"] == GHE_HOST:
                    TOKEN = server["token"]
                    break

            # No token was found
            if TOKEN == None:
                print 'No token found in ' + credFile + ', so we are unable execute actions against GitHub Enterprise.'

            # A valid GitHub Enterprise token was found
            else:
                #print 'Token is ' + TOKEN

                # Perform actions based on the event that occurred. Events are defined at:
                # https://developer.github.com/v3/activity/events/types/
                if EVENT == "ping":
                    debugPrintWebhookJSON(request.json)
                    return jsonify({'event':'ping','status':'success'}), 200

                elif EVENT == "repository":
                    event_action = request.json["action"]
                    print 'Event Action: ' + event_action

                    # Perform this API call when a repository is created
                    if event_action == "created":
                        debugPrintWebhookJSON(request.json)
                        orgRepo = request.json["repository"]["full_name"]
                        api_url = 'https://HOSTNAME/api/v3/teams/ID/repos/' + orgRepo
                        headers = {'Accept':'application/vnd.github.v3+json','Authorization':'token ' + TOKEN}
                        params = {'permission':'admin'}
                        r = requests.put(api_url, data=None, headers=headers, params=params, verify=False)  # Let's add a team to the repo. Only set verify=False on a test instance
                        print r
                        return jsonify({'event':'repository','status':'success'}), 200

                elif EVENT == "create":
                    print 'Event Action: ' + request.json["action"]
                    debugPrintWebhookJSON(request.json)
                    return jsonify({'event':'create','status':'success'}), 200

                elif EVENT == "organization":
                    print 'Event Action: ' + request.json["action"]
                    return jsonify({'event':'organization','status':'success'}), 200

                elif EVENT == "label":
                    print 'Event Action: ' + request.json["action"]
                    return jsonify({'event':'label','status':'success'}), 200

                elif EVENT == "push":
                    print 'Event Action: ' + request.json["action"]
                    return jsonify({'event':'push','status':'success'}), 200

                else:
                    return jsonify({'event':'other','status':'success'}), 200

        else:
            print 'Error: The file ' + credFile + ' does not exist.'
            abort(400)

    else:
        abort(400)

def debugPrintWebhookJSON(data):

    # Debug output
    print ' '
    print '======= DEBUG: BEGIN REQUEST JSON ======='
    print(json.dumps(data))
    print '======= DEBUG: END REQUEST JSON ======='
    print ' '

if __name__ == '__main__':
    app.run(host= '0.0.0.0')  # Run on the machine's IP address and not just localhost
