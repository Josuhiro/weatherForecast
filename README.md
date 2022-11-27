# Weather forecaster

k2 weather monitoring app


## Author

- [@josuhiro](https://www.github.com/josuhiro)


## How to use the aplication

1. Go to https://openweathermap.org/ and create  an account.
Then go to https://home.openweathermap.org/api_keys and copy your api key.
It may take some time for the key to be activated.
2. Paste your api key in .env file next to `API_KEY =`         
3. Open up terminal and type `pip install -r requirements.txt` to install needed libraries.   
4. Run main.py file.    
5. In run window you will see app menu:     
- If you want to check current weather type 1 and press enter.  
- If you want to check diagram forecast for 5 days type 2 and press enter. Maximize the diagram window to make the data easier to read. You have to close diagram window to continue using the application.     
- If you want to check minimum, maximum and average temperature type 3 and press enter.
- If you want to exit application type 0 and press enter.   
6. If you leave the application on, the data for the current temperature will be updated every 11 minutes, and for the five-day weather forecast every 30 minutes.


