import pandas as pd
import time
import concurrent.futures
import requests
import matplotlib.pyplot as plot
# Incorporate 1 or more modules to assess and measure program performance.
# Apply approaches and libraries to deliver asynchronous programming.
# Implement parallel process or multithreading to deliver concurrent program performance
# Implement patterns as a reusable component in programming.
# Use the Documentation Guide and provide a documentation of your project

#These are the URLS that are used for comparison
csv_urls = [
    'https://data.chhs.ca.gov/dataset/e39edc8e-9db1-40a7-9e87-89169401c3f5/resource/c5978614-6a23-450b-b637-171252052214/download/covid19postvaxstatewidestats.csv',
    'https://data.chhs.ca.gov/dataset/e39edc8e-9db1-40a7-9e87-89169401c3f5/resource/de27ce58-edc8-45fb-bebc-08c4b29c5efe/download/covid19postvaxstatewidestats_07172022.csv'
]

def main():
    #start timer
    t1 = time.perf_counter()

    #Retrieve and parse the csv files and the names
    #implemented concurrent.futures to speed up the downloading processes
    def download_csv(csv_url):
        csv_bytes = requests.get(csv_url).content
        csv_names = csv_url.split('/')[8]

        with open(csv_names, 'wb') as csv_file:
            csv_file.write(csv_bytes)
            print(f'{csv_names} was downloaded...')    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_csv, csv_urls)
    
    #end timer
    t2 = time.perf_counter()

    print(f'Finished downloading in {t2-t1} second(s)')

    #Setting variables so that they can be read using the pandas dataframe
    Post_Vax_Without_Boosted = pd.read_csv("covid19postvaxstatewidestats.csv")
    Post_Vax_Without_Boosted.set_index('date', inplace=True)
    
    Post_Vax_With_Boosted = pd.read_csv("covid19postvaxstatewidestats_07172022.csv")
    Post_Vax_With_Boosted.set_index('date', inplace=True)
    
    def menu():
        print("[1] Load Unboosted CSV File ")
        print("[2] Load Boosted CSV File")
        print("[3] Vaccinated Cases vs. Unvaccinated Cases")
        print("[4] Vaccinated Deaths vs. Unvaccinated Deaths")
        print("[5] Population Vaccinated vs. Population Unvaccinated")
        print("[6] Population Vaccinated vs. Population Boosted")
        print("[0] Exit the Program")

    #Displays entire csv file downloaded
    def unboosted_CSV():
        print(Post_Vax_With_Boosted)
    
    #Displays entire csv file downloaded
    def boosted_CSV():
        print(Post_Vax_Without_Boosted)

    #Comparing vaccinated cases and unvaccinated cases
    #using .loc to obtain the columns specified in the targeted csv file
    #Using the pandas plot method and setting certain parameters according to what looks best
    def VC_vs_UC():
        data = Post_Vax_Without_Boosted.loc[:,["vaccinated_cases","unvaccinated_cases"]]
        df = pd.DataFrame(data=data, columns=['vaccinated_cases', 'unvaccinated_cases'])
        df.plot(title = 'Covid Cases: Vaccinated vs Unvaccinated', figsize=(12,5), grid=True)
        plot.show(block=True)

    #Comparing vaccinated deaths and unvaccinated deaths
    #Since the numbers are smaller, I specified yticks
    def VD_vs_UD():
        data = Post_Vax_Without_Boosted.loc[:,["vaccinated_deaths","unvaccinated_deaths"]]
        df = pd.DataFrame(data=data, columns=['vaccinated_deaths', 'unvaccinated_deaths'])
        df.plot(title = 'Covid Deaths: Vaccinated Deaths vs Unvaccinated Deaths', figsize=(10,5), grid=True, yticks=(0,25,50,75,100,125,150,175,200))
        plot.show(block=True)

    #Comparing population of unvaccinated and population of vaccinated
    #This produces an inverser relation as expected
    def PV_vs_PuV():
        data = Post_Vax_Without_Boosted.loc[:,["population_unvaccinated","population_vaccinated"]]
        df = pd.DataFrame(data=data, columns=['population_unvaccinated', 'population_vaccinated'])
        df.plot(title = 'Covid Population: Population Vaccinated vs Population Unvaccinated', figsize=(10,5), grid=True)
        plot.show(block=True)

    #Comparing population vaccinated and population boosted
    #There aren't less people becoming vaccinated... 
    # Vaccinated people getting their booster removes them from the population vaccinated category
    def PV_vs_PB():
        data = Post_Vax_With_Boosted.loc[:,["population_vaccinated","population_boosted"]]
        df = pd.DataFrame(data=data, columns=['population_vaccinated', 'population_boosted'])
        df.plot(title = 'Covid Population: Population Vaccinated vs Population Boosted', figsize=(10,5), grid=True)
        plot.show(block=True)
    
    menu()
    option = int(input("Enter your option: "))

    while option != 0:
        if option == 1: 
            print("Option 1 has been called")
            unboosted_CSV()
        elif option == 2: 
            print("Option 2 has been called")
            boosted_CSV()
        elif option == 3:
            print("Option 3 has been called")
            VC_vs_UC()
        elif option == 4:
            print("Option 4 has been called")
            VD_vs_UD()
        elif option == 5:
            print("Option 5 has been called")
            PV_vs_PuV()
        elif option == 6:
            print("Option 6 has been called")
            PV_vs_PB()
        else: 
            print("Invalid option. Try again")
        print()
        menu()
        option = int(input("Enter your option: "))

if __name__ == '__main__':
    main()