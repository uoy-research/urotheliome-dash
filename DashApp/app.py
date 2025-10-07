import dash
from flask import Flask, session
from callbacks.gene_callbacks import register_callbacks
from layouts.layout_manager import create_layout, register_layout_callbacks
from layouts.navigation import register_navbar_callbacks
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dotenv import load_dotenv
from flask_sso import SSO

load_dotenv()

# Initialise Flask server - required for login
server = Flask(__name__)

# Initialize Dash app with Bootstrap theme
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME  # Add Font Awesome for icons
    ],
    suppress_callback_exceptions=True,
    use_pages=False  # We're using our own routing solution
)

# Setup SSO
ext = SSO(app=server)

# TODO Where should routes live?
@server.route('/login')#, methods=['POST'])
def login():
    if 'user' in session:
        return 'Welcome {name}'.format(name=session['user']['nickname'])
    return redirect(server.config['SSO_LOGIN_URL'])

# TODO where should this go, and is it sensitive?
#: Default attribute map
SSO_ATTRIBUTE_MAP = {
    'ADFS_AUTHLEVEL': (False, 'authlevel'),
    'ADFS_GROUP': (True, 'group'),
    'ADFS_LOGIN': (True, 'nickname'),
    'ADFS_ROLE': (False, 'role'),
    'ADFS_EMAIL': (True, 'email'),
    'ADFS_IDENTITYCLASS': (False, 'external'),
    'HTTP_SHIB_AUTHENTICATION_METHOD': (False, 'authmethod'),
}
server.config['SSO_ATTRIBUTE_MAP'] = SSO_ATTRIBUTE_MAP

# TODO where should this go?!
@ext.login_handler
def login_callback(user_info):
    """Store information in session."""
    session['user'] = user_info

# Set HTML lang attribute for accessibility
app.index_string = '''
<!DOCTYPE html>
<html lang="en">
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Set the main layout with the layout manager
app.layout = dmc.MantineProvider(
    theme={
        "colorScheme": "light",
    },
    children=create_layout()
)
app.title = "Urotheliome"

# Register all callbacks
register_layout_callbacks(app)  # For page routing
register_navbar_callbacks(app)  # For navbar toggle on mobile
register_callbacks(app)         # For gene visualization

# Run the app (for development only)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
