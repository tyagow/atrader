
Como fazer o Deploy?
---------------------------

1. Install Digital Ocean Dokku image
2. Send your ssh-key to dokku
3. Connect via ssh to your server
4. Create app in dokku
5. Install postgres plugin in dokku
6. Create database for your app in dokku
7. Link database and app in dokku
8. Set DEBUG in dokku
9. Generate new SECRET_KEY
10. Set SECRET_KEY in dokku
11. Set ALLOWED_HOSTS in dokku
12. Set Global Domain dor dokku
13. Push your code to dokku
14. Run the migrations
15. Collect static data with DEBUG=False

Digite no terminal ::

    (local) cat ~/.ssh/id_rsa.pub | ssh root@<your.ip.address> "sudo sshcommand acl-add dokku [description]"
    (local) ssh root@<your.ip.address>
    (server) dokku apps:create <app-name>
    (server) sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git
    (server) dokku postgres:create <database-name>
    (server) dokku postgres:link <databse-name> <app-name>
    (local) git remote add dokku dokku@dokku.me:<app-name>
    (local) ssh dokku@<your.ip.address> config:set <app-name> DEBUG=False
    (local) python contrib/secret_gen.py
    (local) ssh dokku@<your.ip.address> config:set <app-name> SECRET_KEY='<new-generated-key>'
    (local) ssh dokku@<your.ip.address> config:set <app-name> ALLOWED_HOSTS=<app-name>.<your.ip.address>.xip.io
    (local) ssh dokku@<your.ip.address> config:set <app-name> AWS_STORAGE_BUCKET_NAME=atrader AWS_ACCESS_KEY_ID= AWS_SECRET_ACCESS_KEY=+EAVvP7JSowfje
    (local) ssh dokku@<your.ip.address> domains:add-global <your.ip.address>.xip.io
    (local) ssh dokku@<your.ip.address> domains:enable <app-name>
    (local) git push dokku master
    (local) ssh dokku@<your.ip.address> run <app-name> python manage.py migrate
    (local) DEBUG=False python manage.py collectstatic


.. note:: * Depois do primeiro deploy feito basta um comando para o deploy:
            ``git push dokku master``

            * Não esquecer de migrar/atualizar o banco de dados sempre que alterar um modelo:
            ``ssh dokku@<your.ip.address> run <app-name> python manage.py migrate``

* http://dokku.viewdocs.io/dokku/deployment/application-deployment/

Dokku
-----

* Change PORT
`
(não recomendado, se configurar na porta 80 só poderei ter 1 serviço (app) )
" you can only bind a single service to port 80 if you do not use a vhost
but i highly suggest using a vhost for your server
so then you get urls like
app.vhost.com " @ savant`

`
dokku config:set APP DOKKU_NGINX_PORT=80 DOKKU_PROXY_PORT_MAP=http:80:5000
`

* **Configurar um vhost**
``dokku domains:add-global domain_here``

* **Re-enable vhosts for your app**
( http://dokku.viewdocs.io/dokku/configuration/domains/ )
``dokku domains:enable APP``

* **Server < 1 GB RAM**
* http://dokku.viewdocs.io/dokku/getting-started/advanced-installation/#vms-with-less-than-1gb-of-memory

Run on server::

    cd /var
    touch swap.img
    chmod 600 swap.img

    dd if=/dev/zero of=/var/swap.img bs=1024k count=1000
    mkswap /var/swap.img
    swapon /var/swap.img
    free

    echo "/var/swap.img    none    swap    sw    0    0" >> /etc/fstab

Configurar AmazonS3
-------------------

* https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/


Circle-ci Automatic Deploy to Dokku
-----------------------------------


1. Generate new ssh-key without password - Give a name to the file.
2. Copy new ssh-key.pub to your project (you must be in your root project)
3. Add ssh-key private to circle-ci in circle-ci website
4. Edit circle.yml
5. add ssh-key to dokku server (go to :ref:`add-ssh-to-dokku` section)


Terminal::

    $ ssh-keygen -t rsa
    $ cp ~/.ssh/<ssh-key>.pub ./deploy_utils/deploy_key
    $ circle.yml ->
            machine:
              python:
                version: 3.5.1
            general:
              artifacts:
                - "htmlcov"
            dependencies:
              pre:
              - cp contrib/env-sample .env
            test:
              override:
                - coverage run manage.py test
              post:
                - coverage html -d $CIRCLE_ARTIFACTS
            deployment:
              production:
                branch: master
                commands:
                  - git remote add deploy dokku@<server ip>:<dokku app name>
                  - git push deploy maste


Travis-ci Automatic Deploy to Dokku
-----------------------------------


1. Generate new ssh-key without password - Give a name to the file.
2. Copy new ssh-key.pub to your project (you must be in your root project)
3. Install Travis CI Command Line Client
4. Login to travis
5. Encrypt new ssh key (private) with travis and copy the command to decrypt in terminal
6. Edit .travis.yml
7. add ssh-key to dokku server (go to :ref:`add-ssh` section)

http://tannguyen.org/2017/02/set-up-hugo-dokku-and-travis/

Terminal::

    $ ssh-keygen -t rsa
    $ cp ~/.ssh/<ssh-key>.pub ./deploy_utils/deploy_key
    $ sudo gem install travis
    $ travis login
    $ travis encrypt-file deploy_utils/deploy_key
    ->[.travis.yml] add before install:
        before_install:
          - openssl aes-256-cbc -K $encrypted_5d3fad67a2c7_key -iv $encrypted_5d3fad67a2c7_iv -in deploy_utils/deploy_key.enc -out deploy_utils/deploy_key -d
          (this command should be given after run travis encrypt-file [...]
    ->[.travis.yml] add after script:
        after_success:
          - eval "$(ssh-agent -s)" #start the ssh agent
          - chmod 600 deploy_utils/deploy_key # this key should have push access
          - ssh-add deploy_utils/deploy_key
          - echo -e "Host <hostname here>\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config
          - git remote add deploy <git-remote>
          - git push deploy


Errors:
~~~~~~
1. installing travis via `sudo gem install travis`

    ERROR:  Error installing travis:
    ERROR: Failed to build gem native extension.

Solution
- https://github.com/travis-ci/travis.rb/issues/391 ::

 sudo apt-get install python-software-properties
 sudo apt-add-repository ppa:brightbox/ruby-ng
 sudo apt-get update
 sudo apt-get install ruby2.1 ruby-switch
 sudo ruby-switch --set ruby2.1
 sudo apt-get install ruby2.1-dev


Add ssh-key to dokku
--------------------

1. Create a ssh-key
2. send ssh-key to server

Terminal::

    ssh-keygen -t rsa
    cat <path to ssh-key> | ssh root@<your.ip.address> "sudo sshcommand acl-add dokku [description]"
