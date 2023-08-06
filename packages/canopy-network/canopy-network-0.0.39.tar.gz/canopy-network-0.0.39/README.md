# canopy
A decentralized social network of personal websites

Store and display content on your own personal website. Interact richly
with other sites.

## Install

[Spawn a host](https://gh.ost.lol) and map `canopy-network` to your domain.

### Manually

    $ pip install canopy-network
    $ web serve canopy

## Features

* render profile, pages, media, posts and feeds with semantic markup a la [microformats](https://indieweb.org/microformats)
  * archive source material for [reply contexts](https://indieweb.org/reply-context)
  * moderated threaded discussion using Webmentions with Salmention & Vouch
  * syndicate to third-party aggregators
* store posts:
  * as [queryable JSON](https://www.sqlite.org/json1.html) in SQLite database
    * [full-text search](https://www.sqlite.org/fts5.html)
  * as JSON flat files inside Git repository for change history
* follow by subscribing and publish to subscribers using WebSub
* sign in to third-party applications using IndieAuth
  * leverage third-party Micropub editors
  * leverage third-party Microsub readers
* import/export tools
  * syndicate/backfeed to/from Twitter/Github/Facebook
  * backup/restore to/from local/remote storage
