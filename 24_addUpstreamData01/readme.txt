sudo apt-get update

sudo apt-get install libffi-dev libssl-dev python-dev python-pip

sudo apt-get install python-numpy cython

sudo apt-get install python-pandas


From GS - > VM

gsutil cp -r gs://wri001-1058/ce . 

mkdir output

sudo chmod 777 output

run python script

gcloud auth login

gcloud compute ssh rutgerhofste@instance-4 --zone us-east1-d

From VM - > GS

gsutil cp -r . gs://wri001-1058/ce 
