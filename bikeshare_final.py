import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = {'chicago', 'new york city', 'washington'}

MONTHS = {'january', 'february', 'march', 'april', 'may', 'june', 'all'}

DAYS = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyse.

    Returns:
        (str) city - name of the city to analyse
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter


    """

    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        try:
            city = (input('What city do you want to look at? You can choose between New York City, Chicago or Washington.\n')).lower()
            if city in CITIES:
                break
        finally:
            if city not in CITIES:
                print("I haven't heard of that city.")

    print("Thanks! You've chosen {}".format(city))

    while True:
        try:
            month = (input("What month, from January to June, do you want to look at? If you want to see all months enter 'all'\n")).lower()
            if month in MONTHS:
                break
        finally:
            if month not in MONTHS:
                print("I haven't heard of that month. Make sure to write it out in full.")

    print("Thanks! You've chosen {}".format(month))

    while True:
        try:
            day = (input("What day do you want to look at? If you want to see data from all days enter 'all' \n")).lower()
            if day in DAYS:
                break
        finally:
            if day not in DAYS:
                print("I haven't heard of that day. Make sure to write it out in full.")

    print("")
    print('-'*40)

    print("Retrieving data from: City = {}, Month = {} and Day = {}".format(city, month, day))

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyse
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # extract month and day of week from Start Time to create new columns
        df['month'] = df['Start Time'].dt.month

        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df['day_of_week'] = df['Start Time'].dt.weekday_name

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print("The most common month is {}.".format(most_common_month))

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print("The most common day of the week is {}.".format(most_common_day_of_week))

    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print("The most common start hour is {}:00. This time is displayed in 24h.".format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is {}.".format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is {}.".format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    df['total_trip']= df['Start Station'] + ' to ' + df['End Station']
    most_popular_trip = df['total_trip'].mode()[0]
    print("The most trip is from {}.".format(most_popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration Stats...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    days_tt = total_travel // 84000
    hours_tt = (total_travel - (days_tt*84000)) // 3600
    minutes_tt = (total_travel - (days_tt*84000) - (hours_tt*3600)) // 60
    seconds_tt = (total_travel - (days_tt*84000) - (hours_tt*3600) - (minutes_tt*60))
    print("Total travel time is:" ,days_tt, "days,", hours_tt, "hours,", minutes_tt, "minutes,", seconds_tt, "seconds.")

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    days_mt = mean_travel // 84000
    hours_mt = (mean_travel - (days_mt*84000)) // 3600
    minutes_mt = (mean_travel - (days_mt*84000) - (hours_mt*3600)) // 60
    seconds_mt = (mean_travel - (days_mt*84000) - (hours_mt*3600) - (minutes_mt*60))
    print("Mean travel time is:" ,days_mt, "days,", hours_mt, "hours,", minutes_mt, "minutes,", seconds_mt, "seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)

def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User stats...\n")
    start_time = time.time()

    print("Amount of User Types:")

    print(df['User Type'].value_counts())

    print("\nGender Distribution:")

    if 'Gender' in df.columns:
        print(df['Gender'].value_counts())
        print()
    else:
        print("Unfortunately this data is not available for {}. \n ".format(city))

    print("Birth Year data:")

    if 'Birth Year' in df.columns:

        max_birth_year = int(df['Birth Year'].max())
        print("Most Recent Birth Year is {}".format(max_birth_year))

        min_birth_year = int(df['Birth Year'].min())
        print("Most Earliest Birth Year is {}".format(min_birth_year))

        frequent_birth_year = int(df['Birth Year'].mode()[0])
        print("Most Frequent Birth Year is {}".format(frequent_birth_year))

    else:
        print("Unfortunately this data is not available for {}.".format(city))

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)

def main():
    while True:
        city,month,day = get_filters()
        df = load_data(city,month,day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        i = 0

        while True:

            display_data = input("Enter 'yes' to see five (more) rows of raw data. Enter 'no' to continue.\n").lower()

            try:
                if display_data == 'yes':
                    print(df[i:i+5])
                    i += 5

                if display_data == 'no':
                    break

            finally:
                print("")

        restart = input("Enter 'yes' to explore different data. Enter anything else to quit.\n")
        if restart.lower() != 'yes':
            break

    print("Thank you and have a nice day :)")

if __name__ == "__main__":
	main()

""" Helpful articles

https://stackoverflow.com/questions/39291499/how-to-concatenate-multiple-column-values-into-a-single-column-in-panda-datafram

https://stackoverflow.com/questions/4048651/python-function-to-convert-seconds-into-minutes-hours-and-days/4048773 """
