#!/usr/bin/env python3

from pathlib import Path

from experiment.xml_converter import XMLConverter


def main():
    # Paths
    schema_path = Path("experiment/schemas/example_schema.xsd")
    examples_dir = Path("experiment/examples")
    out_dir = Path("experiment/out/")

    # Process all XML example files
    xml_files = list(examples_dir.glob("*.xml"))

    for xml_file in xml_files:
        print(f"\nProcessing: {xml_file.name}")
        print("-" * 50)

        converter = XMLConverter(schema_path)

        xml_file_content = xml_file.read_text()

        # Preliminary validation
        converter.validate_xml_string(xml_file_content)

        # Convert XML through the pipeline

        # Step 1: XML file to Pydantic model
        model_from_file = converter.xml_to_pydantic(xml_file_content)

        # Step 2: Pydantic model to JSON
        json_data_from_file = converter.pydantic_to_json(model_from_file)

        # Step 3: JSON to Pydantic model
        reconstructed_model = converter.json_to_pydantic(json_data_from_file)

        # Step 4: Pydantic model to XML string
        reconstructed_xml_string = converter.pydantic_to_xml(reconstructed_model)

        # Final validation
        converter.validate_xml_string(reconstructed_xml_string)

        normalized_original = converter.normalize_xml_string(xml_file_content)
        normalized_reconstructed = converter.normalize_xml_string(
            reconstructed_xml_string
        )

        print(f"Models are equal: {model_from_file == reconstructed_model}")
        print(f"XML strings are equal: {normalized_original == normalized_reconstructed}")

        out_file = out_dir / xml_file.name
        out_file.write_text(converter.pretty_print_xml_string(reconstructed_xml_string))

        # __import__('ipdb').set_trace()
        pass


if __name__ == "__main__":
    main()
