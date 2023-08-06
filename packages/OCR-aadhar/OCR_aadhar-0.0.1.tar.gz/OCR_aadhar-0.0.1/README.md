# OCR_aadhar
##  A dataset Library for Aadhar card

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://github.com/adarsh1mehra/OCR_aadhar)

OCR_aadhar is a ready to use module consisting of Aadhar card image dataset with annotation of features as follows:
1 : Name ( In english only V==0.0.1 )
2 : Date of Birth
3 : Gender
4 : Aadhar Number
Update Soon:
OCR_aadhar==0.1.0
##HOW TO USE
>>> from OCR_aadhar import Unpack
>>>unpack= Unpack()   ## calling class method
>>> #choose a location to save image dataset
>>>loc=r'C://users/adarsh1mehra/Folder'
>>>n=integer<100  #number of images to store Eg:5
>>>data=unpack.img_sv(n,loc) #call img_sv function to save dataset 
>>>#at provided location

New Update will have annotation of below:
1 : Aadhar QR
2 : Face Annotation

Install Requires:
1 : os
2 : numpy
3 : sqlite3
4 : pkg_resources
5 : pathlib

### WARNING : Provided dataset is only for Research purpose
###For Any Further Improvements : Kindly Pinge me on github @adarsh1mehra