from flask import current_app, Markup, Blueprint

class Share(object):
    def __init__(self, app=None):
        share = Blueprint('share', __name__, static_folder='static',
                          static_url_path='/share/static')
        app.register_blueprint(share)

        app.jinja_env.globals['share'] = self

        # default settings
        app.config.setdefault('SHARE_SITES', 'google,facebook,twitter')
        app.config.setdefault('SHARE_SERVE_LOCAL', False)

    @staticmethod
    def create(title='', sites=None,  align='left', addition_class=''):
        """Create a share component.

        :param title: the prompt dispalyed on the left of the share component.
        :param sites: a string that consist of sites, separate by comma. supported site name:  facebook, twitter,google.
        :param mobile_sites: the sites displayed on mobile.
        :param align: the align of the share component, default to `'left'`.
        :param addition_class: the style class added to the share component.
        """

        if sites is None:
            sites = current_app.config['SHARE_SITES']

        return Markup('''<div class="social-share %s" data-sites="%s" align="%s">%s</div>''' % (addition_class, sites,  align, title))

