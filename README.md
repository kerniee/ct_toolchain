# Tool chain for testing with Classification Tree and Combinatorial Testing
This project aims to simplify process of using classification tree method for combinatorial testing.
It translates diagrams from [draw.io](https://draw.io/) directly into ACTS specifications which can be used in many 
Combinatorial Testing tools such as [Matris](https://matris.sba-research.org/tools/cagen/#/workspaces) 
and [ACTS](tools/ACTS3.2).

# Workflow
1. Modeling the Input Domain Using the Classification Tree Method  
- Go to [draw.io](https://draw.io/)  
- Draw Classification Tree. Make sure to name all nodes and connect them with directed edges
- Go to File > Export > XML... and save it to device
2. Convert Classification Tree to ACTS
- Make sure you have python with version 3.9 or greater installed
- Run `pip install xml-to-acts`
- Run `xml-to-acts your_downloaded_file.xml acts.txt`
- (Optional) Add constraints to resulting ACTS
3. Convert ACTS to test cases
- Example: use ACTS3.2 provided in repo. Usage: `java -jar .\tools\ACTS3.2\acts_3.2.jar acts.txt`
- Example: use [Matris](https://matris.sba-research.org/tools/cagen/#/workspaces) 
feature *Import from ACTS configuration file* and generate test cases