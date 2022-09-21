chmod 400 MasterthesisKeyPair.pem
ssh -i "MasterthesisKeyPair.pem" ec2-user@ec2-44-211-40-41.compute-1.amazonaws.com
ssh -L 5901:localhost:5901 -i "MasterthesisKeyPair.pem" ec2-user@ec2-44-211-40-41.compute-1.amazonaws.com

https://medium.com/@jkimera5/installing-a-graphical-user-interface-gui-on-aws-ec2-linux-2-instance-and-accessing-it-over-a-1d96a16949dc
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html
H4lL0$153$

# Install tigerVNC

https://www.cyberciti.biz/faq/install-and-configure-tigervnc-server-on-ubuntu-18-04/

# Transfer files using FileZila

https://it.cornell.edu/academic-web-dynamic-academic-web-static-managed-servers/transfer-files-using-filezilla

# Run a python script 24/7

https://victormerino.medium.com/running-a-python-script-24-7-in-cloud-for-free-amazon-web-services-ec2-76af166ae4fb

# install the working version of twint

pip3 install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint
