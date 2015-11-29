import os
from flask import Flask, render_template, session, g, abort


def create_app(settings_path):
    # setup flask
    app = Flask('jazzband')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html'), 404

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('forbidden.html'), 403

    @app.errorhandler(500)
    def error(error):
        return render_template('error.html'), 500

    @app.before_request
    def before_request():
        g.user_access_token = session.get('user_access_token', None)
        user_login = session.get('user_login', None)
        if g.user_access_token and not user_login:
            user_login = github.get('user').get('login', None)
            if user_login is None:
                abort(500)
            session['user_login'] = user_login
        g.user_login = user_login

    # load decoupled config variables
    app.config.from_object(settings_path)

    if 'SENTRY_DSN' in os.environ:
        from raven.contrib.flask import Sentry
        sentry = Sentry(app)

    from whitenoise import WhiteNoise
    app.wsgi_app = WhiteNoise(
        app.wsgi_app,
        root=app.static_folder,
        prefix=app.static_url_path,
    )

    # setup github-flask
    from .github import github
    github.init_app(app)
    app.template_filter('is_member')(github.is_member)

    # setup webassets
    from .assets import assets
    assets.init_app(app)

    # setup session store
    from flask.ext.session import Session
    Session(app)

    # setup flatpages
    from .views.content import pages
    pages.init_app(app)

    from .views.account import account
    from .views.content import content
    from .views.org import org
    app.register_blueprint(account)
    app.register_blueprint(content)
    app.register_blueprint(org)

    return app