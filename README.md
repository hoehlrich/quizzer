# quizzer
Overview:
- Application to create and show flashcards
- Gui created using tkinter with python

Decks:
- Currently all decks are test decks
- By clicking on the deck name, you initialize a screen that simulates flashcards
    - Press space to "flip" the card
    - Press space again to go to the next card
- Currently all decks are hard coded in main(), hoping to add a deck file/attribute after the school project is completed

Cards:
- Create a card by clicking the add button at the top
- Inits window that allows you to create a card
    - Click on the type box and deck box to set them
        - As of now, the only type of card possible is basic
        - When setting deck, use choose to pick the deck and add to create a new deck
            - Note: you still have to click choose on an added deck
    - Fill out the rest of the box's
        - All boxes are necessart (had to make sure that I could share the json file with other students)
    - Click add to exit the menu
    - To see the newly created card you must click the Decks button again
        - the card will not appear in "all" until you restart the program again

Save:
- After creating or importing cards make sure to click the save button

Import Cards:
- Click import
- Select the .json file with cards to import
- Click open