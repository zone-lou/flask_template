import json
import time
from flask import request, current_app, send_from_directory
from flask_restful import Resource
from werkzeug.utils import secure_filename
from pathlib import Path
from common.custom_response import generate_response
from common.ext import calculate_file_hash


class UploadRarView(Resource):

    def get(self):
        """
        获取pdf
        :return:
        """
        params = request.args
        filename = params.get('filename')
        as_attachment = params.get('as_attachment')
        if str(as_attachment).lower() == "true":
            as_attachment = True
        else:
            as_attachment = False
        pdf_upload_folder = current_app.config['RAR_UPLOAD_FOLDER']
        response = send_from_directory(f"{current_app.static_folder}/{pdf_upload_folder}", filename,
                                       as_attachment=as_attachment)
        return response

    def post(self):
        file_list = request.files.getlist("file")
        file = file_list[0]
        filename = secure_filename(file.filename)
        pdf_upload_folder = current_app.config['ZIP_UPLOAD_FOLDER']
        upload_dir = f"{current_app.static_folder}/{pdf_upload_folder}"
        if not Path(upload_dir).exists():
            Path(upload_dir).mkdir(parents=True, exist_ok=True)
        file_key = f"{calculate_file_hash(file)}{int(time.time())}"
        new_filename = f"{file_key}_{filename}"
        file_path = f"{upload_dir}/{new_filename}"
        # file.save(file_path)
        chunk_size = 8192
        with open(file_path, 'wb') as f:
            while True:
                chunk = file.stream.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)

        # dwg文件不需要生成文件路劲
        # with db.auto_commit():
        #     dwg_object = dwgInfo(
        #         file_key=file_key,
        #         file_name=new_filename,
        #         file_url="",
        #         file_path=file_path,
        #     )
        #     db.session.add(dwg_object)
        #     db.session.flush()
        #     file_id = dwg_object.id
        data = {
            # "url": file_url,
            # "file_key": file_key,
            # "id": file_id
            "fileName": new_filename,
        }
        return generate_response(data=data)
