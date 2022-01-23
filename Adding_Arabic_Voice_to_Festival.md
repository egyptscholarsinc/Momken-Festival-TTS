# Adding Arabic language to Festival

We will add the Arabic voice found at [this repository](https://github.com/linuxscout/festival-tts-arabic-voices)

## Steps
1. First you need to install Festival project by following the steps found in `Install_Festival.md` file, we will assume that the projects are installed at the directory D:\tts_projects, so the D:\tts_projects folder contain hte 2 folders 
2. Clone the [festival-tts-arabic-voices](https://github.com/linuxscout/festival-tts-arabic-voices)
3. Copy the language folder in the repo to festival/lib folder
4. Unzip the zip folder found at releases/ara_norm_ziad_hts.zip in the repo to festival/lib/voices/arabic/ara_norm_ziad_hts folder, such that the festival project directory has the following structure
    - festival
        - lib
            - languages
                - language_arabic.scm
            - voices
                - english
                    - kal_diphone
                        - ...
                    - rab_diphone
                        - ...
                - arabic
                    - ara_norm_ziad_hts
                        - festvox
                            - ara_norm_addenda.scm
                            - ...
                        - hts
                            - ara_norm_ziad_hts.htsvoice
                            - ...
        - bin
            - ...
        - ...
5. In the file festival/lib/voices/arabic/ara_norm_ziad_hts/festvox/ara_norm_ziad_lexicon.scm change all occurrences of *"/usr/share/festival/voices/arabic/ara_norm_ziad_hts/festvox/ara_norm_ziad_char_phone_map.scm"* to the actual absolute path of the *ara_norm_ziad_char_phone_map.scm* file found at your festival/lib/voices/arabic/festvox directory (In my Windows machine I changed it to something like /cygdrive/d/tts_projects/festival/lib/voices/arabic/ara_norm_ziad_hts/festvox/ara_norm_ziad_char_phone_map.scm)
6. **Copy** the whole festival/lib/voices folder to festival/voices such that festival/lib/voices is the same as festival/voices
7. Now you can test the arabic voice by running `festival` and in the prompt type the following commands
```Scheme
(voice_ara_norm_ziad_hts )
(SayText "السلام عليكم")
```
8. (Optional) To be able to run the arabic voice on a text file from the command line using the command `festival --tts --language arabic myFile.txt` you need to make the following change in the *festival/lib/languages.scm* file:
After the definition of spanish language there is the definition of select_language function, replace it with the following code (the code defines the arabic language and re-defines the select_language function)
```Scheme
(define (language_arabic)
"(language_arabic)
Set up language parameters for Arabic."

  (voice_ara_norm_ziad_hts)
  (set! male1 voice_ara_norm_ziad_hts)

  (Parameter.set 'Language 'arabic)
)

(define (select_language language)
  (cond
   ((or (equal? language 'britishenglish)
   (equal? language 'english))  ;; we all know its the *real* English
    (language_british_english))
   ((equal? language 'americanenglish)
    (language_american_english))
   ((equal? language 'scotsgaelic)
    (language_scots_gaelic))
   ((equal? language 'welsh)
    (language_welsh))
   ((equal? language 'spanish)
    (language_castillian_spanish))
    ((equal? language 'arabic)
    (language_arabic))
   ((equal? language 'klingon)
    (language_klingon))
   (t
    (print "Unsupported language, using English")
    (language_british_english))))

```