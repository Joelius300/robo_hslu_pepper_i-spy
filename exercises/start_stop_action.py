import time

from speech_recognition import SpeechRecognition


class StartStopAction(object):
    def __init__(self, robot, start_phrase, stop_phrase, run_action, accuracy_threshold=.35):
        self.__start_phrase = start_phrase
        self.__stop_phrase = stop_phrase
        self.__run_action = run_action
        self.__accuracy_threshold = accuracy_threshold
        self.__start = False
        self.__stop = False
        self.__speech_recognition = SpeechRecognition(robot, [start_phrase, stop_phrase], self.__speech_callback)

    def run(self, interval=0):
        self.__speech_recognition.subscribe()

        try:
            while not self.__start:
                time.sleep(0.05)

            while not self.__stop:
                if not self.__run_action():
                    break
                if interval > 0:
                    time.sleep(interval)

        finally:
            self.__speech_recognition.unsubscribe()
            self.__start = False
            self.__stop = False

    def __speech_callback(self, value):
        [phrase, accuracy] = value
        print("recognized the phrase '" + phrase + "' with accuracy: " + str(accuracy))
        if accuracy < self.__accuracy_threshold:
            return

        if phrase == self.__start_phrase:
            print "received start signal"
            self.__start = True
        elif phrase == self.__stop_phrase:
            print "received stop signal"
            self.__stop = True
