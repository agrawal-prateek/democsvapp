import csv
import os
import random
import string

from flask import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_data', methods=['POST'])
def get_data():
    files = request.form.getlist('filenames')
    fields = request.form.getlist('fieldnames')
    print(fields)
    filedata = dict()
    included_cols = [int(fieldname[-1:])-1 for fieldname in fields]
    for filename in files:
        data = list()
        csvfile = open(os.path.join('static', filename),newline='')
        for row in csv.reader(csvfile, delimiter='\t'):
            content = list(row[i] for i in included_cols)
            data.append(content)
        filedata[filename] = {'fields': fields, 'data': data}
        csvfile.close()

    return jsonify(filedata=filedata)


@app.route('/getfilenames', methods=['GET'])
def getFileNames():
    return jsonify(items=os.listdir('static'))


@app.route('/generate_random_csv', methods=['GET', 'POST'])
def generate_random_csv():
    def random_string(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    try:
        for file in os.listdir('static'):
            os.unlink(os.path.join('static', file))
        for i in range(random.randrange(50, 100)):
            data = 'field1	field2	field3	field4	field5	field6	field7	field8	field9'
            for j in range(random.randrange(5, 10)):
                data += '\n'
                for k in range(8):
                    data += random_string(size=random.randrange(2, 15)) + '\t'
                data += random_string(size=random.randrange(2, 15))
            with open('static/file' + str(i + 1) + '.csv', 'w+') as csv_file:
                csv_file.write(data)
        return 'true'
    except Exception as e:
        print(e)
        return 'false'


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
