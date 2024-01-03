
### Build using Docker

```sh
docker build -t latex .
docker run --rm -i -v "$PWD":/data latex pdflatex maxence_bouvier_resume.tex
```

### Preview

![Resume Screenshot](/resume_preview.png)
