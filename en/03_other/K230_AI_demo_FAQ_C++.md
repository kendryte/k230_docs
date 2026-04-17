# K230 AI Demo Frequently Asked Questions (C++)

## TF Boot Failed with Exit Code 13

Problem: TF card boot reports a "boot failed with exit code 13" error.

Solution: The reasons are as follows: 1. There is an error in the files within the boot medium. 2. Incorrect boot pin settings.

Special note on TF card boot pin settings: The TF card will only boot when the levels of the two boot pins are high (they need to be set to positions 1 and 2 as per the silkscreen, which is the opposite direction of ON).
