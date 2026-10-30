# HERO by Omshree Art

[Open the public HERO website](https://omshreeart.github.io/toolkit/)

HERO brings together Nepali text and calendar utilities, PDF tools, image editing, media conversion, design tools and everyday text utilities. File tools run locally in the visitor's browser; online services identify their provider.

## Publishing

GitHub Pages uses the **Publish HERO website** Actions workflow in `.github/workflows/pages.yml`. It runs `python3 publish.py`, builds `_site`, uploads the Pages artifact and deploys it publicly over HTTPS.

This repository contains the compiled website release, not the full application source. `site-manifest.json` pins every release file by size and SHA-256. The publisher uses matching files already in this repository and downloads the remaining large assets from the public HERO release URL in the manifest. All files must pass verification before deployment. Visitors then load those assets directly from GitHub Pages.

For a new release, update the compiled website files, the public release source if needed, and the manifest hashes together. Editing an application file alone does not update the pinned release. You can also rerun the workflow from the Actions tab.

Dependency and model notices are included in the deployed `licenses.txt`, `ai/` and `media/` directories. Social video download tools require a compatible download service; this static website does not provide a hosted extraction API.
