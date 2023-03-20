# SIS Command Check Scripts
#### Video Demo: <https://youtu.be/EdOlbomS8Xg>
#### Description:
        This python script is to help with my work productivity by testing the Simple-Instruction-Set (SIS) commands which control the unit.

        Although each product have their own set of commands and responses, mine will be a small sample from the product I use the most, the ISS 612[^1].
        User will be able to choose which set of commands they would like to test.
        The program will then connect via telnet to the unit and test the sets of commands
        Once completed a Excel file will be generated to show: 1) the command sent, 2) the expected response, 3) the actual response.

        The Excel file will show which responses were incorrect and highlight/count the number of incorrect responses. The commands and expected responses can be found in the user manual[^2] in the "SIS Configuration and Control" section. To reduce the complexity, I have used certain groups of commands which are crucial to the usuability of the product.

## **How it works**
The code will initally ask for the IP address of the unit.
The IP address must be a certain format (###.###.###.###) or it will keep prompting for the IP address. Once an IP address is entered, it will attempt to make a connection to make sure the unit is online. If not online, it will exit.

The program will then ask which sets of commands they would like to test.
1. Input Switches (Video/Audio/Both)
2. Input Configuration
   - HDCP Authorization
   - Aspect Ratio
3. Output Configuration
   - HDCP Mode
   - Output Mute/Freeze
4. Effect Configuration
   - Effect Type
   - Effect Duration
5. Miscellaneous
   - Test Pattern
   - Executive Mode

Users are able to select one or more sets, before typing "done" to start the testing process.

The program will intially create a save file and then go through each set of commands and verify that the unit will return the expected response. The end result will be a Excel file with the SIS command sent, the expected response, and the received response (highlighted green if correct, red if incorrect).

### **Design Choices**
**GetIPAddress Function:**
I used regex to verify that the entered "address" was correct similar to one of the homework assignments.

**Connection Function:**
This was to make sure the IP was to the correct unit and that it was online.

**CommandSets Function:**
The function will initially prompt the user for their choices. Upon making a choice I wanted to show the option they chose so the user would know which sets they would be choosing.
I wanted to prevent random numbers or words being part of the command sets.

**SaveFile Function:**
The date/time was used to create unique filenames so that there was less chances of files being overwritten.

**SISCommandCheck Function:**
This portion was the most difficult as I had to figure out telnetlib as well as pandas lib. Pandas was used as it allowed me to read/manipulate excel files. 


[^1]: https://www.extron.com/product/iss612
[^2]: https://media.extron.com/public/download/files/userman/iss608_iss612_68-2994-01_D.pdf