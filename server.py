from flask_app import app
# Import ALL controller files
from flask_app.controllers import admin_controller, option_controller, ui_controller

# MUST be at the bottom 
if __name__=="__main__":
    app.run(debug=True)