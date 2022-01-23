# Festival installation

Instructions for installation of Festival version 2.5 and also the Edinburgh Speech Tools (EST) library which is a prerequisite for Festival
## Install Festival directly on Ubuntu
Run the following command:
```bash
sudo apt-get install festival
```

## Build Festival from source

### Requirements
The following requirements are common for Linux and Windows
- Download the following from [this link](http://festvox.org/packed/festival/2.5/)
    - festival-2.5.0-release.tar.gz (Festival source)
    - speech_tools-2.5.0-release.tar.gz (Speech tools source)
    - festlex_CMU.tar.gz (Careign mellon university lexicon)
    - festlex_OALD.tar.gz (Oxford Advanced Learner's Dictionary lexicon)
    - festlex_POSLEX.tar.gz (POSLEX lexicon)
    - From the voices directory download:
        - festvox_kallpc16k.tar.gz (American English voice)
        - festvox_rablpc16k.tar.gz (British English voice)
- C++ compiler (I used GCC 2.7.2)
    - Make sure you can compile a simple Hello World example using the compiler. Refer to [this link] (https://www.linuxtopia.org/online_books/an_introduction_to_gcc/gccintro_54.html) on how to compile a C++ source file using command line.
- GNU Make
- NCurses library
    - For Ubuntu you can install NCurses library using `sudo apt-get install libncurses5-dev`
    - For Windows refer to the *"Setting up Windows building environment"* section

### Setting up Windows building environment
To compile the festival and speech tools projects on Windows, I used [Cygwin](https://www.cygwin.com/) which provides large number of Linux functionality on Windows.
I used Cygwin with the following packages:
- gcc
- make
- grep
- awk
- sed
- libncurses-devel

To install these packages on Cygwin, you have 2 options:
- When installing Cygwin it asks you about what packages to install with it, so check the previous list of packages.
- Or you can get apt-cyg from Cygwin terminal ([refer to this answer from StackOverflow about how to add it](https://stackoverflow.com/a/47485866)), and then manually install each of the previous packages as you do with Ubuntu's apt-get

After setting up Cygwin add the Cygwin bin folder to the Windows `PATH` environment variable

### Installation steps

We will assume that we will install the projects in a folder with path D:\tts_projects. Adjust the paths mentioned in these steps to adapt to the directory where you install the projects
1. Unpack the contents of `speech_tools-2.5.0-release.tar.gz` and `festival-2.5.0-release.tar.gz` in D:\tts_projects (you can use 9zip on windows to unpack tar.gz files), such that you have the following directory structure
    - D:\tts_projects
        - festival
            - config
            - lib
            - src
            - ...
        - speech_tools
            - config
            - audio
            - main
            - ...
2. Before compiling the Festival project we need to compile the speech tools project first.
    - Change directory to `D:\tts_projects\speech_tools`
    - Run the command `make info` (For some `make` installations the command is `gnumake info`)
    - After that I needed to do the following 2 edits on for Cygwin on Windows.
        - Search for the `SYSTEM_TYPE` in the file speech_tools/config/config and change it to `SYSTEM_TYPE=ix86_CYGWIN32`
        - Search for `-lcurses` in the file speech_tools/config/config and change it to `-lncurses`
    - Run the command `make` in the directory D:\tts_projects\speech_tools. If it compiled successfully you should see a `bin` directory inside `speech_tools` directory
3. After successfully compiling the speech tools library, add the D:\tts_projects\speech_tools\bin to the `PATH` environment variable (you may want to restart the computer after that).
4. To compile the Festival project, change directory to `D:\tts_projects\festival` and run `make` command in the terminal. If it compiled successfully you should see a `bin` directory inside `festival` directory
5. After successfully compiling the festival project, add the D:\tts_projects\festival\bin to the `PATH` environment variable (you may want to restart the computer after that).
6. Unpack the `festlex_CMU.tar.gz`, `festlex_OALD.tar.gz` and `festlex_POSLEX.tar.gz` and put their content inside festival/lib/dict directory such that the festival folder has the following structure
    - festival
        - lib
            - dicts
                - cmu
                    - cmudict-0.4.scm
                    - ...
                - oald
                    - oaldlex.scm
                    - ...
                - wsj.wp39.poslexR
                - wsj.wp39.tri.ngrambin
            - multisyn
                - ...
            - ...
        - bin
            - ...
        - ...
7. Compile the cmu and oald lexicons by changing to the directories `festival\lib\dicts\cmu` and `festival\lib\dicts\oald` and running `make` command in each of them
8. Unpack the `festvox_kallpc16k.tar.gz`, `festvox_rablpc16k.tar.gz` and put their content inside festival/lib/voices/english directory such that the festival folder has the following structure
    - festival
        - lib
            - voices
                - english
                    - kal_diphone
                        - festvox
                            - kal_diphone.scm
                            - kaldurtreeZ.scm
                        - group
                            - kallpc16k.group
                        - COPYING
                    - rab_diphone
                        - festvox
                            - rab_diphone.scm
                        - group
                            - rablpc16k.group
                        - COPYING
            - multisyn
                - ...
            - ...
        - bin
            - ...
        - ...
9. After completing all these steps successfully, you should be able to run festival from the terminal by using the command `festival`, you should see then the festival prompt. To test the text to speech run the following command in the festival prompt (with the parentheses):
```Scheme
(SayText "This is a test.")
```

