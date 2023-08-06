# Django Datatable view user columns repository

This is a small repo to allow user based custom columns.

Learn more https://github.com/icmanage/django-datatable-view-user-columns

### Build Process:
1.  Update the `__version_info__` inside of the application. Commit and push.
2.  Tag the release with the version. `git tag <version> -m "Release"; git push --tags`
3.  Build the release `rm -rf dist build *egg-info; python setup.py sdist bdist_wheel`
4.  Upload the data `twine upload dist/*`
