import DocxReader as reader


reader.scan_docx('Resume.docx')
print(reader.get_sentence_list())
