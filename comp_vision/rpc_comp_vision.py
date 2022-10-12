import os
from base64 import b64encode
from xmlrpclib import ServerProxy


def encode_to_string(content_stream):
    return b64encode(content_stream.read()).decode('ascii')


class GodPythonFuckingSucksHolyShit:
    def __init__(self, dict):
        for key, value in dict.items():
            setattr(self, key, objectify(value))

    def __repr__(self):
        return repr(self.__dict__)


def objectify(obj):
    t = type(obj)
    if t == list:
        return [objectify(x) for x in obj]
    elif t == dict:
        return GodPythonFuckingSucksHolyShit(obj)

    return obj


def parents(obj):
    p = obj.parent
    while p:
        yield p.object_property
        p = p.parent


def print_objects(objects):
    if not objects:
        print("No objects detected.")
    else:
        for obj in objects:
            name = obj.object_property
            if obj.parent:
                name += ' (< ' + ' < '.join(parents(obj)) + ')'
            confidence = obj.confidence
            x1, x2 = obj.rectangle.x, obj.rectangle.x + obj.rectangle.w
            y1, y2 = obj.rectangle.y, obj.rectangle.y + obj.rectangle.h

            print("{} at location {} {} ".format(name, x1, x2) +
                  "{} {} with confidence {}".format(y1, y2, confidence))


def detect_objects(image_path_or_fl, rpc_url):
    if isinstance(image_path_or_fl, str):
        with open(image_path, 'rb') as image_stream:
            image_content_b64 = encode_to_string(image_stream)
    else:
        image_content_b64 = encode_to_string(image_path_or_fl)

    proxy = ServerProxy(rpc_url, allow_none=True)
    objects_as_dicts = proxy.detect_objects(image_content_b64)
    return objectify(objects_as_dicts)


if __name__ == '__main__':
    images_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
    image_path = os.path.join(images_folder, "clock.jpg")

    vm_host_ip = '10.0.2.2'
    objects = detect_objects(image_path, "http://" + vm_host_ip + ":42069/")
    print_objects(objects)
    print repr(objects)
