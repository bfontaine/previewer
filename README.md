# Previewer

**Previewer** is a quick hack around [Mattermost][]’s inability to show
previews for links other than images and YouTube videos.
It’s like a proxy for your links: it acts as an image for Mattermost but will
redirect any “normal” user to the original link.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Run

**Previewer** requires Python 3.x. Install its dependencies:

    pip install -r requirements.txt

Then run the app:

    gunicorn app:app

Check [`gunicorn`][Gunicorn]’s options for ports and more. There’s also
`Procfile` and `runtime.txt` files for quick deployment on [Heroku][] &
friends (I use [Flynn][]).

[Flynn]: https://flynn.io/
[Gunicorn]: http://gunicorn.org/
[Heroku]: https://www.heroku.com/
[Mattermost]: https://about.mattermost.com/

## Usage

You have to build URLs by hand for now. Prepend `<your previewer hostname>` to
your URL, and append `/p.png` at its end. Be careful that if your original URLs
has parameter you need to put the `/p.png` *before* them.

### Examples

In the examples below we assume you deployed your instance at
`http://p.example.com`:

* `https://www.google.com` -> `http://p.example.com/https://www.google.com/p.png`
* `https://www.youtube.com/watch?v=Sagg08DrO5U` -> `http://p.example.com/https://www.youtube.com/watch/p.png?v=Sagg08DrO5U`
* `https://news.ycombinator.com/item?id=14068363` -> `http://p.example.com/https://news.ycombinator.com/item/p.png?id=14068363`

## How it works.

[See my blog post][blog].

[blog]: https://bfontaine.net/blog/2017/04/09/a-quick-link-previewer-for-mattermost/
