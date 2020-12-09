import os
from conans import ConanFile, CMake, tools

class PpconsulConan(ConanFile):
    name = "ppconsul"
    version = "v0.2.1"
    license = "Boost Software License 1.0"
    author = "oliora"
    url = "https://github.com/oliora/ppconsul"
    description = "A C++ client library for Consul. Consul is a distributed tool for discovering and configuring services in your infrastructure."
    topics = ("Consul")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
    }
    default_options = {
        "shared": False,
        "libcurl:shared": True
    }
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/oliora/ppconsul.git")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("ppconsul/CMakeLists.txt", "project(Ppconsul VERSION 0.1)",
                              '''project(Ppconsul VERSION 0.1)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="ppconsul")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="ppconsul")
        self.copy("*ppconsul.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["ppconsul"]
        self.cpp_info.includedirs.append(os.path.join("include", "ppconsul"))

    def requirements(self):
        self.requires("boost/[>1.55]")
        self.requires("libcurl/[>7.00]")