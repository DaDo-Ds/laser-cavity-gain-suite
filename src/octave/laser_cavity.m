% LASER_CAVITY - Funciones para cálculo de ganancia umbral en cavidades Fabry-Pérot
% Autor: Darío Ricardo de Santiago Sasinka
% DOI: 10.13140/RG.2.2.29126.18241
% Licencia: CC BY 4.0
%
% Uso típico:
%   [alpha_lin, alpha_exact, x, rel_err] = threshold_gain(10, 0.99, 0.95, 0);
%   F = finesse(0.99, 0.95);
%   fr = fsr(10, 1.82);
%   T = series_terms(0.003, 10, 8);

function [alpha_lin, alpha_exact, x, rel_err] = threshold_gain(L, R1, R2, loss_pct)
% threshold_gain - Calcula la ganancia umbral lineal y exacta
%   L       : longitud de cavidad [cm]
%   R1, R2  : reflectividades de los espejos [fracción]
%   loss_pct: pérdidas internas por paso [%]
%   alpha_lin : ganancia aproximada (Taylor 1er orden) [cm^-1]
%   alpha_exact: ganancia exacta (ecuación trascendental) [cm^-1]
%   x       : parámetro 2*alpha_lin*L
%   rel_err : error relativo de truncamiento [%]
    loss = loss_pct / 100;
    r1e = R1 * (1 - loss);
    r2e = R2 * (1 - loss);
    prod_ef = r1e * r2e;

    alpha_lin = (1 - prod_ef) / (2 * L);
    if prod_ef > 0
        alpha_exact = -log(prod_ef) / (2 * L);
    else
        alpha_exact = Inf;
    end

    x = 2 * alpha_lin * L;
    exact_val = exp(-x);
    approx_val = 1 - x;
    if exact_val > 1e-15
        rel_err = abs(exact_val - approx_val) / exact_val * 100;
    else
        rel_err = Inf;
    end
end

function f = finesse(R1, R2)
% finesse - Calcula la finesse de la cavidad (espejos sin pérdidas)
    producto = R1 * R2;
    if producto >= 1.0
        f = Inf;
    else
        f = pi * sqrt(producto) / (1 - producto);
    end
end

function fr = fsr(L, n)
% fsr - Free Spectral Range en GHz
%   L [cm], n índice de refracción
    c = 2.998e10;  % cm/s
    fr = c / (2 * n * L * 1e9);
end

function T = series_terms(alpha, L, N)
% series_terms - Tabla de convergencia de la serie de Taylor
%   alpha [cm^-1], L [cm], N número de términos (máx 15)
%   Devuelve matriz de (N x 5): [n, término, suma_parcial, exacto, error%]
    x = 2 * alpha * L;
    exact = exp(-x);
    partial = 0;
    factorial = 1;
    T = zeros(N, 5);
    for n = 0:N-1
        if n > 0
            factorial = factorial * n;
        end
        term = (-x)^n / factorial;
        partial = partial + term;
        if abs(exact) > 1e-15
            err = abs(partial - exact) / abs(exact) * 100;
        else
            err = 0;
        end
        T(n+1,:) = [n, term, partial, exact, err];
    end
end

% Ejemplo de uso interactivo (si se ejecuta el script directamente)
if ~nargin
    printf("\n=== LASER CAVITY CALCULATOR (Octave) ===\n");
    printf("DOI: 10.13140/RG.2.2.29126.18241\n");
    L   = input("Longitud L [cm] (default 10): ");
    if isempty(L), L = 10; end
    R1  = input("Reflectividad R₁ [%] (default 99): ");
    if isempty(R1), R1 = 99; else R1 = R1/100; end
    R2  = input("Reflectividad R₂ [%] (default 95): ");
    if isempty(R2), R2 = 95; else R2 = R2/100; end
    loss = input("Pérdidas por paso [%] (default 0): ");
    if isempty(loss), loss = 0; end
    n   = input("Índice de refracción (default 1.82): ");
    if isempty(n), n = 1.82; end

    [a_lin, a_ex, xv, err_rel] = threshold_gain(L, R1, R2, loss);
    F = finesse(R1, R2);
    fr = fsr(L, n);
    opt_path = 2 * n * L;  % cm
    fprintf("\nResultados:\n");
    fprintf("  αc (lineal)   = %.6e cm⁻¹\n", a_lin);
    fprintf("  αc (exacta)   = %.6e cm⁻¹\n", a_ex);
    fprintf("  2αL           = %.6f\n", xv);
    fprintf("  Error         = %.4f %%\n", err_rel);
    if xv < 0.1
        fprintf("  Validez       = ✓ VÁLIDA (error < 0.5%%)\n");
    elseif xv < 0.5
        fprintf("  Validez       = ⚠ MARGINAL\n");
    else
        fprintf("  Validez       = ✗ INVÁLIDA, usar ec. exacta\n");
    end
    fprintf("  Finesse       = %.2f\n", F);
    fprintf("  FSR           = %.4f GHz\n", fr);
    fprintf("  Long. óptica  = %.2f µm\n", opt_path * 1e4);
end