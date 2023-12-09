import json
import os

import numpy as np
import tritonclient.grpc as grpcclient
from sklearn.metrics.pairwise import cosine_similarity

from libs.face_alignment import align
from libs.logger import Logger


class FaceRecognition:
    def __init__(self, databases) -> None:
        super().__init__()
        self.logger = Logger(
            class_name=os.path.basename(__file__).split(".")[0],
            lvl="INFO",
            file_path="logs",
        ).logger

        self.model_name = "adaface_onnx"
        try:
            self.triton_client = grpcclient.InferenceServerClient(
                url="localhost:8001",
            )
            self.model_info = self.triton_client.get_model_metadata(
                model_name=self.model_name, as_json=True
            )

        except Exception as e:
            self.logger.warning(f"{e}")

        self.logger.info(
            f"\n face\n{self.model_name}\n{json.dumps(self.model_info, indent=4, sort_keys=True)}"
        )
        self.inputs = [
            grpcclient.InferInput(
                input["name"],
                tuple(map(int, input["shape"])),
                input["datatype"],
            )
            for input in self.model_info["inputs"]
        ]
        self.outputs = [
            grpcclient.InferRequestedOutput(output["name"])
            for output in self.model_info["outputs"]
        ]

        self.db = databases

    def _preprocessing(self, frame: [str, np.array]):
        aligned_rgb_img = align.get_aligned_face(frame)
        if aligned_rgb_img is not None:
            np_img = np.array(aligned_rgb_img)
            brg_img = ((np_img[:, :, ::-1] / 255.0) - 0.5) / 0.5
            output = np.expand_dims(
                brg_img.transpose(2, 0, 1),
                axis=0,
            ).astype(np.float32)

            return output
        else:
            return None

    def predict(self, raw: [str, np.array]):
        inputs = self._preprocessing(frame=raw)
        if inputs is not None:
            self.inputs[0].set_data_from_numpy(inputs)

            res = self.triton_client.infer(
                model_name=self.model_name,
                inputs=self.inputs,
            )

            _outputs = res.as_numpy(self.model_info["outputs"][0]["name"])[0]
            return list(_outputs)
        else:
            return None

    def registration(
        self,
        collection: str,
        name: str,
        frame: [str, np.array],
    ):
        embs = self.predict(raw=frame)
        if embs is not None:
            self.db.registration(
                collection=collection,
                name=name,
                embs=f"{embs}",
            )

    def compare(self, collection: str, target: [str, np.array]):
        names, embs = self.db.finder(ce_name=collection)
        target_emb = self.predict(raw=target)
        target_embs = [target_emb for i in range(len(embs))]

        similarity_scores = cosine_similarity(
            embs,
            target_embs,
        ).T[0]

        same_face_idx = np.argmax(similarity_scores)
        same_face_score = np.max(similarity_scores)
        same_face_emb = embs[same_face_idx]
        same_face_name = names[same_face_idx]
        return (
            same_face_idx,
            same_face_emb,
            same_face_score,
            same_face_name,
        )
