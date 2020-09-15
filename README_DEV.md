# Developers guide

## Versioning

The versioning follows [pep_440](https://www.python.org/dev/peps/pep-0440) with only beta as pre-release option.
To use the automated updating install bump2version

```
pip install bump2version
```

### Major

There are breaking changes making it no longer backward compatible.

Example: version 0 didn't require a serial number, version 1 does.

```
bump2version major
```

### Minor

New feature is added but everything is still backward compatible.

Example: version 1.0 could not get temperature but version 1.1 did have a function for it.

```
bump2version minor
```

### patch

Just for bugfixes.
No new function or logic is introduced.
Backwards compatibility is there for all situations without a bug.

```
bump2version patch
```

### release

By default the version number ends with b0.
This means it is a beta release.
Once a release is going to be made from the master branch this is removed.

example: 1.0.0b0

```
bump2version release
```

### build

Nothing of the code is changed but the pipeline needed to be triggered again.
This is for when something went wrong with launching or building but a release was made.

```
bump2version build
```
