# python-webhook-handler

Handle a GitHub Enterprise Webhook payload with Flask. It retrieves the source GitHub Enterprise hostname and uses the credential in `/tmp/creds.json`. The idea is to use a single, simple webhook receiver for multiple instances of GitHub (Enterprise). 

**Reference:** [Simple Flask Webhook](https://ogma-dev.github.io/posts/simple-flask-webhook/)

## Install Instructions

1. Install `python` and `pip`:

    ```
    sudo yum install python27 python-pip -y
    ```

1. Clone the repository and navigate to the workspace:

    ```
    git clone https://github.com/colossus9/python-webhook-handler.git
    cd python-webhook-handler
    ```

1. Install the requirements:

    ```
    pip install -r requirements.txt
    ```

1. Create a `/tmp/creds.json` file of the following format. Note: The tokens must have the `admin:org` scope:

    ```
    {
        "servers": [
            {
              "url":"GHE_SERVER_1",
              "token":"XXXXXXX"
            },
            {
              "url":"GHE_SERVER_2",
              "token":"YYYYYYY"
            },
            {
              "url":"GHE_SERVER_3",
              "token":"ZZZZZZZ"
            }
        ]
    }
    ```

1. Run the server:

    ```
    python webhook-server.py
    ```
