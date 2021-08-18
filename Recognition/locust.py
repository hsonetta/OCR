from locust import HttpUser, task, between
import base64

class lambdauser(HttpUser):
    wait_time = between(1,5)

    def get_image(self, file_name):
        with open(file_name, 'rb') as f:
            image_bytes = f.read()
        image = base64.b64encode(image_bytes).decode()
        return image

    @task
    def visit_OCR(self):
        # self.client.get(url="/")
        self.client.post("", json={"image": self.get_image('blackonwhite.jpg')})