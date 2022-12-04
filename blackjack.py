import requests

class deck_api_call:

    def __init__(self, api):
        self.request = requests.get(f"{api}")
        self.response = self.request.json()

class blackJack:
    
    def __init__(self, deckID):
        self.id = deckID
        self.dealerhand = []
        self.hand = []
        self.dealerTotal = 0
        self.total = 0

    def draw_card(self, player):
        cardApiCall = deck_api_call("https://www.deckofcardsapi.com/api/deck/" + self.id + "/draw/?count=1")
        card = cardApiCall.response["cards"][0]["code"]
        cardValue = cardApiCall.response["cards"][0]["value"]

        if cardValue == "ACE":
            cardValue = "11"
        elif cardValue == "JACK" or cardValue == "QUEEN" or cardValue == "KING":
            cardValue = "10"

        if(player):
            self.hand.append(card)
            self.total += int(cardValue)
        else:
            self.dealerhand.append(card)
            self.dealerTotal += int(cardValue)
    
    def deck_shuffle(self):
        shuffleApiCall = deck_api_call("https://www.deckofcardsapi.com/api/deck/"+ self.id +"/shuffle/?remaining=true")
        shuffle = shuffleApiCall.response["remaining"]
        print(str(shuffle) + " cards remaining\n")

if __name__ == "__main__":
    deckApicall = deck_api_call("https://www.deckofcardsapi.com/api/deck/new/")
    game = blackJack(deckApicall.response["deck_id"])

    while(True):

        finalNeeded = True
        userInput = -1
        hit = 1
        player = True
        dealer = False
        game.hand.clear()
        game.dealerhand.clear()
        game.total = 0
        game.dealerTotal = 0

        game.deck_shuffle()
        userInput = int(input("Would you like to play a game of Black Jack? (If yes enter 1, else enter 0):"))

        if userInput == 0:
            exit(0)

        game.draw_card(player)
        game.draw_card(dealer)
        
        print("Your Hand:", game.hand, str(game.total))
        print("Dealer Hand:", game.dealerhand, str(game.dealerTotal))
        print()

        while hit == 1:
            hit = int(input("Would you like to hit or stay? (If hit enter 1, if stay enter 0):"))
            if hit == 1:
                game.draw_card(player)
                print("Your Hand:", game.hand, str(game.total))
                print("Dealer Hand:", game.dealerhand, str(game.dealerTotal))
                print()

            if(game.total > 21):
                print("You lose")
                finalNeeded = False
                hit = -1
        
        while hit == 0:
            game.draw_card(dealer)
            print("Your Hand:", game.hand, str(game.total))
            print("Dealer Hand:", game.dealerhand, str(game.dealerTotal))
            print()
            if(game.dealerTotal > 21):
                print("You win")
                finalNeeded = False
                hit = 1
            elif(game.dealerTotal >= 17):
                hit = 1

        if finalNeeded:
            if(game.dealerTotal > game.total):
                print("You lose")
            elif(game.dealerTotal < game.total):
                print("You win")
            else:
                print("You draw")

