from conans import ConanFile, CMake, tools


class FastCDRConan(ConanFile):
    name = "foonathan-memory"
    version = "1.0.0"
    license = "Apache License 2.0"
    author = "Frieder Pankratz"
    url = "https://github.com/TUM-CONAN/conan-foonathan-memory.git"
    description = "Conan wrapper for foonathan-memory"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [False]}
    default_options = {"shared": False}
    generators = "cmake"

    def source(self):        
        git = tools.Git()        
        git.clone("https://github.com/FriederPankratz/memory.git", self.version)
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("CMakeLists.txt", "project(FOONATHAN_MEMORY)",
                              '''project(FOONATHAN_MEMORY)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.verbose = True

        def add_cmake_option(option, value):
            var_name = "{}".format(option).upper()
            value_str = "{}".format(value)
            var_value = "ON" if value_str == 'True' else "OFF" if value_str == 'False' else value_str
            cmake.definitions[var_name] = var_value

        for option, value in self.options.items():
            add_cmake_option(option, value)

        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
    
            

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

