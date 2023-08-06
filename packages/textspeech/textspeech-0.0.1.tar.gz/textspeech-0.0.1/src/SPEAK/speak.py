class Speaker(__import__("PyQt5.QtTextToSpeech").QtTextToSpeech.QTextToSpeech):
    def __init__(self):
        """A speaker. Mainly uses PyQt5 to work."""
        super(Speaker, self).__init__()
    def speak(self, text):
        'Speak.'
        self.say(text)
class Voice(__import__("PyQt5.QtTextToSpeech").QtTextToSpeech.QVoice):
    def __init__(self):
        """A voice. Mainly uses PyQt5 to work."""
        super(Voice, self).__init__()
