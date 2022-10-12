import time


def topic_subscription(topic_name):
    return topic_name + "-topic_subscription"


class Dialog:

    def __init__(self, robot):
        self.__al_tts = robot.ALTextToSpeech
        self.__al_audio = robot.ALAudioDevice
        self.__al_dialog = robot.session.service("ALDialog")
        self.__session_id = 420  # generating a random id and storing that instead of hardcoding it for all Dialogs would be better
        self.__al_dialog.openSession(self.__session_id)

    def say(self, text):
        self.__al_tts.say(text)

    def say_slowly(self, text):
        original_speed = self.__al_tts.getParameter("speed")
        self.__al_tts.setParameter("speed", 50)
        self.__al_tts.say(text)
        self.__al_tts.setParameter("speed", original_speed)

    def shout(self, text):
        original_volume = self.__al_audio.getOutputVolume()
        self.__al_audio.setOutputVolume(min(original_volume + 20, 100))
        original_pitch = self.__al_tts.getParameter("pitch")
        pitch = 80
        self.__al_tts.setParameter("pitch", pitch)
        self.__al_tts.say(text)
        self.__al_tts.setParameter("pitch", original_pitch)
        self.__al_audio.setOutputVolume(original_volume)

    def add_simple_reaction(self, topic_name, user_input, robot_output):
        topic_content = ('topic: ~' + topic_name + '()\n'
                                                   'language: enu\n'
                                                   'u:(' + user_input + ') ' + robot_output + '\n')
        self.__al_dialog.loadTopicContent(topic_content)
        return topic_name

    def load_yes_no_question(self, question, reaction_yes, reaction_no):
        topic_name = "".join(question.replace(",", "").replace(".", "").replace(";", "").replace("?", "")
                             .replace("!", "").replace('"', "").replace("'", "").replace("-", "").replace("_", "")
                             .split())
        topic_content = ('topic: ~' + topic_name + '()\n'
                         'language: enu\n'
                         'proposal: ' + question + '\n'
                         'u1: (yes) ' + reaction_yes + ' $agree=1' + '\n'
                         'u1: (no) ' + reaction_no + ' $agree=0')
        self.__al_dialog.loadTopicContent(topic_content)
        return topic_name

    def ask_yes_no_question(self, question, reaction_yes, reaction_no, max_wait_time=5, poll_interval=.1, default=False):
        topic = self.load_yes_no_question(question, reaction_yes, reaction_no)
        self.__al_dialog.insertUserData("agree", '', self.__session_id)  # ensure we don't use the previous result if no input is given
        self.start_topic(topic)
        self.__al_dialog.forceOutput()  # start proposal sentence
        agreed = None  # getUserData returns a string so ''=nothing, '1'=True, '0'=False, note: only '' is falsly
        if max_wait_time <= 0:
            while not agreed:
                agreed = self.__al_dialog.getUserData("agree", self.__session_id)
                time.sleep(poll_interval)
        else:
            for _ in range(int(max_wait_time / poll_interval)):
                agreed = self.__al_dialog.getUserData("agree", self.__session_id)
                if agreed:
                    break
                time.sleep(poll_interval)

        if not agreed:  # no answer within max_wait_time
            self.__al_dialog.forceInput("yes" if default else "no")
            agreed = default
        else:
            agreed = bool(int(agreed))

        self.stop_topic(topic)
        self.__al_dialog.unloadTopic(topic)

        return agreed

    def start_topic(self, topic_name):
        self.__al_dialog.activateTopic(topic_name)
        self.__al_dialog.setFocus(topic_name)
        self.__al_dialog.subscribe(topic_subscription(topic_name))

    def stop_topic(self, topic_name):
        self.__al_dialog.unsubscribe(topic_subscription(topic_name))
        self.__al_dialog.deactivateTopic(topic_name)

    def close_session(self):
        self.__al_dialog.closeSession()
