import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def input_data(input_message, input_error, list_compare):
    error = 1
    while (error == 1):
        data = input(input_message).lower()
        if (data in list_compare):
            error = 0
        else:
            print(input_error)
    return data.lower()

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    cities = ["chicago", "new york city", "washington"]
    city = input_data("Enter your city: ", "Error, invalid city name",cities)
    months = ["all","january","february","march","april","may","june"]
    month = input_data("Enter the month (all, january, february, ... , june): ","Error, invalid month",months)
    days = ["all","monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    day = input_data("Enter your day of week (all, monday, tuesday, ... sunday): ", "Error, invalid day", days)
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
    df = pd.read_csv(CITY_DATA[city.lower()],parse_dates = ['Start Time', 'End Time'])
    labels = []

    for column_name in df.columns:
        new_col = column_name.replace(' ', '').lower()
        labels.append(new_col)
    df.columns = labels
    months = {"january":1,"february":2,"march":3,"april":4,"may":5,"june":6}
    days = {"monday":0,"tuesday":1,"wednesday":2,"thursday":3,"friday":4,"saturday":5,"sunday":6}
    if (month.lower() == "all" and day.lower() == "all"):
        pass
    else:

        if (month.lower() != "all" and day.lower() != "all"):
            month_mask = df['starttime'].map(lambda x: x.month) == months[month.lower()]
            day_mask = df['starttime'].map(lambda x: x.weekday()) == days[day.lower()]
            df = df[month_mask & day_mask]
        else if (month.lower() != "all"):
            month_mask = df['starttime'].map(lambda x: x.month) == months[month.lower()]
            df = df[month_mask]
        elif (day.lower() != "all"):
            day_mask = df['starttime'].map(lambda x: x.weekday()) == days[day.lower()]
            df = df[day_mask]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
        start_time = time.time()
    try:
        months = ["January","February","March","April","May","June"]
        print("Most common month " + months[int(df['starttime'].dt.month.mode()) - 1])

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                        'Saturday', 'Sunday']
        print("Most common day of week " + days[int(df['starttime'].dt.dayofweek.mode())])

        print("Most common start hour " + str(datetime.time(df['starttime'].dt.hour.mode())))
    except:
        print("Nothing found!")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    try:

        print("Most commonly used start station " + df['startstation'].mode().to_string(index = False))
        print("Most commonly used end station " + df['endstation'].mode().to_string(index = False))
        df['trip'] = df['startstation'].str.cat(df['endstation'], sep=' -> ')
        print("Most frequent combination of start station and end station trip " + df['trip'].mode().to_string(index = False))
    except:
        print("Nothing found!")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    try:
        print("Total travel time " + str(datetime.timedelta(seconds=int(df['tripduration'].sum()))))
        print("Mean travel time " + str(datetime.timedelta(seconds=int(df['tripduration'].mean()))))
    except:
        print("Nothing found!")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    try:
        print("Count user type = Suscriber " + str(df.query('usertype == "Subscriber"').usertype.count()))
        print("Count user type = Customer " + str(df.query('usertype == "Customer"').usertype.count()))
        print("Count user gender = Male " + str(df.query('gender == "Male"').gender.count()))
        print("Count user gender = Female " + str(df.query('gender == "Female"').gender.count()))
        print("Earliest year of birth " + str(int(df['birthyear'].min())))
        print("Most recent year of birth " + str(int(df['birthyear'].max())))
        print("Most common year of birth " + str(df['birthyear'].mode().to_string(index = False)))
    except:
        print("Nothing found!")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#
def raw_data_user_stats(df):
    counter1=0
    counter2=5
    answer = input('Would you like to see 5 lines of raw data? Enter yes or no: ').lower()
    while True:

        if answer == 'yes':
            print(df.iloc[counter1:counter2])
            counter1+=5
            counter2+=5
            answer = input('Would you like to see 5 more lines of raw data? Enter yes or no: ').lower()
        if answer == 'no':
            break
        else if answer not in ['yes','no']:
            answer = input ('input invalid, please enter yes or no')
def main():
    while True:

        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_user_stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
               break
        else:
            break
if __name__ == "__main__":
    main()









## Change 1 as refactoring
## Change 2 as refactoring branch
