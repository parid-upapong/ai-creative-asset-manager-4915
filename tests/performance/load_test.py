from locust import HttpUser, task, between
import uuid

class CreatorNexusUser(HttpUser):
    wait_time = between(1, 5)

    @task(3)
    def view_dashboard(self):
        self.client.get("/api/v1/dashboard/stats")

    @task(1)
    def simulate_asset_ingestion(self):
        """
        Simulates the heavy lifting: requesting upload slots for multiple assets.
        This tests the API's ability to handle high-frequency DB writes and S3 signing.
        """
        asset_id = str(uuid.uuid4())
        payload = {
            "filename": f"batch_upload_{asset_id}.jpg",
            "file_type": "image",
            "size_bytes": 5000000
        }
        self.client.post("/api/v1/assets/upload-init", json=payload)

    @task(2)
    def poll_ai_status(self):
        # Simulating the frontend polling for AI completion
        self.client.get("/api/v1/assets/recent/status")