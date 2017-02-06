# task-app-demo

This is a simple task management application created just for demo purposes.

Check out how does it work here: https://task-app-demo.herokuapp.com

To run locally please make sure you have Google's `client_id` and `secret` set up.
https://developers.google.com/identity/sign-in/web/devconsole-project

You have to create SocialApp model with your google credentials to be able to use oAuth2. 

Otherwise you can just login throught `/admin/login/?next=/`
