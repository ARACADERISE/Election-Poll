from src.render_app import RenderWebpage

FLASK_APP = RenderWebpage()
FLASK_APP._setup_homepage_()

if __name__ == '__main__':
    FLASK_APP._RUN_()