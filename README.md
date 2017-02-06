# task-app-demo

This is a simple task management application created just for demo purposes.

Check out how does it work here: https://task-app-demo.herokuapp.com

Local setup looks like:

1. checkout repo
2. install and activate venv
3. install packages listed in requirements.txt
4. migrate database
5. create django's superuser
6. make sure you have Google's `client_id` and `secret` set up.https://developers.google.com/identity/sign-in/web/devconsole-project
7. create SocialApp by using admin site and put your google credentials to be able to use oAuth2. 
Otherwise you can just login throught `/admin/login/?next=/`
8. try application
