import requests
import json
from .user import User
from .module import Module


class Bridge:

    def __init__(self, ip, auth, port=3490, scheme="http", api_prefix="/api/v1/"):
        super().__init__()
        self.auth = auth
        self.ip = ip
        self.port = port
        self.scheme = scheme
        self.api_prefix = api_prefix

    def _post(self, request, data):
        response = requests.post(self.scheme + "://" + self.ip + ":" +
                                 str(self.port) + self.api_prefix + request, data=data, auth=self.auth)
        response.raise_for_status()
        return response

    def _get(self, request):
        response = requests.get(self.scheme + "://" + self.ip + ":" +
                                str(self.port) + self.api_prefix + request, auth=self.auth)
        response.raise_for_status()
        return response

    # Benutzerverwaltung

    def createAdminUser(self, label) -> User:
        data = '{{"label": "{label}"}}'.format(label=label)
        response = self._post("users/new-admin", data).json()
        print(response)
        return User(response["id"], response["password"])

    def createIntegrationUser(self, label):
        data = '{{"label": "{label}"}}'.format(label=label)
        return self._post("users/new-integration", data).json()

    def listUsers(self):
        return self._get("users/list").json()

    def deleteUser(self, user_id):
        data = '{{"id": "{userid}"}}'.format(userid=user_id)
        r = self._post("users/delete", data)
        return r.status_code

    def deleteAllUsers(self):
        r = self._post("users/delete-all", "{}")
        return r.status_code

    def getBridgeToken(self):
        rjson = self._get("users/token").json()
        accessToken = rjson.get("accessToken")
        bridgeId = rjson.get("bridgeId")
        return bridgeId, accessToken

    # Modulverwaltung

    def renameModule(self, module_id, name):
        data = '{{"id":"{moduleid}", "newName":"{name}"}}'.format(
            moduleid=module_id, name=name)
        r = self._post("modules/rename", data)
        return r.status_code

    def setModuleAlias(self, module_id, aliases):
        data = '{{"id":"{moduleid}", "aliases":{aliases}}}'.format(
            moduleid=module_id, aliases=json.dumps(aliases))
        r = self._post("modules/set-aliases", data)
        return r.status_code

    # Modulbenutzung



    def getModuleState(self, id):
        return self._get("modules/show?id={id}&aliases=0".format(id=id)).json()[0]["state"]

    def open(self, id):
        data = '{{"id": "{id}", "command":"open"}}'.format(id=id)
        r = self._post("modules/command", data)
        return r.status_code

    def close(self, id):
        data = '{{"id": "{id}", "command":"close"}}'.format(id=id)
        r = self._post("modules/command", data)
        return r.status_code

    # Bridge-Verwaltung

    def factoryReset(self):
        r = self._post("bridge/factory-reset", "{}")
        return r.status_code

    def connectDrives(self):
        r = self._post("bridge/connect-drives", "{}")
        return r.status_code

    def getKitchenInfo(self):
        return self._get("bridge/kitchen").json()

    def setKitchenState(self, state):
        data = '{{"newKitchenState":"{state}"}}'.format(state=state)
        r = self._post("bridge/set-kitchen-state", data)
        return r.status_code

    # misc

    def getSensorData(self):
        return self._get("sensor/data").json()

    def getBridgeInfo(self):
        return self._get("check").json()


