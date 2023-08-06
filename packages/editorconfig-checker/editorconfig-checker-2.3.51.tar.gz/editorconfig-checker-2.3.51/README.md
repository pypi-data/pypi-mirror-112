# editorconfig-checker.python
This Python implementation is simple a wrapper of the [editorconfig-checker][editorconfig-checker-repo] Go version.
Please, refer to the [original implementation][editorconfig-checker-readme] for usage.


## Installation
```
$ pip install .                     # from cloned repo
$ pip install editorconfig-checker  # from PyPI
```


## Run tests
The test script uses `docker`. After installing it, you can run the test with:
```
$ ./test.sh
```


[editorconfig-checker-repo]:   https://github.com/editorconfig-checker/editorconfig-checker
[editorconfig-checker-readme]: https://github.com/editorconfig-checker/editorconfig-checker/blob/master/README.md
