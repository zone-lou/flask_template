from flask import Blueprint
from ..extentions import Api
from .upload_rar import UploadRarView


analysis_blue = Blueprint('analysis', __name__)
api_v2 = Api(analysis_blue, prefix='/api/v2')
api_v2.add_resource(UploadRarView, '/analysis/upload_rar')
