# TODO

## feat: Build website from CSV data with exclude tag support

**Status:** Open

### Summary

The website should be built from the same CSV data source as the LaTeX CV, with support for an exclude tag to filter out entries that shouldn't be shown publicly.

### Requirements

- [ ] Modify `make_cv website` command to support `--exclude-tags` option
- [ ] Filter out entries with specified tags during website JSON generation
- [ ] Output to `ext/bio-website-launch/src/data/` by default

### Use Case

Some CV entries (like current employer details) should appear in the PDF resume but not on the public website. Using tags like `private` or `exclude-web` would allow filtering these out.

### Example Usage

```sh
# Generate website data, excluding entries tagged as 'private'
make_cv website --exclude-tags private

# Or with multiple exclude tags
make_cv website --exclude-tags private,confidential
```
