from abc import ABC, abstractmethod

import albumentations as A
import cv2
import numpy as np
import onnxruntime
import torch
from albumentations.pytorch import ToTensorV2

onnxruntime.set_default_logger_severity(3)


class AbstractImageAnalazer(ABC):
    @abstractmethod
    def analyse_image(self, image: cv2.typing.MatLike) -> bool:
        ...


class SimpleImageAnalazer(AbstractImageAnalazer):
    is_camera_clear_model_runtime = onnxruntime.InferenceSession("/opt/app/cctv/utils/models/efficientnetb1_256x256-imagenetnorm-0907_current.onnx")
    artifacts_classification_model_runtime = onnxruntime.InferenceSession("/opt/app/cctv/utils/models/efficientnetb1-imagenetweight-350x350-0.88-type.onnx")
    first_model_transform = A.Compose([
        A.Resize(256, 256),
        A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
        ToTensorV2(),
    ])
    second_model_transform = A.Compose([
        A.Resize(350, 350),
        A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
        ToTensorV2(),
    ])

    @classmethod
    def analyse_image(cls, image: cv2.typing.MatLike) -> bool:
        im_tensor = cls._apply_transformations(image, cls.first_model_transform)

        input_name = cls.is_camera_clear_model_runtime.get_inputs()[0].name
        output_name = cls.is_camera_clear_model_runtime.get_outputs()[0].name
        predict = cls.is_camera_clear_model_runtime.run([output_name], {input_name: np.array(im_tensor)})[0]

        # predict_list_label = np.argmax(predict, axis=1)
        predict = torch.sigmoid(torch.tensor(predict))
        predict_label = (predict > 0.5).int()
        predict_label = predict_label.item()

        if predict_label == 0:
            return predict_label

        im_tensor = cls._apply_transformations(image, cls.second_model_transform)
        input_name = cls.artifacts_classification_model_runtime.get_inputs()[0].name
        output_name = cls.artifacts_classification_model_runtime.get_outputs()[0].name
        predict = cls.artifacts_classification_model_runtime.run([output_name], {input_name: np.array(im_tensor)})[0]

        predict = torch.sigmoid(torch.tensor(predict))
        predict_label = (predict > 0.5).int()
        predict_label = predict_label.item()

        return predict_label + 1

    # @staticmethod
    # def _to_numpy(tensor):
    #    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()

    @classmethod
    def _apply_transformations(cls, image, transform):
        tensor_image = transform(image=image)['image']
        batch_tensor = np.expand_dims(tensor_image, 0)
        return batch_tensor
