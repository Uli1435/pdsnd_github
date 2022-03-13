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
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_city_list = list(CITY_DATA.keys())
    city = input("Please choose one of the three cities, Chicago, New York City "\
                 "or Washington: \n").lower()

    while city not in valid_city_list:
        city = input("The city you have typed is not on the list. \nPlease choose "\
                     "one of the three cities, Chicago, New York City or Washington "\
                     "by typing the whole name of the city: \n").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    print("Nice! You have chosen {}!\n".format(city.title()))

    valid_month_list = ("January", "February", "March", "April", "May", "June", "All")
    month = input("Now choose one month between January and June by "\
                        "typing the month or choose all of them by typing 'All': \n").title()
    while month not in valid_month_list:
        month = input("The word you have typed doesn't much to one of the months "\
                      "from January to June. Please try again: \n").title()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print("You have chosen {}!\n".format(month.title()))

    valid_day_list = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "All")
    day = input("And lastly please choose a day of the week by writing the "\
                      "day or write 'all' for all the days: \n").title()
    while day not in valid_day_list:
        day = input("The word you have typed doesn't much to one of the days of "\
                    "the week or the word 'all'. Please try again: \n").title()
    print("You have chosen {}!\n".format(day.title()))

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
    months_list = ["January", "February", "March", "April", "May", "June"]
    days_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    if city == "new york city":
        nyc = city.replace(" ", "_")
        df = pd.read_csv("{}.csv".format(nyc))
    else:
        #Read the city file that the user choose
        df = pd.read_csv("{}.csv".format(city))

    #Convert column 'Start Time' to DateTime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Create column month and extract month from it
    df['month'] = df['Start Time'].dt.month

    #Create column day and extract day from it
    df['day'] = df['Start Time'].dt.day

    #Filter by month
    if month != 'All':
        month = months_list.index(month) + 1
        df = df[df['month'] == month]

    #Filter by day
    if day != 'All':
        day = days_list.index(day) + 1
        df = df[df['day'] == day]
    #print(df.head())

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    months_list = ["January", "February", "March", "April", "May", "June"]
    days_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # TO DO: display the most common month
    #Display the most common month
    number_of_month = int(df.mode()['month'][0])
    #Choose the name of the month from the list
    month_name = months_list[number_of_month - 1]
    print("The most common month traveled for the city is: {}.\n".format(month_name))

    # TO DO: display the most common day of week
    #Display the most common day
    #number_of_day = int(df.mode()['day'][0])
    #print("The most common day of the week traveled for the city is: {}.\n".format(number_of_day))

    #Make a column for the day of the week and find the most common day
    df['Week day'] = df['Start Time'].dt.weekday
    number_of_day = int(df.mode()['Week day'][0])
    day_name = days_list[number_of_day]
    print("The most common day of the week traveled for the city is: {}.\n".format(day_name))

    # TO DO: display the most common start hour
    #Create a column 'hour' to extract the most common start hour
    df['hour'] = df['Start Time'].dt.hour

    #Convert the most common hour from float to int
    number_of_the_hour = int(df.mode()['hour'][0])

    #Display the most common start hour
    print("The most common start hour for the city is: {}:00 Hours.\n".format(number_of_the_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df.mode()['Start Station'][0]
    print("The most common Start Station for the users is: {}.\n".format(common_start_station))

    # TO DO: display most commonly used end station
    common_end_station = df.mode()['End Station'][0]
    print("The most common End Station for the users is: {}.\n".format(common_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    common_start_end_station = ("'" + df['Start Station'] + "'" + ' and the ' + "'" + df['End Station'] + "'").mode()[0]
    print("The most frequent combination of Start and End Station trip is between "\
          "the: {}.\n".format(common_start_end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time_in_sec = sum(df['Trip Duration'])
    hours = int(total_time_in_sec / 3600)
    minutes = int((total_time_in_sec - 3600 * hours) / 60)
    seconds = total_time_in_sec - 3600 * hours - 60 * minutes
    print("The total time the users traveled is: {} hours {} minutes and {} "\
          "seconds.\n".format(hours, minutes, seconds))
    print("The total time in seconds is: {}\n".format(total_time_in_sec))

    # TO DO: display mean travel time
    mean_time_in_sec = int(df['Trip Duration'].mean())
    print("The average travel time is: {} seconds.\n".format(mean_time_in_sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("User types: {}".format(df["User Type"].unique()))

    # TO DO: Display counts of gender
    print("\nGenders: {}".format(df["Gender"].dropna().unique()))

    # TO DO: Display earliest, most recent, and most common year of birth
    print("\nEarliest year of birth: {}\n".format(int(df["Birth Year"].min())))

    print("Most recent year of birth: {}\n".format(int(df["Birth Year"].max())))

    common_year = int(df['Birth Year'].mode())
    print("Most common year of birth: {}\n".format(common_year))
    #print(df.head())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays raw data, five lines of data. Can cancel any time"""
    line_number = 0

    exit_func = input("\nWould you like to see the raw data? If yes type 'yes', "\
                      "else type 'no'.\n").lower()
    while exit_func != 'no':
        if exit_func == 'yes':
            print(df.iloc[line_number: line_number + 5])
            exit_func = input("\nWould you like to see more data? If yes type "\
                              "'yes', else type 'no' to exit.\n").lower()
            line_number += 5
        else:
            break


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
