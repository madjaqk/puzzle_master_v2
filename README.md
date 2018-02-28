# Puzzle Master (v2)

This project uses Python 3.6 and Django 2.0

## Getting Started

Clone the repo, install requirements, `python manage.py makemigrations` and `python manage.py migrate`, then `python manage.py loaddata puzzle_data.json` to add the existing puzzles to the database.  (**Warning**: The `puzzle_data.json` file includes spoilers for some puzzles.)

This project uses [`python-decouple`](https://pypi.python.org/pypi/python-decouple) to hide secret data from version control, so make sure you've created a `.env` file at root level with at the very least a secret key.  (You can find more examples in [the `.env-example` file](.env-example)).  You may also need to comment out some of the OAuth values from `settings.py` (pretty much everything that starts with `SOCIAL_AUTH_`), at least at first.

The most important model is `Puzzle`.  Hopefully, most of the fields are self-explanatory, but some of the more obscure ones:
* `short_name` is specifically the file name for the template to render to show that puzzle, minus the `.html`.  Note that for organization purposes, templates for the existing set are all in the `templates/puzzles/halloween` directory, so the short names of the associated puzzles also includes the `halloween/`.
* As of now, `description` only shows on the main page (`index.html`, the `puzzles:index` route), not on the actual puzzle.
* `meta_order` is used to set the order that all of the puzzles in a given meta will be displayed when using the `as_ul` template tag.  If blank, the puzzles will be sorted alphabetically by title, ignoring articles.
* `metapuzzles` is a many-to-many, non-symmetric self-join.  Note that this allows a puzzle to belong to multiple metapuzzles (as in the [Emotions round](http://www.mit.edu/~puzzle/2018/full/island/index.html) of the 2018 MIT Mystery Hunt) and for multiple metas to be part of a supermeta.

## To-Do

Some possible ideas for improvements:

* Changing answer submission to AJAX seems straightforward enough.
* As of now, correct answers are stored in the database in plain text.  I'd rather they be encrypted, just to make hypothetical cheating that much harder; however, I also wanted to include a user's history of answer submissions in the clear (so they could be shown back to them), so the vulnerability's there regardless.  It would avoid the spoilers in `puzzle_data.json`, at least.
* Also in terms of hypothetical cheating: It would be neat to do some sort of rate limiting, so that a person can't submit every 20,000 answers a second and brute force "guess" the answer.
* In the spirit of DRY, whether an answer is correct or not isn't saved directly in the database; rather, it's a method (technically a Python `@property`) that compares the submitted answer to the puzzle's saved answer.  It might be more efficient to store that on the answer itself (or have a separate table tracking which users have solved which puzzles), but I haven't tested that yet.
* It would be neat to add an unlock mechanism, where only some puzzles are available at first and solving those opens up new puzzles to solve, but I haven't made any sets large enough for that to be necessary.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* You can see version 1 [here](https://github.com/madjaqk/puzzle_master), although the code in this project was a from-scratch rewrite.
* I found two guides by Vitor Freitas, [How to Use Django's Built-in Login System](https://simpleisbetterthancomplex.com/tutorial/2016/06/27/how-to-use-djangos-built-in-login-system.html) and [How to Add Social Login to Django](https://simpleisbetterthancomplex.com/tutorial/2016/10/24/how-to-add-social-login-to-django.html), very helpful when trying to get started with Django's `auth` system.  The account settings and password change pages in particular come nearly directly from his examples.
* I'd be remiss if I didn't point to some other fantastic puzzle sites that inspired me to build this project in the first place:
  * [The MIT Mystery Hunt](http://www.mit.edu/~puzzle/)
  * The works of Foggy Brume, including [P&A Magazine](http://www.pandamagazine.com/) and his various Puzzle Boats ([1](http://www.pandamagazine.com/island/index.html), [2](http://www.pandamagazine.com/island2/index.php), [3](http://www.pandamagazine.com/island3/index.php), [4](http://www.pandamagazine.com/island4/index.php))
  * [Galactic Puzzle Hunt](https://galacticpuzzlehunt.com/)
  * [Mark Halpin's Labor Day Extravaganzas](http://www.markhalpin.com/puzzles/puzzles.html)