import avro.schema, csv, codecs
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

schema = avro.schema.parse(open("movies_final.avsc").read())

with codecs.open('data_0_0_0.csv', 'r', encoding='latin_1') as csvfile:
	reader = unicode_csv_reader(csvfile, delimiter=',')
	writer = DataFileWriter(open("movies_demo.avro", "w"), DatumWriter(), schema, codec='deflate')
	for count, row in enumerate(reader):
		print count
		try:
			writer.row[2].replace('\,',',')
			writer.row[3].replace('\,',',')
			writer.append({"title": row[0], "year": row[1], "cast_": row[2], "genres": row[3]})
		except IndexError:
			print "Bad record, skip."
	writer.close()

# Uncomment to read and print the data from the Avro file

# reader = DataFileReader(open("data/songs.avro", "r"), DatumReader())
# for user in reader:
#     print user
# reader.close()
