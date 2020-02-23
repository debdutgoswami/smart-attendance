# system libraries
import os, random,  json

# user-defined
from scripts import speechTOtext, random_string

# flask
from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from flask_cors import CORS

# firebase
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

KEY = 'any random string'
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")

# flask initialization
app = Flask(__name__)
CORS(app)
app.config['KEY'] = KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)

# firebase initialization
cred = credentials.Certificate("path to your credentials")
firebase = firebase_admin.initialize_app(cred)

class File(Resource):
    def post(self):
        key, end = dict(request.form)['key'], int(dict(request.form)['end'])
        prev = None
        try:
            prev = int(dict(request.form)['prevContext'])
        except KeyError:
            prev = 1
        if key is None or key != app.config['KEY']:
            abort(401)

        # key check
        # generating a new random name to avoid name collision during multiple requests at same time
        new_filename = random_string.randomString(random.randint(5,15))

        try:
            # uploading to the UPLOADS_FOLDER
            file1 = request.files['prevAudio']
            file2 = request.files['currAudio']
            filename1 = secure_filename(file1.filename)
            filename2 = secure_filename(file2.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))

            # executing the ffmpeg CLI
            cmd = f"cd {app.config['UPLOAD_FOLDER']} && ffmpeg -i {filename1} -i {filename2} -filter_complex \"[0:0][1:0]concat=n=2:v=0:a=1[out]\" -map \"[out]\" {new_filename}.wav"
            os.system(cmd)

            #removing the old uploaded file
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
        except KeyError:
            # uploading to the UPLOADS_FOLDER
            file = request.files['currAudio']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # executing the ffmpeg CLI
            cmd = f"cd {app.config['UPLOAD_FOLDER']} && ffmpeg -i {filename} {new_filename}.wav"
            os.system(cmd)

            #removing the old uploaded file
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # printing the transcribe for the new file generated by ffmpeg
        response_speech = speechTOtext.transcribe(os.path.join(
            app.config['UPLOAD_FOLDER'], f"{new_filename}.wav"), end, prev)
        
        return response_speech['response'], response_speech['response_code']

# firebase prof updation
class Prof(Resource):
    def post(self):
        # authentication
        key = dict(request.form)['key']
        if key is None or key != app.config['KEY']:
            abort(401)

        pui, pname = dict(request.form)['pui'], dict(request.form)['pname']

        db.reference(path='/', url='your firebase url').child(pui).update({
            "pname": pname
        })

        return 'OK', 201

class Class(Resource):
    def post(self):
        # authentication
        key = dict(request.form)['key']
        if key is None or key != app.config['KEY']:
            abort(401)

        pui, cname, endroll = dict(request.form)['pui'], dict(request.form)['cname'], int(dict(request.form)['endroll'])
        cui = os.urandom(12).hex()

        db.reference(path=f'{pui}', url='your firebase url').child(cui).update({
            "cname": cname,
            "endroll": endroll
        })

        return cui, 201

class AllClass(Resource):
    def post(self):
        # authentication
        key = dict(request.form)['key']
        if key is None or key != app.config['KEY']:
            abort(401)

        pui = dict(request.form)['pui']

        classes = list(db.reference(path="", url='your firebase url').child(f'{pui}').get().keys())

        response = dict()
        classes.remove('pname')
        for cl in classes:
            cname = db.reference(path=f'{pui}', url='your firebase url').child(cl).get()['cname']
            response[cl] = cname
        
        return response, 201

class Update(Resource):
    def post(self):
        # authentication
        key = dict(request.form)['key']
        if key is None or key != app.config['KEY']:
            abort(401)

        # getting the form-data
        pui, cui, endroll, ab, timestamp = dict(request.form)['pui'], dict(request.form)['cui'], int(dict(request.form)['endroll']), list(map(int,str(dict(request.form)['absent']).strip('{}').split(','))), dict(request.form)['timestamp']

        # generating integer set of both absent and present
        present, absent = list(), list()
        attendance = dict()
        for roll in range(1, int(endroll)+1):
            if roll not in ab:
                present.append(roll)
        for ch in ab:
            absent.append(int(ch))

        # sorting it roll number wise
        attendance = dict(sorted(attendance.items(), key=lambda kv: (kv[0], kv[1])))

        #updating in firebase realtime database
        db.reference(path=f'{pui}/{cui}', url='your firebase url').child(timestamp).update({
            'present': sorted(present),
            'absent': sorted(absent)
        })

        return 'OK', 201

class Report(Resource):
    def post(self):
        # authentication
        key = dict(request.form)['key']
        if key is None or key != app.config['KEY']:
            abort(401)

        cui = dict(request.form)['cui']

        puis = db.reference(path="", url='your firebase url').get().keys()
        details = None
        for pui in puis:
            cuis = db.reference(path="", url='your firebase url').child(f'{pui}').get().keys()
            if cui in cuis:
                details = db.reference(path=f'{pui}', url='your firebase url').child(f'{cui}').get()

        return details, 201

'''
TODO create the student register API
'''
class Register(Resource):
    def post(self):

        return 'OK', 201

# url route for API
api.add_resource(File, '/upload')
api.add_resource(Prof, '/prof')
api.add_resource(Class, '/class')
api.add_resource(AllClass, '/allclass')
api.add_resource(Update, '/update')
api.add_resource(Report, '/report')
api.add_resource(Register, '/register')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))