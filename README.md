# Cryptocurrency Analysis & Projection Web Application
---
![Fintech-image](./images/crypto_image.png)

This is an application to analyze historical data on a specific cryptocurrency to help investors decide if they want to include it in their portfolio. We designed the app to run on Streamlit to make it more interactive and fun. We have 5 Dashboards that help the user analyze there favorite crypto. 

***
## Technologies

This app uses python 3.7 with the following libraries and dependencies:

- [streamlit](https://docs.streamlit.io/)

- [pandas](https://pandas.pydata.org/docs/)

- [numpy](https://numpy.org/doc/)

- [nomics](https://github.com/TaylorFacen/nomics-python)

- [tweepy](https://docs.tweepy.org/en/stable/)

- [matplotlib](https://https://pypi.org/project/matplotlib/)

***
## Installation Guide

To get started using this application please go to [Python Download](https://www.python.org/downloads/) and select the version for your operating system. Then install the following libraries and packages.

If you need pip for python 3 use the command  ``` sudo apt install python3-pip ```

Then use pip to install pandas like this:

``` pip install streamlit ```

``` pip install pandas ```

``` pip install numpy ```

``` pip install nomics-python ```

``` pip install tweepy ```

``` pip install matplotlib ```

***
## Usage
To run the application, run *cp.py* web application, open a terminal (CLI) and in the project folder run:
```streamlit run cp.py```


This app uses the Nomics API to get real time data regarding current crypto asset prices. To run the app effectively , go to :

- [Nomics](https://p.nomics.com/cryptocurrency-bitcoin-api)

Get a free API Key, save the API key in a file in the working folder and name the file .env
Please include in the .env file ``` NOMICS_API_KEY = "your api key" ```

***
## Contributors

Noah Beito 

Christina San Diego

Stephen Thomas

***
## License

MIT
