from locust import HttpUser, TaskSet, task, between
import random, uuid, time, io, requests, urllib, os

COLOR_IMAGES = [
    'https://raw.githubusercontent.com/woomurf/ainize-color-transfer/master/images/autumn.jpg',
    'https://raw.githubusercontent.com/woomurf/ainize-color-transfer/master/images/fallingwater.jpg',
    'https://raw.githubusercontent.com/woomurf/ainize-color-transfer/master/images/ocean_day.jpg',
]

BASE_IMAGES = [
    'https://raw.githubusercontent.com/woomurf/ainize-color-transfer/master/images/ocean_sunset.jpg',
    'https://raw.githubusercontent.com/woomurf/ainize-color-transfer/master/images/storm.jpg',
    'https://raw.githubusercontent.com/woomurf/ainize-color-transfer/master/images/woods.jpg'
]
def getFilenameFromURL(url):
    parsedUrl = urllib.parse.urlparse(url)
    return os.path.basename(parsedUrl.path)

def fileopen(image):
    fetched = requests.get(image)
    f_image = (
        getFilenameFromURL(image),
        io.BytesIO(fetched.content),
        fetched.headers.get("Content-Type", "image/jpeg"),
    )
    return f_image

class UserBehavior(TaskSet):

    @task(1)
    def transfer(self):
        req_id = str(uuid.uuid4())      
        color_image = random.choice(COLOR_IMAGES)
        base_image = random.choice(BASE_IMAGES)

        color_source_payload = fileopen(color_image)
        base_payload = fileopen(base_image)

        start = time.time()
        response = self.client.post(
            "/transfer", 
            files={
                'color_source': color_source_payload,
                'base': base_payload
            }
        )
        duration = time.time() - start

        print(
                (
                    "out",
                    req_id,
                    duration,
                    response.status_code,
                    len(response.content),
                )
            )

TARGET_RPS = 1

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]

    def wait_time(self):
        target_wait = between(0, 2 / TARGET_RPS)(self)  
        print(("wait", target_wait))
        return target_wait