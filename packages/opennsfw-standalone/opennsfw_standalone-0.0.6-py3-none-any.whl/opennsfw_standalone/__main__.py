import sys

from .inference_runner import OpenNSFWInferenceRunner


def main() -> int:
    """Entrypoint for the CLI, simple demo application."""

    inference_runner = OpenNSFWInferenceRunner.load()

    for image_filename in sys.argv[1:]:
        with open(image_filename, "rb") as fp:
            nsfw_score = inference_runner.infer(fp.read())
            print(image_filename, nsfw_score)

    return 0


if __name__ == "__main__":
    sys.exit(main())
