/**
 * @file laser_cavity.hpp
 * @brief Funciones para cálculo de ganancia umbral en cavidades láser Fabry-Pérot.
 * @author Darío Ricardo de Santiago Sasinka
 * @license CC BY 4.0
 * @see DOI: 10.13140/RG.2.2.29126.18241
 * 
 * Este archivo es header-only. Inclúyalo en su proyecto y use las funciones.
 * Ejemplo:
 *   #include "laser_cavity.hpp"
 *   auto [alpha_lin, alpha_exact, x, rel_err] = threshold_gain(10.0, 0.99, 0.95, 0.0);
 */

#ifndef LASER_CAVITY_HPP
#define LASER_CAVITY_HPP

#include <cmath>
#include <vector>
#include <tuple>
#include <limits>

namespace lasercavity {

constexpr double C_LIGHT = 2.998e10;   // cm/s

/**
 * @brief Calcula la ganancia umbral (lineal y exacta).
 * @param L Longitud de cavidad [cm]
 * @param R1 Reflectividad espejo posterior (0..1)
 * @param R2 Reflectividad acoplador salida (0..1)
 * @param loss_pct Pérdidas internas por paso [%]
 * @return Tupla (alpha_lin, alpha_exact, x, rel_err)
 */
inline std::tuple<double, double, double, double>
threshold_gain(double L, double R1, double R2, double loss_pct = 0.0) {
    double loss = loss_pct / 100.0;
    double r1e = R1 * (1.0 - loss);
    double r2e = R2 * (1.0 - loss);
    double prod_ef = r1e * r2e;

    double alpha_lin = (1.0 - prod_ef) / (2.0 * L);
    double alpha_exact = (prod_ef > 0.0) ? -std::log(prod_ef) / (2.0 * L)
                                         : std::numeric_limits<double>::infinity();

    double x = 2.0 * alpha_lin * L;
    double exact_val = std::exp(-x);
    double approx_val = 1.0 - x;
    double rel_err = (exact_val > 1e-15) ? std::abs(exact_val - approx_val) / exact_val * 100.0
                                         : std::numeric_limits<double>::infinity();
    return {alpha_lin, alpha_exact, x, rel_err};
}

/**
 * @brief Calcula el Free Spectral Range en GHz.
 */
inline double fsr(double L, double n) {
    return C_LIGHT / (2.0 * n * L * 1e9);
}

/**
 * @brief Calcula la finesse de la cavidad (sin pérdidas internas).
 */
inline double finesse(double R1, double R2) {
    double producto = R1 * R2;
    if (producto >= 1.0) return std::numeric_limits<double>::infinity();
    return M_PI * std::sqrt(producto) / (1.0 - producto);
}

/**
 * @brief Calcula la longitud óptica de ida y vuelta [µm].
 */
inline double roundtrip_optical_path(double L, double n) {
    return 2.0 * n * L * 1e4;   // cm → µm
}

/**
 * @brief Calcula la tabla de convergencia de la serie de Taylor.
 * @return vector de tuplas (n, término, suma_parcial, exacto, error_porcentual)
 */
inline std::vector<std::tuple<int, double, double, double, double>>
series_terms(double alpha, double L, int N) {
    double x = 2.0 * alpha * L;
    double exact = std::exp(-x);
    double partial = 0.0;
    double factorial = 1.0;
    std::vector<std::tuple<int, double, double, double, double>> table;
    for (int n = 0; n < N; ++n) {
        if (n > 0) factorial *= n;
        double term = std::pow(-x, n) / factorial;
        partial += term;
        double err = (std::abs(exact) > 1e-15) ? std::abs(partial - exact) / std::abs(exact) * 100.0 : 0.0;
        table.emplace_back(n, term, partial, exact, err);
    }
    return table;
}

} // namespace lasercavity

#endif // LASER_CAVITY_HPP