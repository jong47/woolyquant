#include <iostream>
#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

// sampleSize cannot be negative, otherwise covariance will not work.
// NOTE: The returnPrice should not exceed the sampleSize since the total volume should be the same
//
// returnPriceA
// returnPriceB
// averagePriceA
// averagePriceB

// class stockPair {
//     private:
//         u_int16_t sampleSize;
//         std::vector<double> returnPriceA;
//         std::vector<double> returnPriceB;
//         double averagePriceA;
//         double averagePriceB;
//     public:
//         stockPair(){}
//         stockPair(u_int16_t sampleSize, double returnPriceA[], double returnPriceB[], double averagePriceA, double averagePriceB) {
//             this->sampleSize = sampleSize;

//             for (int i = 0; i < sampleSize; i++) {
//                 this->returnPriceA.insert(this->returnPriceA.begin(), returnPriceA[i]);
                
//             }

//             this->averagePriceA = averagePriceA;
//             this->averagePriceB = averagePriceB;
//         }
// };

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

// int main(void) {
    
    
//     return 0;   
// }