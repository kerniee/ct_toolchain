from os.path import splitext, join

from xml_to_acts.drawio import xml_to_acts


def test_all_xml(xml_filename: str, xml_input_path: str, xml_output_path: str):
    xml_path = join(xml_input_path, xml_filename)
    with open(xml_path, "r", encoding="utf-8") as f:
        xml = f.read()

    acts = xml_to_acts(xml, "Convertor result").strip()

    name, _ = splitext(xml_filename)
    xml_output_path = join(xml_output_path, f"{name}.txt")
    with open(xml_output_path, "r") as f:
        expected = f.read().strip()
    assert expected == acts

