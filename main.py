import readingDOCX as reader
import data_optimization as optimizer
import JSON_creation as JSON_creator

reader.scan_docx('Mahmoud Saad.docx')
lists = reader.get_heading_internal_data()
print(lists)
print(reader.get_scanning_time())