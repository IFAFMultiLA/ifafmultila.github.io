# MultiLA platform documentation source

Markus Konrad <markus.konrad@htw-berlin.de>, Feb. 2024

This repository contains the source for the documentation of the MultiLA software platform as it is hosted on [ifafmultila.github.io](https://ifafmultila.github.io/). The documentation is written in the [ReStructuredText format](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html) and is transformed to HTML using the he [Sphinx documentation system](https://www.sphinx-doc.org/en/master/).

## Initial setup

1. Create a *Python virtual environment (venv)* e.g. via `python -m venv venv`.
2. Activate the *venv* and install the required dependencies via `pip install -r requirements.txt`.
3. Check that everything works by running `make`; this should simply output a help page for Sphinx.

## Generating the documentation

1. Make sure that you have activated your *venv*.
2. Run `make html` to generate the HTML in the `docs` folder.
3. Check the documentation locally by opening `docs/index.html` in a browser.

Note: `make clean` will remove all output in the `docs` folder.

## Generating codebooks

There are two codebooks (data structure documentations) that are part of this repository and the overall documentation: one for the raw tracking data as it is exported from the MultiLA administration interface and one for the prepared tracking data as it is generated through the `prepare.R` script in the [TrackingDataScripts repository](https://github.com/IFAFMultiLA/TrackingDataScripts). Separate PDFs for these codebooks can be generated via `make codebook_pdfs`. They can be copied to their respective repositories via `make copy_codebooks`. 

## Publish the documentation

Make a git commit of your changes including the updated HTML files in the `docs` folder. The documentation will automatically be published to [ifafmultila.github.io](https://ifafmultila.github.io/) a few seconds to minutes after you push your commits to the repository on GitHub.

