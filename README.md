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

Run `sudo pip3 install mistune Pygments`, restart nginx and take a look at `config.py`.

## Writting

The folder structure under `www` defines the routes. If an invalid path is requested, the index listing is shown for the upper valid path. Just create any markdown file and use github syntac. It also enables most of the plugins of mistune: https://mistune.lepture.com/en/latest/plugins.html


# TODO

- [ ] This could use a web framework and serve over a proxy like any modern thing
- [ ] Proper packaging
- [ ] Poetry run is slow for the cgi
