import boto, time
from boto.s3.key import Key
from boto.s3.lifecycle import Lifecycle, Expiration

FILE_PREFIX='s3iu.'
EXPIRATION=5 # days

def generate_image_name():
    return FILE_PREFIX + str(10000000000 - int(time.time())) + '.jpg'

def upload(bucket_name, image_name, image):
    conn = boto.connect_s3()
    bucket = conn.get_bucket(bucket_name)

    lifecycle = Lifecycle()
    lifecycle.add_rule('s3-image-uploader', prefix=FILE_PREFIX, status='Enabled', expiration=Expiration(days=EXPIRATION))
    bucket.configure_lifecycle(lifecycle)

    k = Key(bucket)
    k.key = image_name
    k.set_contents_from_string(image)
