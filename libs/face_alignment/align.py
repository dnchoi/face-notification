from PIL import Image

from libs.face_alignment import mtcnn

mtcnn_model = mtcnn.MTCNN(device="cuda:0", crop_size=(112, 112))


def add_padding(pil_img, top, right, bottom, left, color=(0, 0, 0)):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result


def get_aligned_face(img):
    if type(img) == str:
        img = Image.open(img).convert("RGB")

    try:
        bboxes, faces = mtcnn_model.align_multi(img, limit=1)
        face = faces[0]
    except Exception as e:
        print("Face detection Failed due to error.")
        print(e)
        face = None

    return face
