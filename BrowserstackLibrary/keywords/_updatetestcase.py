import json

class _UpdateTestCase:
    def __init__(self, client):
        self.client = client

    def update_status(self, session_id, status, reason):
        print(status)

        if status == 'FAIL':
            payload = json.dumps({
                "status": "failed",
                "reason": reason
            })
        else:
            payload = json.dumps({
                "status": "passed",
                "reason": "Test Passed"
            })

        print(payload)

        return self.client.browserstack_request(f"/sessions/{session_id}.json", "PUT", payload)