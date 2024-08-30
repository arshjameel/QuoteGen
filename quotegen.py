from ntscraper import Nitter
import random
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
import threading

class QuoteGenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QuoteGen")
        self.root.minsize(500, 500)
        
        # Initialize tweet list and index
        self.tweet_list = []
        self.current_tweet_index = -1
        
        self.default_font = tkfont.Font(family="Consolas", size=12)  # specify font
        self.bg_color = "#ebdbb2"  # dark background
        self.bg_color_alt = "#fbf1c7"  # light background
        self.fg_color = "#282828"  # text color
        self.root.option_add("*Font", self.default_font)  # apply font to widgets
        self.root.option_add("*Background", self.bg_color)  # apply background color to widgets
        self.root.option_add("*Foreground", self.fg_color)  # apply foreground color to widgets
        self.root.configure(bg=self.bg_color)  # apply background color to the entire program
        
        # Configure grid columns and rows
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)  # column for progress bar
        self.root.grid_columnconfigure(2, weight=0)  # column for the next button
        
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=0)  # row for the progress bar
        self.root.grid_rowconfigure(3, weight=1)  # row for the result label

        self.create_widgets()  # load GUI components
        
        ###--- SPECIFY USERNAMES TO BE SCRAPED ---###
        
        self.hardcoded_usernames = ["thedankoe", "ryanholiday", "QuotesOfNaval", "AlexHormozi", "tferris", "IAmMarkManson"]
        self.start_scraping()
        
        ###---------------------------------------###

    def create_widgets(self):
        # Welcome label
        welcome_label = tk.Label(self.root, text="Welcome to QuoteGen!", font=self.default_font, fg=self.fg_color)
        welcome_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="n")
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(self.root, mode='determinate')
        self.progress_bar.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        self.progress_bar.grid_remove()
        
        # Next button (hidden initially)
        self.next_button = tk.Button(self.root, text="Next", command=self.show_next_tweet, font=self.default_font, bg=self.fg_color, fg=self.bg_color)
        self.next_button.grid(row=2, column=1, padx=10, pady=10, sticky="n")
        self.next_button.grid_remove()
        
        # Result label = tweet
        self.result_label = tk.Label(self.root, text="", justify="left", wraplength=480, font=self.default_font, bg=self.bg_color_alt, fg=self.fg_color)
        self.result_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="n")

    def start_scraping(self):
        self.next_button.grid_remove()  # hide the "Next" button
        self.progress_bar.grid()  # show the loading bar
        self.progress_bar.start()  # start the loading bar
        threading.Thread(target=self.scrape_all_tweets).start()  # scraping done in a new thread to keep the GUI responsive

    def scrape_all_tweets(self):
        scraper = Nitter(log_level=0, skip_instance_check=False)  # initialize the scraper with a nitter instance
        all_tweets = []
        
        for username in self.hardcoded_usernames:
            try:
                tweets = scraper.get_tweets(username, mode='user', number=10) # set number of tweets to fetch per user
                if isinstance(tweets, dict) and 'tweets' in tweets:
                    for tweet in tweets['tweets']:
                            tweet['username'] = username  # Add username to tweet data
                    all_tweets.extend(tweets['tweets'])
                else:
                    for tweet in tweets:
                        tweet['username'] = username  # Add username to tweet data
                    all_tweets.extend(tweets)
            except KeyError as e:
                self.result_label.config(text=f"An error occurred while accessing tweets for {username}: {e}")
            except Exception as e:
                self.result_label.config(text=f"An unexpected error occurred while accessing tweets for {username}: {e}")
        
        self.tweet_list = all_tweets
        if not self.tweet_list:
            self.result_label.config(text="No tweets found for the users.")
            return
        
        self.current_tweet_index = random.randint(0, len(self.tweet_list) - 1) # choose a random index for the first tweet
        self.show_tweet(self.current_tweet_index)  # show the tweet at the chosen index
        
        # Stop and hide the loading bar once fetching is done, then show the "Next" button
        self.progress_bar.stop()
        self.progress_bar.grid_remove()
        self.next_button.grid()
            
    def show_tweet(self, index):
        if self.tweet_list:
            tweet = self.tweet_list[index]
            tweet_handle = tweet.get('username', 'Unknown handle')  # Extract handle
            tweet_date = tweet.get('date', 'Unknown date')  # Extract date
            tweet_text = tweet.get('text', 'No content available')  # Extract tweet content

            tweet_text_display = (
                f"\nFrom: @{tweet_handle}"
                f"\nDate: {tweet_date}"
                f"\nContent: \n\t{tweet_text}\n"
            )
            self.result_label.config(text=tweet_text_display)


    def show_next_tweet(self): # goes to the next tweet in the list in a random order
        if self.tweet_list:
            self.current_tweet_index = random.randint(0, len(self.tweet_list) - 1)
            self.show_tweet(self.current_tweet_index)

def main():
    root = tk.Tk()  # create the main window
    app = QuoteGenApp(root)
    root.mainloop()  # main loop

if __name__ == "__main__":
    main()