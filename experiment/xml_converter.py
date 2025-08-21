import io
from pathlib import Path
from typing import Any

import xmlschema
from lxml import etree  # type: ignore[import-untyped]
from xsdata_pydantic.bindings import XmlParser, XmlSerializer, DictDecoder, DictEncoder

from experiment.models.example_schema import ExampleFile


class XMLConverter:
    def __init__(self, xsd_path: str | Path):
        self.xsd_path = Path(xsd_path)
        self.schema = xmlschema.XMLSchema11(str(self.xsd_path))
        self.parser = XmlParser()
        self.serializer = XmlSerializer()

    def xml_to_pydantic(self, xml_string: str) -> ExampleFile:
        return self.parser.parse(io.BytesIO(xml_string.encode()), ExampleFile)

    def pydantic_to_json(self, model: ExampleFile) -> dict[str, Any]:
        dict_encoder = DictEncoder()
        return dict_encoder.encode(model)

    def json_to_pydantic(self, json_data: dict[str, Any]) -> ExampleFile:
        decoder = DictDecoder()
        document = decoder.decode(json_data, ExampleFile)
        return document


    def pydantic_to_xml(self, model: ExampleFile) -> str:
        return self.serializer.render(model)

    def validate_xml_string(self, xml_string: str) -> bool:
        try:
            self.schema.validate(xml_string)
            return True
        except xmlschema.XMLSchemaException:
            raise
            return False

    def normalize_xml_string(self, xml_string: str) -> str:
        parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
        xml_root = etree.XML(xml_string.encode(), parser)
        return str(etree.tostring(xml_root, method="c14n2").decode("utf8"))

    def pretty_print_xml_string(self, xml_string: str) -> str:
        parser = etree.XMLParser()
        xml_root = etree.XML(xml_string.encode(), parser)
        return str(etree.tostring(xml_root, pretty_print=True).decode("utf8"))



