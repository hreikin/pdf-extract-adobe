<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Commits][commit-shield]][commit-url]
[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
<!-- [![Forks][forks-shield]][forks-url] -->
<!-- [![Stargazers][stars-shield]][stars-url] -->
<!-- [![LinkedIn][linkedin-shield]][linkedin-url] -->
<!-- PROJECT LOGO -->
<!-- <div>
  <a href="https://github.com/hreikin/pdf-toolbox">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
  <h3 align="center">PDF Toolbox</h3>
  <p>
  PDF Toolbox aims to be a PDF content extraction, conversion and creation 
  program. The goal is to extract content via various methods and store it in 
  a database for use in other document creation. 
  <br /><br />
  This should hopefully allow easier conversion to other formats and also let 
  you create new documents using any text, tables pictures, etc you may 
  already have available in other file formats.
  <br /><br />
  PDF Toolbox is in development so things will break regularly until a solid base for 
  the program has been created.
  <br /><br />
  <a href="https://github.com/hreikin/pdf-toolbox"><strong>Explore the docs »</strong></a>
  <br />
  <br />
  <a href="https://github.com/hreikin/pdf-toolbox">View Demo</a>
  <a href="https://github.com/hreikin/pdf-toolbox/issues">Report Bug</a>
  <br />
  <a href="https://github.com/hreikin/pdf-toolbox/issues">Request Feature</a>
  </p>
</div> -->



<!-- ABOUT THE PROJECT -->
## About The Project
<!-- Project Screenshot -->
<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

PDF Toolbox aims to be a PDF content extraction, conversion and creation 
program. The goal is to extract content via various methods and store it in 
a database for use in other document creation. 
<br /><br />
This should hopefully allow easier conversion to other formats and also let 
you create new documents using any text, tables pictures, etc you may 
already have available in other file formats.
<br /><br />
PDF Toolbox is in development so things will break regularly until a solid base for 
the program has been created and an initial version released.
<br />
<!-- <a href="https://github.com/hreikin/pdf-toolbox"><strong>Explore the docs »</strong></a>
<br />
<br />
<a href="https://github.com/hreikin/pdf-toolbox">View Demo</a> -->
<ol>
  <ul>
    <li>
      <a href="https://github.com/hreikin/pdf-toolbox/issues">Report Bug</a>
    </li>
    <li>
      <a href="https://github.com/hreikin/pdf-toolbox/issues">Request Feature</a>
    </li>
  </ul>
</ol>
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#known-issues">Known Issues</a></li>
        <li><a href="#comparison-scores">Comparison Scores</a></li>
      </ul>
    </li>
    <!-- <li><a href="#usage">Usage</a></li> -->
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <!-- <li><a href="#acknowledgments">Acknowledgments</a></li> -->
  </ol>
</details>

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Python3](https://www.python.org/)
* [PyMuPDF](https://github.com/pymupdf/PyMuPDF)
* [PyTesseract](https://github.com/madmaze/pytesseract)
* [Adobe PDF Extract API](https://developer.adobe.com/document-services/apis/pdf-extract/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* **Adobe**
  * Place `Adobe PDF Extract API` credentials in root of repository. Credentials are available from [Adobe](https://developer.adobe.com/document-services/apis/pdf-extract/) with a 1000 credit/six month free trial.
* **Pillow/PIL**
  * Install `Python Imaging Library` (or the `Pillow fork`) for your OS
* **TesseractOCR**
  * Install `Tesseract OCR` for your OS.
* **MuPDF**
  * Install `MuPDF` for your OS.

### Installation

1. Get a free API Key/Credentials at [Adobe](https://developer.adobe.com/document-services/apis/pdf-extract/).
2. Clone the repo
    ```sh
    git clone https://github.com/hreikin/pdf-toolbox.git
    ```
3. Create and source a Python virtual environment.
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```
4. Install requirements with `pip`
    ```sh
    pip install -r requirements.txt
    ```



### Known Issues
On Linux (Windows/Mac untested) the file `.venv/lib64/python3.9/site-packages/ado
be/pdfservices/operation/internal/io/file_ref_impl.py` from `pdfservices-sdk` 
inside the `venv` you create needs a few changes otherwise it might fail with a 
false `cross-device link` error.

Add `import shutil` to the top of the file and on line 46 alter it to the 
following to successfully save the JsonSchema/zip file it outputs. This does not 
deal with deleting the temporary file as it only copies it however with it being 
in temp it should be deleted on a reboot anyway so for now this hacky workaround 
should be ok:

```python
shutil.copy(self._file_path, abs_path)
```

### Comparison Scores
The file `confidence.py` creates three text files for comparison to create a 
rudimentary confidence check as one isn't provided by the API. The score is a 
comparison between the API's extraction and other extraction techniques. Scores 
are calculated using the `SequenceMatcher` class and `get_close_matches` method 
from `difflib`. 

A score of **0.6** for any of the calculated scores is considered a close match. 
All scores are stored in a dictionary and a text file is created with the 
results.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
<!-- ## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p> -->



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/hreikin/pdf-toolbox/issues) for a full list of proposed features (and known issues).

<!-- **Related Issues** -->

- [ ] [Database](https://github.com/hreikin/pdf-toolbox/issues/2)
- [ ] [Extraction](https://github.com/hreikin/pdf-toolbox/issues/3)
- [x] [Comparison Score](https://github.com/hreikin/pdf-toolbox/issues/4)
- [ ] [Conversion](https://github.com/hreikin/pdf-toolbox/issues/5)
- [ ] [Creation](https://github.com/hreikin/pdf-toolbox/issues/6)
- [ ] [Merge & Combine](https://github.com/hreikin/pdf-toolbox/issues/7)
- [ ] [GUI](https://github.com/hreikin/pdf-toolbox/issues/11) 


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Personal Website: [https://hreikin.co.uk](https://hreikin.co.uk)

Project Link: [https://github.com/hreikin/pdf-toolbox](https://github.com/hreikin/pdf-toolbox)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
<!-- ## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#top">back to top</a>)</p> -->



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/hreikin/pdf-toolbox.svg?style=for-the-badge
[contributors-url]: https://github.com/hreikin/pdf-toolbox/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/hreikin/pdf-toolbox.svg?style=for-the-badge
[forks-url]: https://github.com/hreikin/pdf-toolbox/network/members
[stars-shield]: https://img.shields.io/github/stars/hreikin/pdf-toolbox.svg?style=for-the-badge
[stars-url]: https://github.com/hreikin/pdf-toolbox/stargazers
[issues-shield]: https://img.shields.io/github/issues/hreikin/pdf-toolbox.svg?style=for-the-badge
[issues-url]: https://github.com/hreikin/pdf-toolbox/issues
[license-shield]: https://img.shields.io/github/license/hreikin/pdf-toolbox.svg?style=for-the-badge
[license-url]: https://github.com/hreikin/pdf-toolbox/blob/master/LICENSE.txt
[commit-shield]: https://img.shields.io/github/commit-activity/m/hreikin/pdf-toolbox?style=for-the-badge
[commit-url]: https://github.com/hreikin/pdf-toolbox/graphs/commit-activity
<!-- [linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555 -->
<!-- [linkedin-url]: https://linkedin.com/in/linkedin_username -->
<!-- [product-screenshot]: images/screenshot.png -->
