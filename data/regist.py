import docx

doc = docx.Document('./data/persons.docx')

table = doc.tables[0]

full_names = []

for row in table.rows:
    text: str
    text = row.cells[1].text
    if text is not None or ' ' or '':
        if text.split()[-1] != 'округ':
            full_names.append(' '.join(text.split()[::-1][0:][::-1]))

print(full_names[0])
