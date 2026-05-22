# Laser Cavity Gain Simulation Suite

[![DOI](https://img.shields.io/badge/DOI-10.13140%2FRG.2.2.29126.18241-blue)](https://doi.org/10.13140/RG.2.2.29126.18241)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

An open-source scientific computing suite designed to model, simplify, and analyze the threshold condition and optical gain of resonant laser cavities. This project connects advanced calculus Taylor series expansions with cross-platform engineering applications tailored for advanced metallurgical manufacturing processes such as Selective Laser Melting (SLM) and Direct Metal Laser Sintering (DMLS).

## 🌐 Academic & Professional Profiles

You can find my complete research portfolio, CAD designs, philosophical papers, and professional network here:

[![ResearchGate](https://img.shields.io/badge/ResearchGate-00CCBB?style=for-the-badge&logo=ResearchGate&logoColor=white)](https://www.researchgate.net/profile/Dario_De_Santiago_Sasinka)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/dariodesantiagosasinka/)
[![GrabCAD](https://img.shields.io/badge/GrabCAD-FF4444?style=for-the-badge&logo=GrabCAD&logoColor=white)](https://grabcad.com/dario.de.santiago-2)
[![PhilPeople](https://img.shields.io/badge/PhilPeople-412991?style=for-the-badge&logo=academia&logoColor=white)](https://philpeople.org/profiles/dario-ricardo-de-santiago-sasinka)
[![Zenodo](https://img.shields.io/badge/Zenodo-168294?style=for-the-badge&logo=zenodo&logoColor=white)](https://zenodo.org/deposit)
[![ORCID](https://img.shields.io/badge/ORCID-A6CE39?style=for-the-badge&logo=orcid&logoColor=white)](https://orcid.org/0000-0002-7684-9532)

## 📄 Project Structure

The repository is organized as follows:

* **`docs/`**: Technical papers, academic reports, and schematic assets.
    * `GananciaLASER_SeriesNumericas_v3.tex`: Official Spanish manuscript (UTN-FRC).
    * `GainLASER_NumericSeries_v3.tex`: Official English translation.
    * `GananciaLASER_SeriesNumericas_v3.pdf`: Compiled physical production report.
    * `img/`: Vector and high-resolution schematics (cavity configurations, energy levels, and emission charts).
* **`src/`**: Cross-verified numerical engines and source code.
    * `cpp/`: Modular native hardware library (`laser_cavity.hpp` and `example.cpp`) for low-level industrial integration.
    * `octave/`: Vectorized numerical matrix functions (`laser_cavity.m`) for rapid parametric sweep modeling in Octave/MATLAB.
    * `python/`: Interactive CLI application (`laser_calculator.py`) with real-time error analysis and Windows API ANSI support.
    * `web/`: Complete dynamic web UI engine dashboard (`laser_calculator.html`) with SVG beam visualization and canvas plotting.

## 🛠️ Quick Start

### Python CLI Terminal Engine
```bash
python src/python/laser_calculator.py