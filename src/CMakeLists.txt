cmake_minimum_required(VERSION 3.4)
project(smart-pair)
add_subdirectory(build)
pybind11_add_module(stock_pair stock_pair.cc)

