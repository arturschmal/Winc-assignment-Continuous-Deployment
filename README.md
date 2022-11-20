[![Test and Deploy](https://github.com/arturschmal/winc-cd/actions/workflows/run-test-deploy.yml/badge.svg)](https://github.com/arturschmal/winc-cd/actions/workflows/run-test-deploy.yml)

# Winc Continuous Deployment assignment report

Although not much Python coding was involved this turned out to be an assignment not that easy. At first it felt like we were just required to follow tutorial-like steps, but eventually there were enough pitfalls and challenges along the way that required an effort in thinking and researching.

## Components

During this module we were introduced to quite a few new concepts and software and it took me a while to grasp how the various components related to each other. I was wondering things like why Nginx was needed while there was already a VPS and Ubuntu? And what is Gunicorn for? I asked for a bit of elaborating on this on the Slack channel and mentor Jip pointed me to an article that made things a bit clearer for me. After that I was able to make a visualization that reflects how I understand the components and their relation.

<img src="/static/cd_pipeline.jpeg" width="600"/>

At the bottom of the process there is me, making a Flask app and pushing that to the remote Github repository. When I push to this repo there’s a Github Actions `yaml` file activated that runs a `pytest` on my app and if it passes the test, it logs into a remote server and pulls the flask app to that server. 

That server can be a physical or virtual server. In this case it’s a virtual server. In order to execute stuff on that server, it needs an operating system running on it, Ubuntu in this case.

On that operating system three components are installed:

- the Flask app
- Gunicorn: a Web Server Gateway Interface
- Nginx: a webserver

The Flask app is the website or web application itself, written in a python based framework. In order to be accessible to users on the internet, we need a webserver: Nginx. In order for the webserver and the Flask app to be able to communicate with eachother, they need a translator: Gunicorn.

## Problems

Along the way I encountered some problems that I had to tackle. The first problem I encountered was how to get my app from the remote github repository to the virtual private server using Github Actions. The marketplace for actions offered some solutions and eventually I chose for a widely used action called `appleboy/ssh-action@v0.1.4`.

This action requires you to have:

- SSH access to the remote server
- Github Secrets

Making the SSH connection to the server did not go without a struggle. I followed Github’s recommendations for generating an ssh key on the server. But somehow I did not manage to do that succesfully. After doing some online research I found a tutorial that helped me with both making the key, and setting up the Github secrets successfully. It turned out I was placing the public and private part of the key in the wrong places.

Now I was able to make the connection and pull my repository to the remote server successfully. After that I made final preparations on the remote server by modifying these files:

```bash
/etc/systemd/system/winc-cd.service 
/etc/nginx/sites-available/default
```

Followed by a restart of the webserver: `systemctl restart nginx` and my flask app was visible live on [`http://178.128.255.173/`](http://178.128.255.173/)!

Unfortunately that was not the end of it. I couldn’t resist trying out another method of deploying my files to the vps. I was thinking that maybe pulling repositories in it’s entirety to a webserver is not such a good idea. Git is a versioning system, why should that be on the webserver? You don’t need all the files on the repository for serving the web app to users, so it’s much cleaner to only deploy the files you need.

To this end I used another github action that allows you specify exactly which files from the source repo you want to copy to the target directory on the vps. In doing so I deleted the directory with the clone of the repository in it on the vps, and created a new directory to deploy my files to. This caused an issue with running processes of Gunicorn that were referring to the deleted directory and it caused serving a cached version of my webapp to the browser.

I could not find this cause myself and turned to Slack for help. Sebastiaan helped me with finding the problem with the processes and suggested I ran `systemctl restart winc-cd`. That solved the issue in the end.

In the process of solving the last problem I reverted back to my first deploy method, but the second method can still be seen commented out in my `yaml` file.
