#include <iostream>
#include <array>
#include <cmath>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

float calculateCovariance(u_int16_t sampleSize, pybind11::array_t<float> returnPercentA, pybind11::array_t<float> returnPercentB, float averagePercentA, float averagePercentB) {
    // Get buffer info for returnPercentA
    pybind11::buffer_info bufA = returnPercentA.request();
    float* ptrA = static_cast<float*>(bufA.ptr);

    // Get buffer info for returnPercentB
    pybind11::buffer_info bufB = returnPercentB.request();
    float* ptrB = static_cast<float*>(bufB.ptr);

    float sigma = 0.0f;

    for (u_int16_t i = 1; i < sampleSize; i++) {
        float percentA = ptrA[i];
        float percentB = ptrB[i];

        sigma += ((percentA - averagePercentA) * (percentB - averagePercentB));
    }

    return (sigma / (sampleSize - 1));
}

float calculateAverageSpread(u_int16_t sampleSize, pybind11::array_t<float> returnPricesA, pybind11::array_t<float> returnPricesB) {
    auto ptrA = static_cast<const float*>(returnPricesA.data());
    auto ptrB = static_cast<const float*>(returnPricesB.data());

    float spread = 0.00f;
    for (int i = 0; i < sampleSize; i++) {
        spread += std::abs(std::abs(ptrA[i]) - std::abs(ptrB[i]));
    }

    float averageSpread = spread / static_cast<float>(sampleSize);
    return averageSpread;
}

PYBIND11_MODULE(stock_pair, stock_pair) {
    stock_pair.doc() = "pybind11 plugin to speed up calculations for Covariance, Correlation, and Cointegration.";
    stock_pair.def("calculateCovariance", &calculateCovariance, "A function which calculates the covariance between two stocks");
    stock_pair.def("calculateAverageSpread", &calculateAverageSpread, "Function to calculate the average spread price over a time series between two stocks");
}