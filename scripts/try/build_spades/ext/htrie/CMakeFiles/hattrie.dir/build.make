# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.12

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /home/sg461/anaconda3/lib/python3.6/site-packages/cmake/data/bin/cmake

# The command to remove a file.
RM = /home/sg461/anaconda3/lib/python3.6/site-packages/cmake/data/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades

# Include any dependencies generated for this target.
include ext/htrie/CMakeFiles/hattrie.dir/depend.make

# Include the progress variables for this target.
include ext/htrie/CMakeFiles/hattrie.dir/progress.make

# Include the compile flags for this target's objects.
include ext/htrie/CMakeFiles/hattrie.dir/flags.make

ext/htrie/CMakeFiles/hattrie.dir/ahtable.c.o: ext/htrie/CMakeFiles/hattrie.dir/flags.make
ext/htrie/CMakeFiles/hattrie.dir/ahtable.c.o: /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/ext/src/htrie/ahtable.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object ext/htrie/CMakeFiles/hattrie.dir/ahtable.c.o"
	cd /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/ext/htrie && /home/sg461/anaconda3/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/hattrie.dir/ahtable.c.o   -c /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/ext/src/htrie/ahtable.c

ext/htrie/CMakeFiles/hattrie.dir/ahtable.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/hattrie.dir/ahtable.c.i"
	cd /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/ext/htrie && /home/sg461/anaconda3/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/ext/src/htrie/ahtable.c > CMakeFiles/hattrie.dir/ahtable.c.i

ext/htrie/CMakeFiles/hattrie.dir/ahtable.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/hattrie.dir/ahtable.c.s"
	cd /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/ext/htrie && /home/sg461/anaconda3/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/ext/src/htrie/ahtable.c -o CMakeFiles/hattrie.dir/ahtable.c.s

ext/htrie/CMakeFiles/hattrie.dir/hat-trie.c.o: ext/htrie/CMakeFiles/hattrie.dir/flags.make
ext/htrie/CMakeFiles/hattrie.dir/hat-trie.c.o: /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/ext/src/htrie/hat-trie.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building C object ext/htrie/CMakeFiles/hattrie.dir/hat-trie.c.o"
	cd /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/ext/htrie && /home/sg461/anaconda3/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/hattrie.dir/hat-trie.c.o   -c /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/ext/src/htrie/hat-trie.c

ext/htrie/CMakeFiles/hattrie.dir/hat-trie.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/hattrie.dir/hat-trie.c.i"
	cd /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/ext/htrie && /home/sg461/anaconda3/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/ext/src/htrie/hat-trie.c > CMakeFiles/hattrie.dir/hat-trie.c.i

ext/htrie/CMakeFiles/hattrie.dir/hat-trie.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/hattrie.dir/hat-trie.c.s"
	cd /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/ext/htrie && /home/sg461/anaconda3/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/ext/src/htrie/hat-trie.c -o CMakeFiles/hattrie.dir/hat-trie.c.s

ext/htrie/CMakeFiles/hattrie.dir/misc.c.o: ext/htrie/CMakeFiles/hattrie.dir/flags.make
ext/htrie/CMakeFiles/hattrie.dir/misc.c.o: /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/ext/src/htrie/misc.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building C object ext/htrie/CMakeFiles/hattrie.dir/misc.c.o"
	cd /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/ext/htrie && /home/sg461/anaconda3/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/hattrie.dir/misc.c.o   -c /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/ext/src/htrie/misc.c

ext/htrie/CMakeFiles/hattrie.dir/misc.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/hattrie.dir/misc.c.i"
	cd /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/ext/htrie && /home/sg461/anaconda3/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/ext/src/htrie/misc.c > CMakeFiles/hattrie.dir/misc.c.i

ext/htrie/CMakeFiles/hattrie.dir/misc.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/hattrie.dir/misc.c.s"
	cd /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/ext/htrie && /home/sg461/anaconda3/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/ext/src/htrie/misc.c -o CMakeFiles/hattrie.dir/misc.c.s

ext/htrie/CMakeFiles/hattrie.dir/murmurhash3.c.o: ext/htrie/CMakeFiles/hattrie.dir/flags.make
ext/htrie/CMakeFiles/hattrie.dir/murmurhash3.c.o: /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/ext/src/htrie/murmurhash3.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building C object ext/htrie/CMakeFiles/hattrie.dir/murmurhash3.c.o"
	cd /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/ext/htrie && /home/sg461/anaconda3/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/hattrie.dir/murmurhash3.c.o   -c /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/ext/src/htrie/murmurhash3.c

ext/htrie/CMakeFiles/hattrie.dir/murmurhash3.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/hattrie.dir/murmurhash3.c.i"
	cd /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/ext/htrie && /home/sg461/anaconda3/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/ext/src/htrie/murmurhash3.c > CMakeFiles/hattrie.dir/murmurhash3.c.i

ext/htrie/CMakeFiles/hattrie.dir/murmurhash3.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/hattrie.dir/murmurhash3.c.s"
	cd /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/ext/htrie && /home/sg461/anaconda3/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/ext/src/htrie/murmurhash3.c -o CMakeFiles/hattrie.dir/murmurhash3.c.s

# Object files for target hattrie
hattrie_OBJECTS = \
"CMakeFiles/hattrie.dir/ahtable.c.o" \
"CMakeFiles/hattrie.dir/hat-trie.c.o" \
"CMakeFiles/hattrie.dir/misc.c.o" \
"CMakeFiles/hattrie.dir/murmurhash3.c.o"

# External object files for target hattrie
hattrie_EXTERNAL_OBJECTS =

ext/htrie/libhattrie.a: ext/htrie/CMakeFiles/hattrie.dir/ahtable.c.o
ext/htrie/libhattrie.a: ext/htrie/CMakeFiles/hattrie.dir/hat-trie.c.o
ext/htrie/libhattrie.a: ext/htrie/CMakeFiles/hattrie.dir/misc.c.o
ext/htrie/libhattrie.a: ext/htrie/CMakeFiles/hattrie.dir/murmurhash3.c.o
ext/htrie/libhattrie.a: ext/htrie/CMakeFiles/hattrie.dir/build.make
ext/htrie/libhattrie.a: ext/htrie/CMakeFiles/hattrie.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Linking C static library libhattrie.a"
	cd /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/ext/htrie && $(CMAKE_COMMAND) -P CMakeFiles/hattrie.dir/cmake_clean_target.cmake
	cd /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/ext/htrie && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/hattrie.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
ext/htrie/CMakeFiles/hattrie.dir/build: ext/htrie/libhattrie.a

.PHONY : ext/htrie/CMakeFiles/hattrie.dir/build

ext/htrie/CMakeFiles/hattrie.dir/clean:
	cd /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/ext/htrie && $(CMAKE_COMMAND) -P CMakeFiles/hattrie.dir/cmake_clean.cmake
.PHONY : ext/htrie/CMakeFiles/hattrie.dir/clean

ext/htrie/CMakeFiles/hattrie.dir/depend:
	cd /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/src /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/ext/src/htrie /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/ext/htrie /n/groups/church/shilpa/new/butter_ex/butter_ex/scripts/try/build_spades/ext/htrie/CMakeFiles/hattrie.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : ext/htrie/CMakeFiles/hattrie.dir/depend

