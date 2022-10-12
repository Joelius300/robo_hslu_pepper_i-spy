import random


class Responses:
    correct_responses = ["Yes! That's correct! It was {}.", "{}, correct, you are so smart."]
    play_again_responses = ["Would you like to play another round?", "That was so much fun. Let's play again."]
    close_responses = ["Almost {}! Be more precise.", "{} is not precise enough."]
    wrong_responses = ["{} is not what I'm looking for.", "No, {} is not it.", "Keep trying, it's not {}.", "{}, really?"]
    give_up_responses = ["Thanks for playing. The correct guess would have been {}.", "Nerd. I was thinking of the {}."]
    your_turn_responses = ["Now it's your turn.", "Your turn. You can guess my object now."]
    guess_responses = ["Hmm, is it the {}", "I think it's that {} over there.", "Oh I know. It's the {}, am I right?"]
    win_responses = ["Ah yes! That was hard.", "That was fun!", "Oh my god that was so easy hahahaha."]
    lose_responses = ["Huh, I don't see anything starting with {}.",
                      "You said it starts with {}, right? Because I don't see shit.",
                      "I'm stumped. I don't know what it is that could start with {}."]
    retry_responses = ["If you could move me a bit I might be able to see your object better. Would you like me to try again?",
                       "Would you like me to try again? If so, please reply with yes and move me a bit so I can see your object better."]
    my_turn_responses = ["Now it's my turn.", "My turn. I'll guess your object next.", "Okay, My turn now."]

    def __init__(self):
        pass

    def get_correct_response(self, correct_obj):
        return random.choice(self.correct_responses).format(correct_obj)

    def get_play_again_response(self):
        return random.choice(self.play_again_responses)

    def get_close_response(self, guess):
        return random.choice(self.close_responses).format(guess)

    def get_wrong_response(self, guess):
        return random.choice(self.wrong_responses).format(guess)

    def get_give_up_response(self, guess):
        return random.choice(self.give_up_responses).format(guess)

    def get_your_turn_response(self):
        return random.choice(self.your_turn_responses)

    def get_guess_response(self, guess):
        return random.choice(self.guess_responses).format(guess)

    def get_win_response(self):
        return random.choice(self.win_responses)

    def get_lose_response(self, first_letter):
        return random.choice(self.lose_responses).format(first_letter)

    def get_retry_response(self):
        return random.choice(self.retry_responses)

    def get_my_turn_response(self):
        return random.choice(self.my_turn_responses)
