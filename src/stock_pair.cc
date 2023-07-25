#include <iostream>
#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

float calculateCovariance(u_int16_t sampleSize, pybind11::array_t<float> returnPricesA, pybind11::array_t<float> returnPricesB, float averagePriceA, float averagePriceB) {
    // Get buffer info for returnPricesA
    pybind11::buffer_info bufA = returnPricesA.request();
    float* ptrA = static_cast<float*>(bufA.ptr);

    // Get buffer info for returnPricesB
    pybind11::buffer_info bufB = returnPricesB.request();
    float* ptrB = static_cast<float*>(bufB.ptr);

    float sigma = 0.0f;

    for (int i = 1; i < sampleSize; i++) {
        // Access A array data
        float priceA = ptrA[i];
        // Access B array data 
        float priceB = ptrB[i];

        sigma += ((priceA - averagePriceA) * (priceB - averagePriceB));
    }

    // Cleanup 
    // returnPricesA.request().ptr = nullptr;
    // returnPricesB.request().ptr = nullptr;

    float covariance = sigma / (sampleSize - 1);
    sigma = 0.00f;
    return covariance;
}

PYBIND11_MODULE(stock_pair, stock_pair) {
    stock_pair.doc() = "pybind11 plugin to speed up calculations for Covariance, Correlation, and Cointegration.";
    stock_pair.def("calculateCovariance", &calculateCovariance, "A function which calculates the covariance between two stocks");
}