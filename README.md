# termicoder-codechef-oauth
codechef authentication server for termicoder hosted on Alibaba cloud

Using client_id and client_secret from .env file in the current folder

The web server is being used for Oauth authentication (as I don't want to give away my application secret to users). 

This also servers the offline archive with extracted testcases for termicoder.

The near future plan is to use this for:
  - termicoder-random (generating random practice contests using termicoder)
  - termicoder-predict (predicting possible tags of a unknown problem using NLP and input constraints)

## NOTE
codechef does not support oauth for teams yet so termicoder doesn't work for teams
