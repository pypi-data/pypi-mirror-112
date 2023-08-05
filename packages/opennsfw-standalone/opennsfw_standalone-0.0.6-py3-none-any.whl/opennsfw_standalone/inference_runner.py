from io import BytesIO

import numpy as np
import onnxruntime
import pkg_resources

from PIL import Image


class OpenNSFWInferenceRunner:
    """Performs inference against Yahoo"s OpenNSFW model."""

    def __init__(self, model) -> None:
        self._model = model

    @classmethod
    def load(
        cls,
        model_path: str = pkg_resources.resource_filename(__name__, "open-nsfw.onnx"),
    ):
        """Initialzies the classifier by loading the model from disk and
        preparing it for inference."""

        model = onnxruntime.InferenceSession(model_path)
        return cls(model)

    def infer(self, image_data: bytes) -> float:
        """Classifies the the specified image.

        Arguments:
            image_data:
                JPEG/PNG/BMP/WEBP data to classify.

        Returns:
            A score indicating how likely it is that
            this model contains NSFW content.
        """

        image = self._preprocess_image(image_data)

        input_name = self._model.get_inputs()[0].name
        outputs = [output.name for output in self._model.get_outputs()]

        result = self._model.run(outputs, {input_name: image})
        return result[0][0][1]

    @staticmethod
    def _preprocess_image(image_data: bytes) -> np.array:
        """Loads and and pre-processes the specified image for the model.

        Approximation of: https://github.com/yahoo/open_nsfw/blob/a4e13931465f4380742545932657eeea0a10aa48/classify_nsfw.py#L40
        """

        image = Image.open(BytesIO(image_data))
        if image.mode != "RGB":
            image = image.convert("RGB")

        image = image.resize((256, 256), resample=Image.BILINEAR)

        cropped_size = 224
        image_width, image_height = image.size
        image = image.crop(
            (
                (image_width - cropped_size) / 2,
                (image_height - cropped_size) / 2,
                (image_width + cropped_size) / 2,
                (image_height + cropped_size) / 2,
            )
        )

        # Save as JPEG into a buffer, convert it to a
        # numpy array so we can do some more manipulation
        with BytesIO() as jpeg_buffer:
            image.save(jpeg_buffer, format="JPEG")
            jpeg_buffer.seek(0)

            image_jpeg_data = np.array(Image.open(jpeg_buffer), dtype=np.float32, copy=False)

        # Convert from RGB to BGR
        # See: https://github.com/yahoo/open_nsfw/blob/a4e13931465f4380742545932657eeea0a10aa48/classify_nsfw.py#L116
        image_jpeg_data = image_jpeg_data[:, :, ::-1]

        # Subtract dataset-mean in each channel
        # See: https://github.com/yahoo/open_nsfw/blob/a4e13931465f4380742545932657eeea0a10aa48/classify_nsfw.py#L114
        image_jpeg_data -= np.array([104, 117, 123], dtype=np.float32)

        # Move image channels to outermost
        # See: https://github.com/yahoo/open_nsfw/blob/a4e13931465f4380742545932657eeea0a10aa48/classify_nsfw.py#L113
        image_jpeg_data = np.expand_dims(image_jpeg_data, axis=0)

        return image_jpeg_data
