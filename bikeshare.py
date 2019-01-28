# Author: Carlos ANdre da Costa Sol

import time
import pandas as pd
import numpy as np
#import ggplot as gp
# import matplotlib.pyplot as plt


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city_get - name of the city to analyze
        (str) month_get - name of the month to filter by, or "all" to apply no month filter
        (str) day_get - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    month_aux_valid = ["MONTH", "DAY", "BOTH", "NONE"]
    month_valid = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE"]
    city_valid = ["CHICAGO", "NEW YORK", "WASHINGTON"]
    day_valid = ["1","2","3","4","5","6","7"]
    city_get=""
    month_aux=""
    month_get=""
    day_get=""
    global msg1 
    msg1 = "Please, type a valid answer."

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    try:
        city_get = str(input("Would you like to see data for Chicago, New York, or Washington? \n")).upper()
    except: 
        print (msg1)
    else:
        while  city_get not in city_valid:
            print (msg1)
            try:
                city_get = str(input("Would you like to see data for Chicago, New York, or Washington? \n")).upper()
            except:
                print (msg1)
                city_get = "erro"
    # get user input for month (all, january, february, ... , june)
    try: 
        month_aux = str(input('Would you like to filter data by month, day, both, or not at all? Type "none" for no time: \n')).upper()
    except: 
        print (msg1)
    else:
        while (month_aux not in month_aux_valid):
            print (msg1)
            try:
                month_aux = str(input('Would you like to filter data by month, day, both, or not at all? Type "none" for no time: \n')).upper()
            except:
                print (msg1)
                month_aux = "erro"
        if (month_aux == "MONTH") or (month_aux == "BOTH"):
            try:
                month_get = str(input('Which month? Type January, February, March, April, May or June: \n')).upper()
            except:
                print (msg1)
            else:
                while (month_get not in month_valid):
                    print (msg1)
                    try:
                        month_get = str(input('Which month? Type January, February, March, April, May or June: \n')).upper()
                    except:
                        print (msg1)
                        month_get = "erro"
                day_get = "0" #if both or month, force here a day_get = 0
             # get user input for day of week (all, monday, tuesday, ... sunday)
            if month_aux == "BOTH":
                try:
                    day_get = str(input('Which day of week? Type 1=Sunday, ...: \n')).upper()
                except:
                    print("Please, type a valid answer.")
                else:
                    while (day_get not in day_valid):
                        print (msg1)
                        try:
                            day_get = str(input('Which day of week? Type 1=Sunday, ...: \n')).upper()
                        except:
                            print (msg1)
                            day_get = "erro"
            else:
                day_get = "0" #if do no choose both, force here a day_get = 0
        elif month_aux == "DAY":
            try:
                day_get = str(input('Which day of week? Type 1=Sunday, ...: \n')).upper()
            except:
                print (msg1)
            else:
                while (day_get not in day_valid):
                    print (msg1)
                    try:
                        day_get = str(input('Which day of week? Type 1=Sunday, ...: \n')).upper()
                    except:
                        print (msg1)
                        day_get = "erro"  
        else:
            day_get = "0" #if do no choose day, force here a day_get = 0
    
    print('-'*40)
    return city_get, month_get, int(day_get)


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    if city == "Chicago":
        filename = "chicago.csv" 
    elif city == "New York":
        filename = "new_york_city.csv"
    else:
        filename = "washington.csv"
    
    if month != "":
        if month ==  "January":    
            m=1            
        elif month == "February":
            m=2
        elif month == "March":
            m=3
        elif month == "April":
            m = 4
        elif month == "May":
            m = 5
        else:
            m = 6
    else:
        m=0
    
    #open and transform
    df = pd.read_csv(filename, delimiter = ',')
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # df['month'] = df['Start Time'].dt.month 
    df['month'] = df['Start Time'].dt.month
    df['dow'] = df['Start Time'].dt.dayofweek
    
    #filter
    if not((m == 0) & (day == 0)):  #has filter
        if ((m != 0) & (day == 0)): # has only month filter
            df = df[df['month'] == m]
        elif ((m == 0) & (day !=0)): #has only day filter
            df = df[df['dow'] == day]
        else: #has month and day filter 
            df = df[(df['month'] == m) & (df['dow'] == day)]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start Month:', popular_month)

    # display the most common day of week
    popular_dow = df['dow'].mode()[0]
    print('Most Popular Start Day of Week:', popular_dow)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    user_aux = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station:', user_aux)

    # display most commonly used end station
    user_aux = df['End Station'].mode()[0]
    print('Most Commonly Used End Station:', user_aux)

    # display most frequent combination of start station and end station trip
    df['Combination'] = df['Start Station'] + " - " + df['End Station']
    user_aux = df['Combination'].mode()[0]
    print('Most Frequent Start Station - End Station Combination:', user_aux)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    
    user_aux = df['Trip Duration'].sum()
    print('Total Travel Time in seconds:', user_aux)

    # display mean travel time
    user_aux = df['Trip Duration'].mean()
    print('Average Travel Time in seconds:', user_aux)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender and Birth Year statistics
    # Display earliest, most recent, and most common year of birth
    if (city == "Chicago") or (city == "New York"):
        user_types = df['Gender'].value_counts()
        print(user_types)
        user_aux = df['Birth Year'].mode()[0]
        print('Most Popular Birth Year:', user_aux)
        user_aux = df['Birth Year'].min()
        print('Earliest Birth Year:', user_aux)
        user_aux = df['Birth Year'].max()
        print('Most Recent Birth Year:', user_aux)
    else:
        print('Washington do not have info about Gender and Birth Year')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def get_lines(df):
    """
    Asks user to specify show lines of data and shows.

    """
    msg1 = "Please, type a valid answer."
    see = 1
    see_valid = [0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    try:
        see = int(input("Would you like to see lines of data? Type from 5 to 50 lines. 0 is no. \n"))
    except: 
        print (msg1)
    else:
        while  see not in see_valid:
            print (msg1)
            try:
                see = int(input("Would you like to see lines of data? Type from 5 to 50 lines. 0 is no \n"))
            except:
                print (msg1)
                see = 1
    if see != 0:
        print('\nShowing Lines...\n')
        start_time = time.time()
        print(df.head(int(see)))
        print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def get_numbers(df):
    """
    Asks user if wants to see descriptive statiscs of data and shows.

    """
    msg1 = "Please, type a valid answer."
    see = ""
    see_valid = ["YES", "NO"]
    try:
        see = str(input("Would you like to see Statistics of data? Type yes or no. \n")).upper()
    except: 
        print (msg1)
    else:
        while  see not in see_valid:
            print (msg1)
            try:
                see = str(input("Would you like to see Statistics of data? Type yes or no. \n")).upper()
            except:
                print (msg1)
                see = "" 
    if see in see_valid:
        print('\nShowing Lines...\n')
        start_time = time.time()
        print(df.describe())
    print('-'*40)

#def get_graph(df):
#    """
#    Asks user if wants to see graph of Trip Duration and shows.

#    """
#    msg1 = "Please, type a valid answer."
#    see = ""
#    see_valid = ["YES", "NO"]
#    try:
#        see = str(input("Would you like to see Graph of Trip Duration? Type yes or no. \n")).upper()
#    except: 
#        print (msg1)
#    else:
#        while  see not in see_valid:
#            print (msg1)
#            try:
#                see = str(input("Would you like to see Graph of Trip Duration? Type yes or no. \n")).upper()
#            except:
#                print (msg1)
#                see = "" 
#    if see in see_valid:
#        print('\nShowing Graph of Trip Duration by hour...\n')
#        start_time = time.time()
        
       # p = gp.ggplot(aes(x='hour', y='Trip Duration'), data=df)
       # p = p + gp.geom_line()  # add points
       # p = p + gp.stat_smooth(color='blue') # add trend line
       # p
        
 #      p = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
#       p = p.cumsum()
#       p.plot()
#       
#        print('\nShowing Graph of Trip Duration Density...\n')
       # p = gp.ggplot(aes(x='Trip Duration'), data=df)
       # p = p + gp.geom_density()  # add type of graph
       # p
        
#        print("\nThis took %s seconds." % (time.time() - start_time))
#    print('-'*40)



def main():
    """
    Explore Bikeshare data.
    Calculate Statistcs 
    
    Returns:
        Calculate Statistcs based on some inputs of ueser: City, month and day of week
        
    Author: Carlos Andre da Costa Sol
    """
    
    
    print('Hello! Let\'s explore some US bikeshare data!')  
    while True:
        city, month, day = get_filters()
        
        df = load_data(city, month, day)
        #df.to_csv('out.csv')
        #df.head()
        #df.describe()
        #df.info()
        
        time_stats(df)
        x = str(input("Press Enter to continue. \n"))
        station_stats(df)
        x = str(input("Press Enter key to continue. \n"))
        trip_duration_stats(df)
        x = str(input("Press Enter to continue. \n"))
        user_stats(df, city)
        x = str(input("Press Enter to continue. \n"))
        get_lines(df)
        x = str(input("Press Enter to continue. \n"))
        get_numbers(df)
        #get_graph(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
