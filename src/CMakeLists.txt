cmake_minimum_required(VERSION 3.10)
project(COMPAS)

# Set C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find required packages
find_package(Boost REQUIRED COMPONENTS filesystem program_options system)
find_package(HDF5 REQUIRED COMPONENTS CXX HL)
find_package(GSL REQUIRED)

# Add your source files
set(SOURCES
    profiling.cpp utils.cpp yaml.cpp vector3d.cpp
    Rand.cpp Options.cpp Log.cpp Errors.cpp
    BaseStar.cpp Star.cpp
    MainSequence.cpp MS_lte_07.cpp MS_gt_07.cpp
    CH.cpp
    GiantBranch.cpp HG.cpp FGB.cpp CHeB.cpp EAGB.cpp TPAGB.cpp
    HeMS.cpp HeHG.cpp HeGB.cpp
    Remnants.cpp
    WhiteDwarfs.cpp HeWD.cpp COWD.cpp ONeWD.cpp
    NS.cpp BH.cpp MR.cpp
    BinaryConstituentStar.cpp BaseBinaryStar.cpp BinaryStar.cpp
    main.cpp
)

# Create the executable
add_executable(${PROJECT_NAME} ${SOURCES})

# Include directories
target_include_directories(${PROJECT_NAME} PRIVATE
    ${Boost_INCLUDE_DIRS}
    ${HDF5_INCLUDE_DIRS}
    ${GSL_INCLUDE_DIRS}
)

# Link libraries
target_link_libraries(${PROJECT_NAME} PRIVATE
    ${Boost_LIBRARIES}
    ${HDF5_LIBRARIES}
    ${GSL_LIBRARIES}
    m z dl pthread
)

# Optimization flags
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_options(${PROJECT_NAME} PRIVATE -O3 -march=native)
endif()

# Static build option
option(BUILD_STATIC "Build static executable" OFF)
if(BUILD_STATIC)
    set_target_properties(${PROJECT_NAME} PROPERTIES LINK_FLAGS "-static")
endif()