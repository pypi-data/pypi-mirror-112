# django-doctor

[![pypi-image]][pypi]
[![semver-image]][semver]

**Django code quality assistant. Offline version of https://django.doctor**

Find and fix around 40 breaches of Django best practice - helping you build world-class websites, release faster, and reduce dev costs.

---

## Installation

    $ pip install django-doctor


## Fix

Run the fix suggestion wizard like so:

    $ django_doctor fix

This runs a simple server on http://localhost:9000 and opens the wizard in your browser:

![](https://i.imgur.com/GMcuQFl.png)

You then accept or reject the suggestions

![](https://i.imgur.com/0FRqflf.png)

And ultimately the selected changes are saved to your file system

![](https://i.imgur.com/rMeNH4n.png)

You can change the address:

	$ django_doctor fix --address=0.0.0.0 --port=9001

Your virtual environment directory is automatically skipped. To exclude other directories use the `--ignore` flag:

    $ django_doctor fix --ignore=foo # single directory
    $ django_doctor fix --ignore=foo --ignore=bar # multiple directories

You can also specify a directory to check instead of running on the current working directory. To run on only on "my_app" and "my_other_app":

	$ django_doctor fix my_app my_other_app


## Check

You can see suggested changes in your shell:

    $ django_doctor check

![](https://i.imgur.com/jb5Q9P3.png)

Consider running this as a pre-commit hook, or on your CI to prevent new Django anti-patterns from being merged.

You can also use `--ignore` the same as with the `fix` command.

## Configuration

You turn checks on/off with `--disable` and `--enable`. See [here](https://django.doctor/config) for the codenames of the checks.

## Troubleshooting

### Debugging

Try running `django_doctor` in verbose mode by adding `--log-level=debug` when executing the `fix` or `check` commands.


### Pipenv

If you're using `pipenv` you may need to do `pipenv install django-doctor --pre` because:

- `django-doctor` depends on [black](https://pypi.org/project/black/)
- `black` only releases pre-releases
- `pipenv` ignores pre-releases


[pypi-image]: https://badge.fury.io/py/django-doctor.svg
[pypi]: https://badge.fury.io/py/django-doctor
[semver-image]: https://img.shields.io/badge/Versioning%20strategy-SemVer-5FBB1C.svg
[semver]: https://semver.org

## Support

Chat with us on https://django.doctor if you have any problems or have a feature request

## GitHub integration

Django Doctor has GitHub integration. Learn more at https://django.doctor/github