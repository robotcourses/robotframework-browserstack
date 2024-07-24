class _UploadApplication:
    def __init__(self, client):
        self.client = client

    def upload_app_file(self, app_name, app_path, custom_id):
        data = {'custom_id': custom_id}
        files = {'file': (app_name, open(app_path, 'rb'), 'application/octet-stream')}
        return self.client.browserstack_request("/upload", "POST", data=data, files=files)

    def upload_public_url(self, download_url, custom_id):
        data = {'url': download_url, 'custom_id': custom_id}
        return self.client.browserstack_request("/upload", "POST", data=data)

    def get_list_app(self, custom_id):
        return self.client.browserstack_request(f"/recent_apps/{custom_id}", "GET")