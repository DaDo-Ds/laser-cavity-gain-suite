#include <iostream>
#include <iomanip>
#include "laser_cavity.hpp"

int main() {
    using namespace lasercavity;

    // Parámetros de ejemplo
    double L = 10.0;      // cm
    double R1 = 0.99;
    double R2 = 0.95;
    double loss = 0.0;    // %
    double n = 1.82;      // índice refracción (Nd:YAG)

    auto [alpha_lin, alpha_exact, x, rel_err] = threshold_gain(L, R1, R2, loss);
    double F = finesse(R1, R2);
    double fr = fsr(L, n);
    double opt_path = roundtrip_optical_path(L, n);

    std::cout << std::fixed << std::setprecision(6);
    std::cout << "=== LASER CAVITY CALCULATOR (C++) ===" << std::endl;
    std::cout << "DOI: 10.13140/RG.2.2.29126.18241\n" << std::endl;
    std::cout << "Parámetros:" << std::endl;
    std::cout << "  L     = " << L << " cm" << std::endl;
    std::cout << "  R₁    = " << R1 * 100 << " %" << std::endl;
    std::cout << "  R₂    = " << R2 * 100 << " %" << std::endl;
    std::cout << "  loss  = " << loss << " %/pass" << std::endl;
    std::cout << "  n     = " << n << std::endl;
    std::cout << "\nResultados:" << std::endl;
    std::cout << "  αc (lineal)   = " << alpha_lin << " cm⁻¹" << std::endl;
    std::cout << "  αc (exacta)   = " << alpha_exact << " cm⁻¹" << std::endl;
    std::cout << "  2αL           = " << x << std::endl;
    std::cout << "  Error         = " << rel_err << " %" << std::endl;
    if (x < 0.1)
        std::cout << "  Validez       = ✓ VÁLIDA (error < 0.5%)" << std::endl;
    else if (x < 0.5)
        std::cout << "  Validez       = ⚠ MARGINAL" << std::endl;
    else
        std::cout << "  Validez       = ✗ INVÁLIDA, usar ec. exacta" << std::endl;
    std::cout << "  Finesse       = " << F << std::endl;
    std::cout << "  FSR           = " << fr << " GHz" << std::endl;
    std::cout << "  Long. óptica  = " << opt_path << " µm" << std::endl;

    // Tabla de convergencia de la serie
    std::cout << "\n--- Convergencia de la serie de Taylor ---" << std::endl;
    double alpha_series = 0.003;   // cm⁻¹
    int N = 8;
    auto table = series_terms(alpha_series, L, N);
    std::cout << "  n      Término            Suma parcial        Exacto              Error %" << std::endl;
    for (const auto& [n, term, partial, exact, err] : table) {
        std::cout << std::setw(4) << n << "   "
                  << std::scientific << std::setprecision(6) << term << "   "
                  << std::fixed << std::setprecision(8) << partial << "   "
                  << exact << "   " << err << " %" << std::endl;
    }

    return 0;
}