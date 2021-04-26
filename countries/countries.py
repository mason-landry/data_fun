import requests
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

class Country:
    def __init__(self, name, capital, population, borders, currencies):
        self.name = name
        self.capital = capital
        self.population = population
        self.borders = borders
        self.currencies = currencies
        
    def get_currencies_USD(self):
        self.converted_currencies = get_currencies_USD(self.currencies)

def get_countries():
    ''' 
    This function simply returns information using the REST Countries API found on Rapid-API
    https://rapidapi.com/ajayakv/api/rest-countries/endpoints '''
    
    url = "https://ajayakv-rest-countries-v1.p.rapidapi.com/rest/v1/all" # Base URL

    headers = {
        'x-rapidapi-key': "5fd1799244msh9b3ecad011754c7p1df26bjsnfea159fb049a", # You will have your own long key created by Rapid API
        'x-rapidapi-host': "ajayakv-rest-countries-v1.p.rapidapi.com" # This is the default
        }

    response = requests.request("GET", url, headers=headers) # Generate the response using a GET request
    return response.json()

def filter_countries(countries:list):
    '''We want to filter the country list for only the relevant parameters we care about, which are:
        -Name
        -Capital
        -Population
        -Borders
        -Currencies
    '''
    stats = []
    for c in countries:
        stats.append(Country(c["name"], c["capital"], c["population"], c["borders"], c["currencies"]))
    
    return stats

def get_currencies_USD(currencies:list):
    url = "https://exchangerate-api.p.rapidapi.com/rapid/latest/USD"

    headers = {
        'x-rapidapi-key': "5fd1799244msh9b3ecad011754c7p1df26bjsnfea159fb049a",
        'x-rapidapi-host': "exchangerate-api.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers)
    rates = response.json()["rates"]
    try:
        curr = [rates[c] for c in currencies]
        return curr
    except:
        return [1]


if __name__ == "__main__":

    countries = get_countries()
    filtered_countries = filter_countries(countries)

    ## Plot top 25 countries by population
    sorted_countries = sorted(filtered_countries, key=lambda x: x.population, reverse=False) # Sort the countries by population
    sorted_countries = sorted_countries[-25:] # Only look at the last 25 countries
    names = [c.name for c in sorted_countries]
    pops = [c.population for c in sorted_countries]

    # Set dark grid using seaborn
    sns.set()

    # Create plot and define parameters
    fig, ax = plt.subplots()
    bar_width = 0.5
    opacity = 0.8
    y_pos = np.arange(len(names)) # create a range the length of our 'names' list
    p = plt.barh(y_pos+bar_width, pops, alpha=opacity, label='Top 25 Countries by Population')
    plt.yticks(y_pos+bar_width, names, fontsize=12)
    plt.xlabel('Population')
    plt.xticks(ticks=range(0,1500000000,250000000))
    plt.ticklabel_format(style='plain', axis='x')
    plt.title('Top 25 Countries by Population')
    # Small loop to place text on plot for each bar value:
    for i, v in enumerate(pops):
        plt.text(v + 1000000, i+0.25, str(v), color='black')
    plt.show()



        
    
    ## Plot top 25 countries by currency value
    
    # Loop to get the currency value for our sorted countries
    for i, c in enumerate(sorted_countries):
        c.get_currencies_USD()
    
    names = [c.name for c in sorted_countries]
    if 'Democratic Republic of the Congo' in names:
        names[names.index('Democratic Republic of the Congo')] = 'DROC'
    currs = [c.converted_currencies for c in sorted_countries]
    currs = [c[0] for c in currs]

    # Set dark grid using seaborn
    sns.set()

    # Create plot and define parameters
    fig, ax = plt.subplots()
    bar_width = 0.5
    opacity = 0.8
    y_pos = np.arange(len(names)) # create a range the length of our 'names' list
    p = plt.barh(y_pos+bar_width, currs, alpha=opacity, label='Exchange Rates of Top 25 Most Populous Countries')
    plt.yticks(y_pos+bar_width, names, fontsize=12)
    plt.xlabel('Value of USD in Local Currency')
    # plt.xticks(ticks=range(0,1500000000,250000000))
    plt.ticklabel_format(style='plain', axis='x')
    plt.title('Exchange Rates of Top 25 Most Populous Countries')
    # Small loop to place text on plot for each bar value:
    for i, v in enumerate(currs):
        plt.text(v, i+0.25, str(v), color='black')
    plt.show()
    