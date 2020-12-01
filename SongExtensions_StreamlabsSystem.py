import clr, json, os, codecs, re, System
clr.AddReference([asbly for asbly in System.AppDomain.CurrentDomain.GetAssemblies() if "AnkhBotR2" in str(asbly)][0])
import AnkhBotR2

ScriptName = "Bulk Song Add Parameter"
Description = "Adds a parameter to allow bulk adding of songs from playlist via a command."
Creator = "EncryptedThoughts"
Version = "1.0.0"
Website = "twitch.tv/encryptedthoughts"

#---------------------------
#   Define Global Variables
#---------------------------
SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
ReadMe = os.path.join(os.path.dirname(__file__), "README.txt")

#---------------------------------------
# Classes
#---------------------------------------
class Settings(object):
    def __init__(self, SettingsFile=None):
        if SettingsFile and os.path.isfile(SettingsFile):
            with codecs.open(SettingsFile, encoding="utf-8-sig", mode="r") as f:
                self.__dict__ = json.load(f, encoding="utf-8")
        else:
            self.EnableDebug = True

    def Reload(self, jsondata):
        self.__dict__ = json.loads(jsondata, encoding="utf-8")
        return

    def Save(self, SettingsFile):
        try:
            with codecs.open(SettingsFile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8")
            with codecs.open(SettingsFile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8')))
        except:
            Parent.Log(ScriptName, "Failed to save settings to file.")
        return

#---------------------------------------
#   [Required] Initialize Data / Load Only
#---------------------------------------
def Init():
    global ScriptSettings
    ScriptSettings = Settings(SettingsFile)
    ScriptSettings.Save(SettingsFile)

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    ScriptSettings.__dict__ = json.loads(jsonData)
    ScriptSettings.Save(SettingsFile)
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters) 
#---------------------------
def Parse(parseString, userid, username, targetid, targetname, message):

    regex = "\$addsongs\(.*\)"
    item = re.search(regex, parseString)
    if item is not None:
        fileName = item.group().strip()[10:][:-1]

        if ScriptSettings.EnableDebug:
            Parent.Log(ScriptName, fileName)
        filePath = os.path.join(os.path.dirname(__file__) + "\Song Lists", fileName + ".csv")
        if ScriptSettings.EnableDebug:
            Parent.Log(ScriptName, filePath)
        if os.path.isfile(filePath):
            songManager = AnkhBotR2.Managers.GlobalManager.Instance.SongCom
            playlist = list(songManager.PlayList)
            songQueue = list(songManager.SongList)

            if ScriptSettings.EnableDebug:
                SavePlaylistToFile()

            with open(filePath) as f:
                content = f.readlines()
            for data in content:
                songs = data.split(",")

                for song in songs:
                    songName = song.strip()
                    if ScriptSettings.EnableDebug:
                        Parent.Log(ScriptName, songName)
                    if not any(s.Title == songName for s in songQueue):
                        for playlistSong in playlist:
                            if playlistSong.Title == songName:
                                songManager.AddToQueue(playlistSong)

        parseString = parseString.replace(item.group(), "")
        if ScriptSettings.EnableDebug:
            Parent.Log(ScriptName, parseString)

    return parseString

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return

def OpenReadme():
    os.startfile(ReadMe)

def SavePlaylistToFile():
    songManager = AnkhBotR2.Managers.GlobalManager.Instance.SongCom
    playlist = list(songManager.PlayList)

    file = os.path.join(os.path.dirname(__file__), "Playlist.csv")
    Parent.Log(ScriptName, file)
    with open(file, 'w') as f:
        for song in playlist:
            f.write(str(song.Title) + "\n")