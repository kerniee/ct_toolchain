import pytest
from os import listdir
from os.path import isfile, join


XML_INPUT_PATH = "tests/xml"
XML_OUTPUT_PATH = "tests/expected"


@pytest.fixture
def xml_input_path():
    return XML_INPUT_PATH


@pytest.fixture
def xml_output_path():
    return XML_OUTPUT_PATH


def pytest_generate_tests(metafunc: pytest.Metafunc):
    XML_FILENAME_FIXTURE = "xml_filename"
    if XML_FILENAME_FIXTURE in metafunc.fixturenames:
        paths = []
        for filename in listdir(XML_INPUT_PATH):
            filepath = join(XML_INPUT_PATH, filename)
            if not isfile(filepath):
                continue
            paths.append(filename)
        metafunc.parametrize(XML_FILENAME_FIXTURE, paths)
