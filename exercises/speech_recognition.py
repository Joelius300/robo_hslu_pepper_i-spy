class SpeechRecognition(object):

    def __init__(self, robot, vocabulary, word_spotting=False):
        self.subscriber = None
        self.__subscription_id = None
        self.__memory = robot.session.service("ALMemory")
        self.__speech_recognition = robot.session.service("ALSpeechRecognition")
        self.pause()  # need to pause speech recognition to set parameters
        self.__speech_recognition.setLanguage("English")
        self.__speech_recognition.setVocabulary(vocabulary, word_spotting)
        self.unpause()

    def subscribe(self, callback):
        self.subscriber = self.__memory.subscriber("WordRecognized")
        self.__subscription_id = self.subscriber.signal.connect(callback)
        self.__speech_recognition.subscribe("SpeechDetection")
        print('Speech recognition engine started')

    def unsubscribe(self):
        self.__speech_recognition.unsubscribe("SpeechDetection")
        self.subscriber.signal.disconnect(self.__subscription_id)
        self.subscriber = None
        print('Speech recognition engine stopped')

    def pause(self):
        self.__speech_recognition.pause(True)

    def unpause(self):
        self.__speech_recognition.pause(False)
