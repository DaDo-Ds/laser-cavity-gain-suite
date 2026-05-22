# Suite de Simulación de Ganancia de Cavidad LÁSER

[![DOI](https://img.shields.io/badge/DOI-10.13140%2FRG.2.2.29126.18241-blue)](https://doi.org/10.13140/RG.2.2.29126.18241)
[![Licencia: CC BY 4.0](https://img.shields.io/badge/Licencia-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/deed.es)

Una suite de computación científica de código abierto diseñada para modelar, simplificar y analizar la condición de umbral y la ganancia óptica de cavidades resonantes láser lineales. Este proyecto conecta desarrollos en series de Taylor de cálculo avanzado con aplicaciones de ingeniería multiplataforma, adaptadas a procesos metalúrgicos de manufactura avanzada como el Sinterizado Selectivo por Láser (SLM) y el Sinterizado Láser Directo de Metales (DMLS).

## 🌐 Perfiles Académicos y Profesionales

Podés encontrar mi portafolio completo de diseños CAD, preprints científicos, artículos filosóficos y redes profesionales acá:

[![ResearchGate](https://img.shields.io/badge/ResearchGate-00CCBB?style=for-the-badge&logo=ResearchGate&logoColor=white)](https://www.researchgate.net/profile/Dario_De_Santiago_Sasinka)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/dariodesantiagosasinka/)
[![GrabCAD](https://img.shields.io/badge/GrabCAD-FF4444?style=for-the-badge&logo=GrabCAD&logoColor=white)](https://grabcad.com/dario.de.santiago-2)
[![PhilPeople](https://img.shields.io/badge/PhilPeople-412991?style=for-the-badge&logo=academia&logoColor=white)](https://philpeople.org/profiles/dario-ricardo-de-santiago-sasinka)
[![Zenodo](https://img.shields.io/badge/Zenodo-168294?style=for-the-badge&logo=zenodo&logoColor=white)](https://zenodo.org/deposit)
[![ORCID](https://img.shields.io/badge/ORCID-A6CE39?style=for-the-badge&logo=orcid&logoColor=white)](https://orcid.org/0000-0002-7684-9532)

## 📄 Estructura del Proyecto

El repositorio está organizado de la siguiente manera:

* **`docs/`**: Artículos técnicos, reportes académicos y recursos esquemáticos.
    * `GananciaLASER_SeriesNumericas_v3.tex`: Manuscrito oficial en español (UTN-FRC).
    * `GainLASER_NumericSeries_v3.tex`: Traducción oficial al inglés.
    * `GananciaLASER_SeriesNumericas_v3.pdf`: Reporte técnico final compilado.
    * `img/`: Esquemas vectoriales y de alta resolución (configuraciones de cavidad, niveles de energía y diagramas de emisión).
* **`src/`**: Motores numéricos de verificación cruzada y código fuente.
    * `cpp/`: Librería de hardware nativa y modular (`laser_cavity.hpp` y `example.cpp`) para integración industrial de bajo nivel.
    * `octave/`: Funciones numéricas matriciales vectorizadas (`laser_cavity.m`) para modelado rápido de barridos paramétricos en Octave/MATLAB.
    * `python/`: Aplicación interactiva de consola (`laser_calculator.py`) con análisis de error en tiempo real y soporte ANSI para la API de Windows.
    * `web/`: Dashboard web dinámico (`laser_calculator.html`) con visualización de haz en SVG y gráficos en Canvas.

## 🛠️ Inicio Rápido

### Motor de Consola en Python (CLI)
```bash
python src/python/laser_calculator.py