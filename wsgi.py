from app import create_app
from utils.logger import init_logging

init_logging()
application = create_app()
