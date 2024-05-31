import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #Get user input for city
    while True:
        cities = ['chicago', 'c', 'new york city', 'n', 'washington', 'w']
        city = input('Choose one city only: (C)hicago, (N)ew York City, (W)ashington ').lower()
        if city in cities:
            if city == 'c':
                city = 'chicago'
            if city == 'n':
                city = 'new york city'
            if city == 'w':
                city = 'washington'
            break
        else:
            print('Please specify only Chicago, New York City, or Washington \n')                    
                 

    # get user input for month
    while True:
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        nd_months = ['july', 'august', 'september', 'october', 'november', 'december']
        month = input('Specify a month (January - June) to filter by, or type all for no filter: ').lower()
        if month in months:
            break
        if month in nd_months:
            print('No data for this month.')
        else:
            print('Please check your spelling or type all for no filter \n') 

    # get user input for day of week
    while True:
        day = input('Specify a day to filter by, or type all for no filter: ').lower()
        if (day == 'monday' or day == 'tuesday' or day == 'wednesday' or day == 'thursday' or day == 'friday' or day == 'saturday' or day == 'sunday' or day == 'all'):
            break
        else:
            print('Please check your spelling or type all for no filter \n') 

    print('-'*40)
    return city, month, day


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
# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    common_month = df['month'].mode()
    print(f'The most common month is {months[common_month[0]-1].title()}')

    #display the most common day of week
    common_day = df['day_of_week'].mode()
    print(f'The most common day of the week is {common_day[0]}')

    #display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()
    print(f'The most common start hour is {common_hour[0]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    common_ss = df['Start Station'].mode()
    print(f'\nThe most commonly used start station is {common_ss[0]}\n')

    #display most commonly used end station
    common_es = df['End Station'].mode()
    print(f'\nThe most commonly used end station is {common_es[0]}\n')

    #display most frequent combination of start station and end station trip
    print('Most frequent combination of start station and end station trip: \n')
    grouped = pd.DataFrame(df.groupby(['Start Station', 'End Station'])['Start Station'].count())
    grouped.columns = ['Total Trips']
    grouped = grouped.reset_index()
    print(grouped.sort_values('Total Trips', ascending = False).iloc[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Time'] = df['Trip Duration'].round().apply(pd.to_timedelta, unit = 's')
    
    timesum = df['Time'].sum()
    timemean = df['Time'].mean()

    #display total travel time
    print(f'The total travel time for all users is {timesum}\n')
    
    #display mean travel time
    print(f'The average travel time of all users is {timemean}\n')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f'The counts of user types is \n{user_types}')
    print('\n')
    #Display counts of gender
    if city == 'washington':
        print('Gender data not available for this city\n')
    else:
        gender = df['Gender'].value_counts()
        print(f'The counts of users by gender is \n{gender}')

    #Display earliest, most recent, and most common year of birth
    
    if city == 'washington':
        print('Birth year data not available for this city\n')
    else:        
        print(f"\nThe earliest birth year is {df['Birth Year'].min()}")
        print(f"\nThe most recent birth year is {df['Birth Year'].max()}")
        print(f"\nThe most common year of birth is {df['Birth Year'].mode()}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def ind_data(df):
    prompt = input('Would you like to view 5 lines of individual trip data? (Y / N): ')
    if prompt.lower() == 'y':
        count = 0
        while count < df.shape[0]:
            if count + 5 > df.shape[0]:
                for i in range(df.shape[0] - count):
                    print(df.iloc[count+i,~df.columns.isin(['month', 'day_of_week'])])
            else:
                for i in range(5):
                    print(df.iloc[count+i,~df.columns.isin(['month', 'day_of_week'])])
                    print('\n')
            count += 5
            cont = input('Press enter to continue or type end to quit: ')
            if cont == 'end':
                break
    else:
        return

def main():
    global city
    while True:
        city, month, day = (get_filters())
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        ind_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
