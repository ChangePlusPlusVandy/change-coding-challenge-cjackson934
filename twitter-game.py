import tweepy as tw
import re
import random

# set up authorization for tweepy API - enter your own keys to run program
consumer_key = {"YOUR CONSUMER KEY"}
consumer_secret = {"YOUR SECRET CONSUMER KEY"}
access_token = {"YOUR ACCESS TOKEN"}
access_token_secret = {"YOUR SECRET ACCESS TOKEN"}

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth)


# method asks the user for input for which usernames they would like to play the game with
# allows for user to select default users (elon and kanye)
# calls get_tweets to load tweets into list (takes some time)

def get_usernames():
    user_input = input('Please enter two twitter usernames you would like to guess between:\n'
                       'You may enter them without the @ sign and with a space in between.\n'
                       'If you would like to play the default version between Elon Musk and Kayne West,'
                       ' press enter\n')

    if user_input == '':
        username1 = 'elonmusk'
        username2 = 'kanyewest'
    else:
        username1 = user_input.split(' ')[0]
        username2 = user_input.split(' ')[1]
        username1 = username1.strip(' ' '@')
        username2 = username2.strip(' ' '@')

    print(f'Loading tweets from {username1} and {username2}')

    user1_list = get_tweets(username1)
    user2_list = get_tweets(username2)

    guess_tweets(user1_list, user2_list, username1, username2)


# method uses tweepy api to search for and load the full tweets from a given user that are not replies or
# retweets, and filters out links and mentions of other users

def get_tweets(screen_name):
    tweetList = []

    for status in tw.Cursor(api.user_timeline, screen_name=screen_name, include_rts=False, exclude_replies=True,
                            tweet_mode="extended").items():
        status.full_text = re.sub(r"http\S+", "", status.full_text)
        if status.full_text:
            tweetList.append(status.full_text)

    print(len(tweetList))
    return tweetList


# method guess_tweets is the primary game method of the program. It randomly selects one of the lists of users and then
# selects a random tweet and outputs it to the user to guess. Users may guess new tweets as many times as they would
# like. When they are done, their game statistics are displayed.

def guess_tweets(user1_list, user2_list, username1, username2):
    correct_count = 0
    total_count = 0

    play_again = True
    while play_again is True:

        rnd_list = random.choice(['1', '2'])

        correct_user = False

        print("Here's the tweet:")
        if rnd_list == '1':
            correct_user = True
            rnd_tweet = (random.choice(user1_list))
            print(rnd_tweet.strip('\n'))
        else:
            rnd_tweet2 = (random.choice(user2_list))
            print(rnd_tweet2.strip('\n'))

        user_response = input(f"Who tweeted that - {username1} or {username2}? (you may type 1 or 2 or the usernames)")

        if (user_response == username1 or user_response == '1') and correct_user is True:
            correct_count += 1
            total_count += 1
            print("Yay! You guessed correctly")
        elif (user_response == username2 or user_response == '2') and correct_user is False:
            correct_count += 1
            total_count += 1
            print("Yay! You guessed correctly")
        else:
            total_count += 1
            print("Oops, not quite")

        user_play_again = input("Would you like a new tweet to guess again? (y/n)")
        if user_play_again.lower() == 'n':
            play_again = False
            calc_game_stats(correct_count, total_count)


# method calc_game_stats calculates the user's accuracy rate and displays their results and a funny message

def calc_game_stats(correct, total):
    accuracy = (correct / total) * 100

    print("\nHere are your game statistics:")
    if total > 1:
        print(f"You played {total} times and guessed correctly {correct} times!")
        print(f"That is an accuracy rate of {accuracy.__round__(2)}%")
        if accuracy > 75:
            print("yer a wizard!")
        elif accuracy > 50:
            print("pretty decent guessing pal! :)")
        else:
            print("these tweeters have fooled you :(")
    else:
        print("You only played once :( try again sometime!")


def main():
    print('Welcome to Guess the Tweeter!\n'
          '\nYou will enter two twitter usernames (or you can play with the default @elonmusk and @kaynewest)'
          '\nA random tweet will be shown and then you can guess between the users.\n')

    get_usernames()


if __name__ == '__main__':
    main()
