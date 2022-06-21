# RANKER 🏓

### General Games and Stats for Offices or Local Leagues

##### !NOTE this site only contains convergle, a wordle clone

Add players, Ratings and leaderboard are updated automatically.

Hobby project, made with Django + DRF, VueJS (Vuex, Vue Rouer, Vuetify).

#### Localization

App is available in one languages: English. (Support could be added for more)

##### Local installation steps:

1. Install docker and docker-compose
2. Build the docker image `$ sudo docker-compose build`
3. Launch the local version of the app `$ sudo docker-compose up -d`
4. Create a super user account `$ sudo docker-compose exec web python3 manage.py createsuperuser`
5. Use superuser account at `/admin` to manage the database content and to save new match results.

##### Heroku deployment:

> :warning: **This section is out of date and likely will not work**: If you want to contribute and help me get this working feel free


1. Sign up for free Heroku account and install Heroku CLI
2. Shell commands:

```
$ heroku apps:create your_app_name
$ heroku git:remote --app your_app_name
$ heroku buildpacks:add --index 1 heroku/nodejs
$ heroku buildpacks:add --index 2 heroku/python
$ heroku addons:create heroku-postgresql:hobby-dev
$ heroku config:set DJANGO_SETTINGS_MODULE=ranker.settings.prod
$ heroku config:set RANKER_SECRET_KEY='production SECRET_KEY value'

# superuser section, set values as needed
$ heroku config:set DJANGO_SUPERUSER_USERNAME=admin
$ heroku config:set DJANGO_SUPERUSER_PASSWORD=admin
$ heroku config:set DJANGO_SUPERUSER_EMAIL=admin@admin.admin

$ git push heroku
```

3. Use `$ heroku open` to reach the application.

**Big thanks** to [gtalarico/django-vue-template](https://github.com/gtalarico/django-vue-template) for settings template and perfect instructions.
