cmake_minimum_required(VERSION 3.10)

project(planar_arm_physics_sim LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(
    planar_arm_physics_sim
    src/cpp/main.cpp
)