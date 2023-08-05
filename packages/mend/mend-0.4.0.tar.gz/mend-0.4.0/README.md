# mend

Mend, update, and repair git repositories.


## Design

Provides a semi-generic mechanism to produce changes -- using a `Generator` -- and
and apply them to repositories -- using a `Plugin`:

 - `generators` produce one or more files.

   Generator may produce files from templates or programmatic manipulations of existing
   files (in some git repository).

 - `plugins` apply the files produced by a generator to something.

   Plugins may simply output planned changes or may apply them a repository in some way.


## CLI

Both generators and plugins use `setuptools` `entry_points` for extensibility: the `mend`
CLI reflects the known instances of both types and allows `Generator` and `Plugin` implementations
to provide custom CLI parameters.

For example, the `.circlci/config.yml` file in this repo was generated using:

```sh
mend circleci --project mend copy --path .
```
