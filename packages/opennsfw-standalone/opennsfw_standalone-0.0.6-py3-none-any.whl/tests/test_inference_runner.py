import pytest

from opennsfw_standalone import OpenNSFWInferenceRunner


@pytest.fixture(scope='session')
def inference_runner():
    return OpenNSFWInferenceRunner.load()


@pytest.mark.parametrize('image_path,nsfw_score', [
    ('./tests/data/sexy-1.jpg', 0.8291498),
    ('./tests/data/sexy-2.jpg', 0.3111369),
    ('./tests/data/sexy-3.jpg', 0.34722114),
    ('./tests/data/nude-1.jpg', 0.9987545),
    ('./tests/data/porn-1.jpg', 0.99944717),
    ('./tests/data/porn-2.jpg', 0.93480694),
    ('./tests/data/porn-3.jpg', 0.8638213),
    ('./tests/data/porn-4.jpg', 0.7389689),
    ('./tests/data/penis-1.jpg', 0.982685),
    ('./tests/data/penis-2.jpg', 0.9972377),
    ('./tests/data/car-1.jpg', 0.00019015299),
    ('./tests/data/car-2.jpg', 0.036598504),
    ('./tests/data/house-1.jpg', 0.0019087311),
    ('./tests/data/house-2.jpg', 0.08629423),
    ('./tests/data/phone-1.jpg', 0.00019739063),
    ('./tests/data/headphones-1.jpg', 0.0010423164),
    ('./tests/data/person-1.jpg', 0.00064663886),
])
def test_inference_runner(image_path, nsfw_score, inference_runner):
    with open(image_path, 'rb') as fp:
        assert inference_runner.infer(fp.read()) == pytest.approx(nsfw_score, rel=1e-3)
