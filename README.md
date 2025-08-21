# xsdata-experiments

This project contains several XML files that have given problems with xsdata.
The xsd file is based on a real-world XSD file, but has been simplified to the minimum that still reproduces the problem.

It tries to read an xml file, convert it to a pydantic model, convert it to a python dict, and then back to an pydantic model and finally back to an xml string.
The final xml string is expected to be the same as the original xml string and the same with the pydantic models obtained from the original xml and the python dict.
The files in the `out` folder are the final xml strings.

`uv` is required to run the project: `uv run experiment/main.py`

To regenerate the models use `make generate`

I have found the following 4 problems:

- Trying to define an extension of type class to create a mixin doesn't work as expected because if the class inherits BaseModel directly there is no way to put the mixin at the beginning of the base list.

- `similar_types_sequence_error.xml`: If there are several optional elements of the same type in a sequence they will get wrong types

- `xs_all_ordering_error.xml`: Elements inside `xs:all` doesn't respect the order in which they are defined in the original XML.

- `similar_types_choice_error.xml`: Running the project several times will eventually raise an error

```
Processing: similar_types_choice_error.xml
--------------------------------------------------
Traceback (most recent call last):
  File "/Users/pedro.almirall/work/xsdata-experiments/experiment/main.py", line 61, in <module>
    main()
  File "/Users/pedro.almirall/work/xsdata-experiments/experiment/main.py", line 43, in main
    converter.validate_xml_string(reconstructed_xml_string)
  File "/Users/pedro.almirall/work/xsdata-experiments/experiment/xml_converter.py", line 37, in validate_xml_string
    self.schema.validate(xml_string)
  File "/Users/pedro.almirall/work/xsdata-experiments/.venv/lib/python3.12/site-packages/xmlschema/validators/schemas.py", line 1335, in validate
    for error in self.iter_errors(source, path, schema_path, use_defaults,
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/pedro.almirall/work/xsdata-experiments/.venv/lib/python3.12/site-packages/xmlschema/validators/schemas.py", line 1458, in iter_errors
    xsd_element.raw_decode(elem, validation, context)
  File "/Users/pedro.almirall/work/xsdata-experiments/.venv/lib/python3.12/site-packages/xmlschema/validators/elements.py", line 746, in raw_decode
    content = content_decoder.raw_decode(obj, validation, context)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/pedro.almirall/work/xsdata-experiments/.venv/lib/python3.12/site-packages/xmlschema/validators/groups.py", line 1036, in raw_decode
    result_item = xsd_element.raw_decode(child, validation, context)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/pedro.almirall/work/xsdata-experiments/.venv/lib/python3.12/site-packages/xmlschema/validators/elements.py", line 746, in raw_decode
    content = content_decoder.raw_decode(obj, validation, context)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/pedro.almirall/work/xsdata-experiments/.venv/lib/python3.12/site-packages/xmlschema/validators/groups.py", line 1005, in raw_decode
    self.check_dynamic_context(child, xsd_element, model.element, namespaces)
  File "/Users/pedro.almirall/work/xsdata-experiments/.venv/lib/python3.12/site-packages/xmlschema/validators/groups.py", line 878, in check_dynamic_context
    xsd_type = self.maps.get_instance_type(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/pedro.almirall/work/xsdata-experiments/.venv/lib/python3.12/site-packages/xmlschema/validators/xsd_globals.py", line 241, in get_instance_type
    xsi_type = self.types[extended_name]
               ~~~~~~~~~~^^^^^^^^^^^^^^^
  File "/Users/pedro.almirall/work/xsdata-experiments/.venv/lib/python3.12/site-packages/xmlschema/validators/builders.py", line 394, in __getitem__
    raise XMLSchemaKeyError(msg) from None
xmlschema.exceptions.XMLSchemaKeyError: "global component 'WorkAddress' not found"
```
