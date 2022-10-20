# PYMACC

This is a simple hacky script to serve a directory of markdown files over nginx's fastcgi. Put your `.md` files under `www` and add to your nginx configuration something like:

```nginx
  location ~^/notes/* {
    gzip off;
    fastcgi_pass unix:/var/run/fcgiwrap.socket;
    include /etc/nginx/fastcgi_params;
    fastcgi_param SCRIPT_FILENAME {PUT_THEPATH_HERE}/main.py;
  }
```

Replacing `{PUT_THEPATH_HERE} ` with wherever your cloned this repo into.

Run `sudo pip3 install mistune`, restart nginx and take a look at `config.py`.


# TODO

- [ ] This could use a web framework and serve over a proxy like any modern thing
- [ ] Proper packaging
- [ ] Poetry run is slow for the cgi
