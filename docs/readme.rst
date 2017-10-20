=============================
Autometed Trader
=============================


.. image:: https://travis-ci.org/tyagow/atrader.svg?branch=master
    :target: https://travis-ci.org/tyagow/atrader

Documentation
-------------

The full documentation is at http://atrader.readthedocs.io.

Quickstart
----------

1. Clone o repositório.
2. Crie um virutalenv com o Python 3.6
3. Ative o Virtualenv.
4. Instale as dependencias.
5. Configure as variaveis sensiveis do projeto com o .env
5. Configure as variaveis referentes ao dokku no arquivo deploy_utlis/.env
6. Migre seus modelos para o Banco de Dados
7. Roda o collectstatic para configurar arquivos staticos
8. Execute os testes.

Digite no terminal::

    git clone https://github.com/tyagow/atrader.git ATrader
    cd ATrader
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    cp contrib/env-sample .env
    cp contrib/env-d0kku-sample deploy_utlis/.env
    python manage.py collectstatic
    python manage.py migrate
    python manage.py test
    python manage.py runserver


Como fazer o Deploy?
--------------------

:doc:`deploy`

Features
--------

* Django 1.11.4
* Bootstrap 3
* JQuery 3.1.1
* Python Decouple
* DJ Static (serving static files locally)
* Dj Database URL
* Django test without migrations
* Django Crispy Forms
* Django bootstrap3
* Social User Login App* (facebook e twitter)
* Django Extensions
* Dokku pre configured
* Multi languange i18n
* Coverage

**Need additional configuration**

Social Auth
------------

* **Adicionar ao INSTALLED_APPS**
::

  'social_django',

* **Adicionar ao settings.py**
::

  AUTHENTICATION_BACKENDS = (
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
  )

* **Adicionar ao requirements.txt**

::

 social-auth-app-django

* **Adicionar ao urls.py**
::

  url('', include('social_django.urls', namespace='social'))

* **Adicionar ao MIDDLEWARE_CLASSES**
::

    'social_django.middleware.SocialAuthExceptionMiddleware',

* **Adicionar ao TEMPLATES**
::

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',

* **Configurar variaveis no .env e no servidor**
::

    SOCIAL_AUTH_TWITTER_KEY=
    SOCIAL_AUTH_TWITTER_SECRET=
    SOCIAL_AUTH_FACEBOOK_KEY=
    SOCIAL_AUTH_FACEBOOK_SECRET=

* **Configurar o HOST no App do Facebook**

* **Uncomment buttons to social login in registration/login.html**

* Tutorial: https://simpleisbetterthancomplex.com/tutorial/2016/10/24/how-to-add-social-login-to-django.html

Translation
-----------

* Tutorial: http://www.marinamele.com/taskbuster-django-tutorial/internationalization-localization-languages-time-zones


Running Tests
--------------

Does the code actually work?

::

    source .venv/bin/activate
    (myenv) $ python manage.py test


