import DocxReader as reader


reader.scan_docx('cv.docx')
print(reader.get_sentence_list())
