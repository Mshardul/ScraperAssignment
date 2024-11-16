'''
This module defines the notification handler for the APIs.
'''

class NotificationHandler:
    ''' A class to handle notifications. '''
    def notify(self, scraped_count):
        ''' Notify through the Console log. '''
        print(f"Scraping complete. {scraped_count} products were scraped and stored.")
