import base64
import numpy as np
import cv2


def base64_to_numpy(image_base64):
    image_bytes = base64.b64decode(image_base64)
    image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    image_np2 = (cv2.imdecode(image_np, cv2.IMREAD_COLOR))
    # image_np2 = cv2.cvtColor(image_np2, cv2.COLOR_BGR2RGB)
    image_np2 = image_np2 / 255
    return image_np2.astype(np.float32)


def numpy_to_base64(image, unnormalize: bool):
    if unnormalize:
        image = image / 2 + 0.5  # unnormalize
    if image.dtype in (np.float32, np.double) and image.max() <= 1:
        image = (image * 255).astype('uint8')
    retval, buffer = cv2.imencode('.jpg', image)
    pic_str = base64.b64encode(buffer)
    return pic_str.decode()


def numpy_to_tensor(image_np, normalize=True):
    if normalize:
        image_np = (image_np - 0.5) * 2
    return np.transpose(image_np, (2, 0, 1))[None, ...]


def tensor_to_base64(image_tensor, unnormalize=True):
    import torch
    if image_tensor.dtype == torch.float:
        image_tensor = np.array(image_tensor.cpu())
    b64_list = [numpy_to_base64(np.transpose(image, (1, 2, 0)), unnormalize) for image in image_tensor]
    return b64_list


def base64_list_to_tensor(b64_list, normalize=True):
    tensor_list = [numpy_to_tensor(base64_to_numpy(b64), normalize) for b64 in b64_list]
    return np.concatenate(tensor_list, 0)
