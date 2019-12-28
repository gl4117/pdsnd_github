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
    print('Hello! Let\'s explore some US bikeshare data! Note: only Chicago, NYC and Washington available.')

    MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

    # User input for city (chicago, new york city, washington). Invalid inputs are caught using an if loop.
    city = input('Enter name of a city (Note: only chicago, nyc and washington available at this time): ').lower()

    while True:
        if city in CITY_DATA:
            break
        else:
            print('Sorry, data not available for that city')
            city = input('Enter name of a city (Note: only chicago, nyc and washington available at this time): ').lower()

    # Get user input for month (all, january, february, ... , june). Invalid inputs are caught using an if loop.

    month = input('Choose month (Note: only jan to jun available at this time): ').lower()

    while True:
        if month in MONTHS:
            break
        else:
            print('Sorry, data not available for that month')
            month = input('Choose month (Note: only jan to jun available at this time): ').lower()

    # Get user input for day of week (all, monday, tuesday, ... sunday). Invalid inputs are caught using an if loop.

    day = input('Choose weekday: ').lower()

    while True:
        if day in WEEKDAYS:
            break
        else:
            print('invalid input')
            day = input('Choose weekday: ').lower()

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
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all': #use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

    # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all': #filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['month'].mode()[0]
    print('\nThe most common month was...', common_month)

    # Display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('\nThe most common day was...', common_day)

    # Display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('\nThe most common start hour was...', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('\nThe most common start station was...', common_start_station)

    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('\nThe most common end station was...', common_end_station)

    # Display most frequent combination of start station and end station trip
    df['combination_station'] = df['Start Station'] + ' to ' + df['End Station']
    common_combo_station = df['combination_station'].mode()[0]
    print('\nThe most common route was...', common_combo_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print('\nThe total duration of trips is...', total_trip_duration, 'seconds')

    # Display mean travel time
    avg_trip_duration = df['Trip Duration'].mean()
    print('\nThe average duration of trips is...', avg_trip_duration, 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('\nThe user type breakdown is...\n', pd.DataFrame(user_type_count))

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('\nThe gender breakdown is...\n', pd.DataFrame(gender_count))
    except:
        print('\nNo gender data is available for this dataset.')

    # Display earliest, most recent, and most common year of birth
    try:
        oldest_year = df['Birth Year'].min()
        print('\nThe oldest user was born in...', int(oldest_year))

        youngest_year = int(df['Birth Year'].max())
        print('\nThe youngest user was born in...', int(youngest_year))

        common_year = int(df['Birth Year'].mode())
        print('\nThe year the most common users were born in is...', int(common_year))
    except:
        print('\nNo birth year data is available for this dataset.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data if input is provided by user"""

    pd.set_option('display.max_columns', None)

    raw_data = input('\nWould you like to see the raw data? Enter yes or no.\n')
    start_row = 0
    end_row = 5

    while raw_data.lower() == 'yes':
        print(df.loc[start_row:end_row])
        raw_data = input('\nWould you like to see more raw data? Enter yes or no.\n')
        start_row += 5
        end_row += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
