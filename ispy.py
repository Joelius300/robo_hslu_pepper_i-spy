import itertools
import random
import time
from tempfile import TemporaryFile, NamedTemporaryFile

import almath

from comp_vision.rpc_comp_vision import detect_objects, parents, print_objects, WhatAGreatLanguage
from exercises.camera import Camera
from exercises.dialog import Dialog
from exercises.file_transfer import FileTransfer
from exercises.speech_recognition import SpeechRecognition
from ispy_answers import Responses
from pepper_robots import PepperConfiguration, Robot, PepperNames


# staticmethod cannot be called cleanly from within class -> module scope
def _simplify_objects(detected_objects):
    return map(
        lambda o: WhatAGreatLanguage(
            {"name": o.object_property, "parents": list(parents(o)), "confidence": o.confidence}), detected_objects)


def _choose_random_object(detected_objects, confidence_threshold=.5, uniform_selection_chance=True):
    filtered_objects = filter(lambda o: o.confidence >= confidence_threshold, detected_objects)
    if uniform_selection_chance:
        filtered_objects = sorted(filtered_objects, key=lambda o: o.name)  # must sort before grouping because wtf
        groups = itertools.groupby(filtered_objects, lambda o: o.name)  # CANNOT MAKE TO LIST BEFORE ITERATING GROUPS! WTF
        filtered_objects = [sorted(g, key=lambda o: o.confidence, reverse=True)[0] for (k, g) in groups]

    return random.choice(filtered_objects)


def _get_guessing_function(exact_phrases, close_phrases, abortion_phrases, exact_callback, close_callback,
                           abortion_callback, miss_callback):
    def guess(g):
        [guessed_object, accuracy] = g
        print("recognized the phrase '" + guessed_object + "' with accuracy: " + str(accuracy))

        if accuracy <= .4:
            return

        guessed_object = guessed_object.lower()

        if guessed_object in exact_phrases:
            exact_callback(guessed_object)
        elif guessed_object in close_phrases:
            close_callback(guessed_object)
        elif guessed_object in abortion_phrases:
            abortion_callback(guessed_object)
        else:
            miss_callback(guessed_object)

    return guess


def _flatten_objects_incl_parents(objects):
    return [o.name.lower() for o in objects] + [p.lower() for l in
                                                map(lambda o: o.parents,
                                                    objects) for p
                                                in l]


class ISpy:
    _pepper_image_folder = "/home/nao/recordings/cameras/top/"
    _image_file = "i_spy.jpg"
    _common_objects = ["chair", "bottle", "computer", "laptop", "table", "clock", "wall clock", "bucket",
                       "person", "pen", "pencil", "glasses", "sunglasses", "toothbrush", "animal", "bear", "cat", "dog",
                       "mouse", "monitor", "tv", "screen", "faucet", "machine", "human", "bag", "backpack",
                       "door", "desk", "whiteboard", "blackboard", "folder", "window",
                       "footwear", "pair", "apple", "banana", "orange", "mango", "lemon"]
    _abortion_phrases = ["i give up", "stop playing", "I can't take it anymore", "I don't know"]

    def __init__(self, robot, rpc_url, keep_temp_files=False, scan_room=False, room_scan_delay=2):
        self._robot = robot
        self._rpc_url = rpc_url
        self.keep_temp_files = keep_temp_files
        self.scan_room = scan_room
        self.room_scan_delay = room_scan_delay
        self._camera = Camera(robot)
        self._file_transfer = FileTransfer(robot)
        self._dialog = Dialog(robot)
        self._responses = Responses()

    def _detect_objects_in_view(self):
        self._camera.take_picture(ISpy._pepper_image_folder, ISpy._image_file)

        pepper_img = NamedTemporaryFile(delete=False, prefix="i-spy-",
                                        suffix=".jpg") if self.keep_temp_files else TemporaryFile()
        with pepper_img:
            self._file_transfer.get(ISpy._pepper_image_folder + ISpy._image_file, pepper_img)
            pepper_img.seek(0)
            detected_objects = detect_objects(pepper_img, self._rpc_url)

        return detected_objects

    def _look_around_the_room(self, callback_each_step, wait_time=1, reset_to_starting_point=True):
        [orig_yaw, orig_pitch] = self._robot.ALMotion.getAngles(['HeadYaw', 'HeadPitch'], useSensors=False)

        # if the original yaw is negative, the first pic should be at -120 since it requires less movement than to go to 120
        inverter = 1 if orig_yaw < 0 else -1
        for pitch in [-10, 25]:
            self._robot.ALMotion.setAngles('HeadPitch', pitch * almath.TO_RAD, .05)
            for yaw in range(9):
                angle_deg = (30 * yaw - 120) * inverter
                self._robot.ALMotion.setAngles('HeadYaw', angle_deg * almath.TO_RAD, .05)
                time.sleep(wait_time)  # waiting _before_ callback to try to avoid shaking
                callback_each_step()
            inverter *= -1

        if reset_to_starting_point:
            self._robot.ALMotion.setAngles('HeadPitch', orig_pitch, .2)
            self._robot.ALMotion.setAngles('HeadYaw', orig_yaw, .2)

    # the higher the wait time the longer it takes obv but the better the pictures and accuracy are too
    def _detect_objects_with_looking_around(self):
        objects = []
        # watch for rate limit: 20 per minute and like 1000 per month
        self._look_around_the_room(lambda: objects.extend(self._detect_objects_in_view()), self.room_scan_delay)
        return objects

    def _detect_objects_in_view_until_something_found(self, wait_time_nothing_recognized):
        while True:
            self._speak("I'm looking, give me a second." + (
                " Since azure is rate limiting us, you have to be patient. Sorry." if self.scan_room else ""))
            objects_in_view = self._detect_objects_with_looking_around() if self.scan_room else self._detect_objects_in_view()
            if objects_in_view:  # python isn't sophisticated enough for a do while loop apparently
                break

            self._speak("I don't recognize anything. Can you move me a bit please? I'll look again in " + str(
                wait_time_nothing_recognized) + " seconds.")
            time.sleep(wait_time_nothing_recognized)

        print_objects(objects_in_view)
        objects_in_view = _simplify_objects(objects_in_view)

        return objects_in_view

    # returns True if the player aborted the game, False/None if not
    def _play_one_game_player_guessing(self, wait_time_nothing_recognized=5):
        objects_in_view = self._detect_objects_in_view_until_something_found(wait_time_nothing_recognized)
        chosen_object = _choose_random_object(objects_in_view, confidence_threshold=.25,
                                              uniform_selection_chance=True)
        print repr(chosen_object)

        self._speak("I spy, with my little eye, something beginning with " + chosen_object.name[0])

        exact_phrases = [chosen_object.name.lower()]
        close_phrases = [p.lower() for p in chosen_object.parents]
        all_object_and_their_parents = _flatten_objects_incl_parents(objects_in_view)
        vocab = all_object_and_their_parents + ISpy._common_objects + ISpy._abortion_phrases

        # <rant>because python, by design, cannot differentiate between variable declaration/initialisation and a simple
        # assignment, you cannot assign values to variables one scope higher unless they're global. In later versions
        # there is a nonlocal keyword to solve this but the fact that this exists alone speaks for how absolutely
        # garbage this language's design is.</rant>
        stopping = [False]
        given_up = [False]

        sr = SpeechRecognition(self._robot, vocab)

        def win_game(_guess):
            self._speak(self._responses.get_correct_response(chosen_object.name), sr)
            stopping[0] = True

        def give_up(_guess):
            self._speak(self._responses.get_give_up_response(chosen_object.name), sr)
            stopping[0] = True
            given_up[0] = True

        guessing_func = _get_guessing_function(exact_phrases, close_phrases, ISpy._abortion_phrases,
                                               win_game,
                                               lambda g: self._speak(self._responses.get_close_response(g), sr),
                                               give_up,
                                               lambda g: self._speak(self._responses.get_wrong_response(g), sr))

        sr.subscribe(guessing_func)

        try:
            while not stopping[0]:
                time.sleep(0.05)

        finally:
            sr.unsubscribe()

        return given_up[0]

    # returns True if the player aborted the game, False/None if not
    def _play_one_game_robot_guessing(self, wait_time_nothing_recognized=5):
        self._speak(
            "Once you're ready, say... I spy with my little eye, something beginning with... then the first letter.")
        # generate "something beginning with [A-Z]"
        vocab = ["something beginning with " + chr(x) for x in range(65, 91)]
        sr = SpeechRecognition(self._robot, vocab, word_spotting=True)
        object_the_player_saw = [None]  # just to reiterate, I dislike python

        def player_object_heard(g):
            print repr(g)
            print str(g)
            [guessed_object, accuracy] = g
            if accuracy >= .5:
                # ends with '{LETTER} <...>'
                # ______________-7________-1
                object_the_player_saw[0] = guessed_object[-7]
            elif guessed_object:  # make sure it's not an empty guess when the speech recognition ends
                self._speak("Sorry, I didn't quite get that.")

        sr.subscribe(player_object_heard)

        try:
            while not object_the_player_saw[0]:
                time.sleep(0.05)
        finally:
            sr.unsubscribe()

        player_guess_beginning_letter = object_the_player_saw[0].lower()
        print(player_guess_beginning_letter)

        while True:
            detected_objects = self._detect_objects_in_view_until_something_found(wait_time_nothing_recognized)
            possible_answers = list(set(filter(lambda w: w.startswith(player_guess_beginning_letter),
                                               _flatten_objects_incl_parents(detected_objects))))

            success = False

            # no guess is made when no possible answers are there -> same flow as no correct guess
            for answer in possible_answers:
                if self._dialog.ask_yes_no_question(self._responses.get_guess_response(answer),
                                                    self._responses.get_win_response(), "Hmm...", max_wait_time=-1):
                    success = True
                    break

            if success:
                break

            self._speak(self._responses.get_lose_response(player_guess_beginning_letter))
            if not self._dialog.ask_yes_no_question(self._responses.get_retry_response(),
                                                    "Yay! Give me a few seconds to look again.",
                                                    "Congratulations on your win then! Thanks for playing.",
                                                    max_wait_time=5):
                return True

        return False

    def play_continuously(self):
        keep_playing_question = " Do you want to keep playing?"
        keep_playing_response = "Great!"
        exit_phrase = "Okay, thanks for playing."

        self._speak("Let's play a game of I spy!")

        def do_turn(players_turn):
            response = self._responses.get_my_turn_response() if players_turn else self._responses.get_your_turn_response()
            player_aborted = self._play_one_game_player_guessing() if players_turn else self._play_one_game_robot_guessing()
            return player_aborted or not self._dialog.ask_yes_no_question(response + keep_playing_question,
                                                                          keep_playing_response, exit_phrase,
                                                                          max_wait_time=10)

        players_turn = True
        stopping = False
        while not stopping:
            stopping = do_turn(players_turn)
            players_turn = not players_turn

    def _speak(self, words, speech_recognition=None):
        if speech_recognition:
            speech_recognition.pause()

        self._dialog.say(words)

        if speech_recognition:
            speech_recognition.unpause()


if __name__ == '__main__':
    config = PepperConfiguration(PepperNames.Ale)
    pepper = Robot(config, full_reset=False, reset_ai=True)

    vbox_host_ip = '10.0.2.2'
    ispy = ISpy(pepper, "http://" + vbox_host_ip + ":42069/", keep_temp_files=True, scan_room=True)

    ispy.play_continuously()
