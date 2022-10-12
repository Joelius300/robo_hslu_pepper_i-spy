#!/usr/bin/env python
from enum import Enum
from naoqi import qi
from naoqi_python_wrapper.ALAnimatedSpeech import ALAnimatedSpeech
from naoqi_python_wrapper.ALAudioDevice import ALAudioDevice
from naoqi_python_wrapper.ALAudioPlayer import ALAudioPlayer
from naoqi_python_wrapper.ALAudioRecorder import ALAudioRecorder
from naoqi_python_wrapper.ALAudioSourceLocalization import ALAudioSourceLocalization
from naoqi_python_wrapper.ALAutomaticVolume import ALAutomaticVolume
from naoqi_python_wrapper.ALAutonomousLife import ALAutonomousLife
from naoqi_python_wrapper.ALAutonomousMoves import ALAutonomousMoves
from naoqi_python_wrapper.ALBacklightingDetection import ALBacklightingDetection
from naoqi_python_wrapper.ALBarcodeReader import ALBarcodeReader
from naoqi_python_wrapper.ALBasicAwareness import ALBasicAwareness
from naoqi_python_wrapper.ALBattery import ALBattery
from naoqi_python_wrapper.ALBehaviorManager import ALBehaviorManager
from naoqi_python_wrapper.ALBodyDetection3D import ALBodyDetection3D
from naoqi_python_wrapper.ALBodyTemperature import ALBodyTemperature
from naoqi_python_wrapper.ALChestButton import ALChestButton
from naoqi_python_wrapper.ALChoregrapheRecorder import ALChoregrapheRecorder
from naoqi_python_wrapper.ALCloseObjectDetection import ALCloseObjectDetection
from naoqi_python_wrapper.ALColorBlobDetection import ALColorBlobDetection
from naoqi_python_wrapper.ALConnectionManager import ALConnectionManager
from naoqi_python_wrapper.ALDarknessDetection import ALDarknessDetection
from naoqi_python_wrapper.ALDiagnosis import ALDiagnosis
from naoqi_python_wrapper.ALEngagementZones import ALEngagementZones
from naoqi_python_wrapper.ALExpressiveListening import ALExpressiveListening
from naoqi_python_wrapper.ALFaceDetection import ALFaceDetection
from naoqi_python_wrapper.ALFaceTracker import ALFaceTracker
from naoqi_python_wrapper.ALFastPersonTracking import ALFastPersonTracking
from naoqi_python_wrapper.ALFileManager import ALFileManager
from naoqi_python_wrapper.ALFindPersonHead import ALFindPersonHead
from naoqi_python_wrapper.ALFrameManager import ALFrameManager
from naoqi_python_wrapper.ALFsr import ALFsr
from naoqi_python_wrapper.ALGazeAnalysis import ALGazeAnalysis
from naoqi_python_wrapper.ALHeadPoseAnalysis import ALHeadPoseAnalysis
from naoqi_python_wrapper.ALInfrared import ALInfrared
from naoqi_python_wrapper.ALLandMarkDetection import ALLandMarkDetection
from naoqi_python_wrapper.ALLaser import ALLaser
from naoqi_python_wrapper.ALLauncher import ALLauncher
from naoqi_python_wrapper.ALLeds import ALLeds
from naoqi_python_wrapper.ALLocalization import ALLocalization
from naoqi_python_wrapper.ALLogger import ALLogger
from naoqi_python_wrapper.ALMemory import ALMemory
from naoqi_python_wrapper.ALMotion import ALMotion
from naoqi_python_wrapper.ALMotionRecorder import ALMotionRecorder
from naoqi_python_wrapper.ALMovementDetection import ALMovementDetection
from naoqi_python_wrapper.ALNavigation import ALNavigation
from naoqi_python_wrapper.ALNotificationManager import ALNotificationManager
from naoqi_python_wrapper.ALObjectDetection import ALObjectDetection
from naoqi_python_wrapper.ALPanoramaCompass import ALPanoramaCompass
from naoqi_python_wrapper.ALPeoplePerception import ALPeoplePerception
from naoqi_python_wrapper.ALPhotoCapture import ALPhotoCapture
from naoqi_python_wrapper.ALPreferenceManager import ALPreferenceManager
from naoqi_python_wrapper.ALPreferences import ALPreferences
from naoqi_python_wrapper.ALPwtiUpdate import ALPwtiUpdate
from naoqi_python_wrapper.ALPythonBridge import ALPythonBridge
from naoqi_python_wrapper.ALRecharge import ALRecharge
from naoqi_python_wrapper.ALRedBallDetection import ALRedBallDetection
from naoqi_python_wrapper.ALRedBallTracker import ALRedBallTracker
from naoqi_python_wrapper.ALResourceManager import ALResourceManager
from naoqi_python_wrapper.ALRobotModel import ALRobotModel
from naoqi_python_wrapper.ALRobotPose import ALRobotPose
from naoqi_python_wrapper.ALRobotPosture import ALRobotPosture
from naoqi_python_wrapper.ALSegmentation3D import ALSegmentation3D
from naoqi_python_wrapper.ALSensors import ALSensors
from naoqi_python_wrapper.ALSittingPeopleDetection import ALSittingPeopleDetection
from naoqi_python_wrapper.ALSonar import ALSonar
from naoqi_python_wrapper.ALSoundDetection import ALSoundDetection
from naoqi_python_wrapper.ALSoundLocalization import ALSoundLocalization
from naoqi_python_wrapper.ALSpeechRecognition import ALSpeechRecognition
from naoqi_python_wrapper.ALStore import ALStore
from naoqi_python_wrapper.ALSystem import ALSystem
from naoqi_python_wrapper.ALTextToSpeech import ALTextToSpeech
from naoqi_python_wrapper.ALTouch import ALTouch
from naoqi_python_wrapper.ALTracker import ALTracker
from naoqi_python_wrapper.ALVideoDevice import ALVideoDevice
from naoqi_python_wrapper.ALVideoRecorder import ALVideoRecorder
from naoqi_python_wrapper.ALVisionRecognition import ALVisionRecognition
from naoqi_python_wrapper.ALVisionToolbox import ALVisionToolbox
from naoqi_python_wrapper.ALVisualCompass import ALVisualCompass
from naoqi_python_wrapper.ALVisualSpaceHistory import ALVisualSpaceHistory
from naoqi_python_wrapper.ALWavingDetection import ALWavingDetection
from naoqi_python_wrapper.ALWorldRepresentation import ALWorldRepresentation
from naoqi_python_wrapper.ALFaceCharacteristics import ALFaceCharacteristics
from naoqi_python_wrapper.DCM import DCM

# Class that helps on calling naoqi different modules and methods
# by joining them all in the same place
# This has been half generated, half cleaned up by hand
# Author: Sammy Pfeiffer <Sammy.Pfeiffer at student.uts.edu>
# and updated by Florian Herzog


class PepperNames(Enum):
    Amber = "Amber"
    Pale = "Pale"
    Ale = "Ale"
    Simulation = "Simulation"


class PepperConfiguration(object):
    Name = None
    Ip = None
    Port = 0
    Username = None
    Password = None

    def __init__(self, name, ip="", port=9559):
        self.Name = name
        self.Username = "nao"
        self.Port = port
        if name== PepperNames.Amber:
            self.Ip = "192.168.1.101"
            self.Password = "i1-p2e3p"
        elif name == PepperNames.Pale:
            self.Ip = "192.168.1.103"
            self.Password = "i3-p2e3p"
        elif name == PepperNames.Ale:
            self.Ip = "192.168.1.104"
            self.Password = "i4-p2e3p"
        elif name == PepperNames.Simulation:
            self.Ip = "localhost"
        else:
            self.Ip = ip
            self.Port = port

    @property
    def IpPort(self):
        return self.Ip + ":" + str(self.Port)


class Robot(object):

    def __init__(self, configuration, reset = False):
        self.configuration = configuration
        self.connection_url = "tcp://" + configuration.IpPort
        self.app = qi.Application(["OurProject", "--qi-url=" + self.connection_url])
        self.app.start()
        self.session = self.app.session

        self.ALAnimatedSpeech = ALAnimatedSpeech(self.session)
        self.ALAudioDevice = ALAudioDevice(self.session)
        self.ALAudioPlayer = ALAudioPlayer(self.session)
        self.ALAudioRecorder = ALAudioRecorder(self.session)
        self.ALAutonomousLife = ALAutonomousLife(self.session)
        self.ALBacklightingDetection = ALBacklightingDetection(self.session)
        self.ALBarcodeReader = ALBarcodeReader(self.session)
        self.ALBasicAwareness = ALBasicAwareness(self.session)
        self.ALBattery = ALBattery(self.session)
        self.ALBehaviorManager = ALBehaviorManager(self.session)
        self.ALBodyTemperature = ALBodyTemperature(self.session)
        self.ALChestButton = ALChestButton(self.session)
        self.ALColorBlobDetection = ALColorBlobDetection(self.session)
        self.ALConnectionManager = ALConnectionManager(self.session)
        self.ALDarknessDetection = ALDarknessDetection(self.session)
        self.ALDiagnosis = ALDiagnosis(self.session)
        self.ALEngagementZones = ALEngagementZones(self.session)
        self.ALFaceDetection = ALFaceDetection(self.session)
        self.ALFaceCharacteristics = ALFaceCharacteristics(self.session)
        self.ALFsr = ALFsr(self.session)
        self.ALGazeAnalysis = ALGazeAnalysis(self.session)
        self.ALLandMarkDetection = ALLandMarkDetection(self.session)
        self.ALLaser = ALLaser(self.session)
        self.ALLeds = ALLeds(self.session)
        self.ALLocalization = ALLocalization(self.session)
        self.ALMemory = ALMemory(self.session)
        self.ALMotion = ALMotion(self.session)
        self.ALMovementDetection = ALMovementDetection(self.session)
        self.ALNavigation = ALNavigation(self.session)
        self.ALNotificationManager = ALNotificationManager(self.session)
        self.ALPeoplePerception = ALPeoplePerception(self.session)
        self.ALPhotoCapture = ALPhotoCapture(self.session)
        self.ALPreferenceManager = ALPreferenceManager(self.session)
        self.ALRedBallDetection = ALRedBallDetection(self.session)
        self.ALRedBallTracker = ALRedBallTracker(self.session)
        self.ALResourceManager = ALResourceManager(self.session)
        self.ALRobotPosture = ALRobotPosture(self.session)
        self.ALSegmentation3D = ALSegmentation3D(self.session)
        self.ALSensors = ALSensors(self.session)
        self.ALSittingPeopleDetection = ALSittingPeopleDetection(self.session)
        self.ALSonar = ALSonar(self.session)
        self.ALSoundDetection = ALSoundDetection(self.session)
        self.ALSoundLocalization = ALSoundLocalization(self.session)
        self.ALSpeechRecognition = ALSpeechRecognition(self.session)
        self.ALSystem = ALSystem(self.session)
        self.ALTextToSpeech = ALTextToSpeech(self.session)
        self.ALTouch = ALTouch(self.session)
        self.ALTracker = ALTracker(self.session)
        self.ALVideoDevice = ALVideoDevice(self.session)
        self.ALVideoRecorder = ALVideoRecorder(self.session)
        self.ALVisionRecognition = ALVisionRecognition(self.session)
        self.ALVisualCompass = ALVisualCompass(self.session)
        self.ALVisualSpaceHistory = ALVisualSpaceHistory(self.session)
        self.ALWavingDetection = ALWavingDetection(self.session)
        self.ALWorldRepresentation = ALWorldRepresentation(self.session)
        self.ALAudioSourceLocalization = ALAudioSourceLocalization(self.session)
        self.ALAutomaticVolume = ALAutomaticVolume(self.session)
        self.ALAutonomousMoves = ALAutonomousMoves(self.session)
        self.ALBodyDetection3D = ALBodyDetection3D(self.session)
        self.ALChoregrapheRecorder = ALChoregrapheRecorder(self.session)
        self.ALCloseObjectDetection = ALCloseObjectDetection(self.session)
        self.ALExpressiveListening = ALExpressiveListening(self.session)
        self.ALFaceTracker = ALFaceTracker(self.session)
        self.ALFastPersonTracking = ALFastPersonTracking(self.session)
        self.ALFileManager = ALFileManager(self.session)
        self.ALFindPersonHead = ALFindPersonHead(self.session)
        self.ALFrameManager = ALFrameManager(self.session)
        self.ALHeadPoseAnalysis = ALHeadPoseAnalysis(self.session)
        self.ALInfrared = ALInfrared(self.session)
        self.ALLauncher = ALLauncher(self.session)
        self.ALLogger = ALLogger(self.session)
        self.ALMotionRecorder = ALMotionRecorder(self.session)
        self.ALObjectDetection = ALObjectDetection(self.session)
        self.ALPanoramaCompass = ALPanoramaCompass(self.session)
        self.ALPreferences = ALPreferences(self.session)
        self.ALPwtiUpdate = ALPwtiUpdate(self.session)
        self.ALPythonBridge = ALPythonBridge(self.session)
        self.ALRecharge = ALRecharge(self.session)
        self.ALRobotModel = ALRobotModel(self.session)
        self.ALRobotPose = ALRobotPose(self.session)
        self.ALStore = ALStore(self.session)
        self.ALVisionToolbox = ALVisionToolbox(self.session)
        self.DCM = DCM(self.session)

        if reset:
            if self.ALAutonomousLife.getState() != "disabled":
                self.ALAutonomousLife.setState("disabled")
            self.ALRobotPosture.goToPosture("StandInit", 0.5)
            self.ALTextToSpeech.setLanguage("English")
            self.ALTextToSpeech.setVolume(0.3)

