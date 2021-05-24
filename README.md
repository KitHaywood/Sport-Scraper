# Sport-Scraper
A trial dashboard which allows users to scrape some top goal scoring data and write to a DB after checking for duplicated lineitems.

To use this code locally simply clone into the repo & run 

```python
pip3 install -r requirements.txt
```
This will spin up a little server on your local machine and allow you to access it in a browser @ 127.0.0.1. 

If you want to deploy the app to the internet and have it scrape and write to your own MySQL database first install MySQL (skip ahead if MySQL is already installed and set up). 
```linux
sudo apt-get install mysql-server
```
You may also need a MySQL interface but it isn't required. I use Workbench, for the download process I suggest using a relevant youtube tutorial - there are plenty in that space. This is to help manage connections and set up users etc. All this is possible in the terminal but it's nice to do it in a GUI. 

It is a good idea to make sure you know your MySQL password, to do this attempt to connect to the database in the terminal with:
```linux
sudo mysql -u root -p
```
And then enter your password when prompted - if the terminal accepts the credentials then you are good to go. 

Once you have a MySQL server working. Then it's time to set up a Database. First create a schema:
```sql
CREATE SCHEMA SportScraper;
```
Exit MySQL back to the terminal. Start a virtual environment with:
```linux
python3 -m venv venv/
```
And activate with:
```linux
source venv/bin/activate
```
You can confirm that you are in the venv by looking at the hostname or by using:
```linux
echo $VIRTUAL_ENV
```
Now do:
```linux
pip3 install -r requirements.txt
```
Once the modules having finished installing in the venv we need to have a look at deployment. I use GCP and that will be the focus here. First, if you don't have a GCP account then that is where to start, set one up and then install the gcloud-sdk. Again, there are plenty of youtube videos to use here if you are unsure how to proceed - it is a well documented process.

Once this is set up, go to App Engine in the g
