# IT_Automation Project

IT_Automation_Project is a Python library I wrote to complete the final project in Google's IT automation with Python class.

The library provides basic system monitoring, image processing, PDF file generation,  and email generation.

# overview
There are 7 modules in this project. 

### health_checks
This module contains functions for checking if system resources are overloaded and then emailing a error message.
### ChangeImage
Functions for converting images in a directory into jpeg images, images can also be resized.
### emails
This module contains functions for generating and sending emails. Email attachments are optional.
### reports
Functions for generating pdf reports.
### report_email
This module is specific to the final assignment but I will in include it here.
Generates a pdf report from Google's supplier data. The report is attached to an email message and sent.
### Supplier_image_upload
This module is specific to the final assignment but I will in include it here. Makes a post request for every jpeg image in a directory. This script is used for Google's IT_automation class. The directory contains images for every fruit that will be displayed in customers website.
### run
This module is specific to the final assignment but I will in include it here. Functions for reading a directory and then making post request with the data. This is used for Google's IT automation class project. Reads a directory with files containing information on fruits and then makes a post request to the class website to show the data.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install it-automation-martin.

```bash
pip install it-automation-martin
```

## Usage

### health_checks
```python
from it_automation import health_checks

cpu_percent_usage_threshold = 80
available_disk_space_percent_threshold = 20
memory_threshold = 500 * 1024 * 1024  # 500MB
email_body = 'Please check your system and resolve the issue as soon as possible.'
sender = "test_email@gmail.com"
receiver = "test_email@gmail.com"

health_checks.check_systems(cpu_percent_usage_threshold, 
    available_disk_space_percent_threshold,
    memory_threshold, 
    sender, 
    receiver, 
    email_body)
```
### changeImage
```python
from it_automation import changeImage

image_directory = os.path.expanduser('~') + '/Images'

output_directory = os.path.expanduser('~') + '/Images'
resize_width = 600
resize_height = 400
convert_image(image_directory, resize_width, resize_height, output_directory)
```

## Apology
Sorry for the mixture of camel case and snake case in some module names. I prefer snake case but I had to have some modules named in camel case because the course required some modules to have specific names that were given to me. I might refactor later to be consistent.

## Contributing
Pull requests are welcome.

## License
[MIT](https://choosealicense.com/licenses/mit/)
