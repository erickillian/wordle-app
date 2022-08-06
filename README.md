# Full-Stack Wordle Ranking Application  (django and vue.js)
- Hobby project, made with Django + DRF, VueJS (Vuex, Vue Rouer, Vuetify).
- App is available in one languages: English. (Support could be added for more)

## Features

- Daily ranking system, first rankes wordles by number of guesses, then time
- All time ranking (uses average guesses and average time after a player has completed 10 wordles)

## Local installation steps:

1. Install docker and docker-compose
2. Install npm (comes with node.js)
3. Install npm packages and build production bundle
```
npm install
npm run build
```

4. Build the docker image 
```
docker compose build
```
5. Launch the local version of the app as a daemon (background process)
```
docker compose up -d
```
6. Create a super user account 
```
sudo docker-compose exec web python3 manage.py createsuperuser
```
7. Use superuser account at `/admin` to manage and add users

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
