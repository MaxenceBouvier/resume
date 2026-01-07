# TODO

## ~~feat: Build website from CSV data with exclude tag support~~

**Status:** ✅ Completed

### Summary

The website is now built from the same CSV data source as the LaTeX CV, with support for an exclude tag to filter out entries that shouldn't be shown publicly.

### Implemented

- [x] Added `--exclude-tags` / `-x` option to `make_cv website` command
- [x] Filter excludes entries that have ANY of the specified tags
- [x] Output to `ext/bio-website-launch/src/data/` by default

### Usage

```sh
# Generate website data, excluding entries tagged as 'sensitive'
make_cv website --exclude-tags sensitive

# Or with multiple exclude tags
make_cv website -x sensitive -x private
```
