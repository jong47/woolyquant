#include <iostream>
#include <array>
#include <cmath>
#include <omp.h>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

float calculateCovariance(u_int32_t sampleSize, pybind11::array_t<float> returnPercentA, pybind11::array_t<float> returnPercentB, float averagePercentA, float averagePercentB) {
    // Get buffer info for returnPercentA
    pybind11::buffer_info bufA = returnPercentA.request();
    float* ptrA = static_cast<float*>(bufA.ptr);

    // Get buffer info for returnPercentB
    pybind11::buffer_info bufB = returnPercentB.request();
    float* ptrB = static_cast<float*>(bufB.ptr);

    // Divides loop iterations across multiple threads for sigma
    float sigma = 0.0f;
    #pragma omp parallel for reduction(+:sigma)
    
    for (u_int32_t i = 1; i < sampleSize; i++) {
        float percentA = ptrA[i];
        float percentB = ptrB[i];

        sigma += ((percentA - averagePercentA) * (percentB - averagePercentB));
    }

    return (sigma / (sampleSize - 1));
}

float calculateAverageSpread(u_int32_t sampleSize, pybind11::array_t<float> returnPricesA, pybind11::array_t<float> returnPricesB) {
    auto ptrA = static_cast<const float*>(returnPricesA.data());
    auto ptrB = static_cast<const float*>(returnPricesB.data());

    // Divides loop iterations across multiple threads for spread
    float spread = 0.00f;
    #pragma omp parallel for reduction(+:spread)

    for (u_int32_t i = 0; i < sampleSize; i++) {
        spread += std::abs(std::abs(ptrA[i]) - std::abs(ptrB[i]));
    }

    float averageSpread = spread / static_cast<float>(sampleSize);
    return averageSpread;
}

// pybind11::list generateStockPairs(pybind11::array_t<float> leftEquity, pybind11::array_t<float> rightEquity) {

// }

PYBIND11_MODULE(stock_pair, stock_pair) {
    stock_pair.doc() = "pybind11 plugin to speed up calculations for Covariance, Correlation, and Cointegration.";
    stock_pair.def("calculateCovariance", &calculateCovariance, "A function which calculates the covariance between two stocks");
    stock_pair.def("calculateAverageSpread", &calculateAverageSpread, "Function to calculate the average spread price over a time series between two stocks");
    // stock_pair.def("generateStockPairs", &generateStockPairs, "Takes in ");
}