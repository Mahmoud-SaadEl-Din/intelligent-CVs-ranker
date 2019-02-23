import readingDOCX as reader
import data_optimization as optimizer
import JSON_creation as JSON_creator

reader.scan_docx('Mahmoud Saad.docx')
optimizer.optimize_this_data(reader.get_heading_internal_data())
JSON_creator.set_JSON_title(reader.get_heading_list())
JSON_creator.set_JSON_bodies(reader.get_heading_internal_data())
JSON_creator.build_JSON_parts()
JSON_creator.finalize_JSON()
print(JSON_creator.json.dumps(JSON_creator.JSON_object, indent=4, sort_keys=True))
