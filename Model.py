import myenum


class Model:
    def __init__(self):
        self.data = []
        self.addItem(UserVO('lstooge', 'Larry', 'Stooge', 'larry@stooges.com', 'ijk456', myenum.DEPT_ACCT))
        self.addItem(UserVO('cstooge', 'Curly', 'Stooge', 'curly@stooges.com', 'xyz987', myenum.DEPT_SALES))
        self.addItem(UserVO('mstooge', 'Moe', 'Stooge', 'moe@stooges.com', 'abc123', myenum.DEPT_PLANT))

    def getUsers(self):
        return self.data

    def addItem(self, item):
        self.data.append(item)

    def updateItem(self, user):
        if self.data is not None:
            for index, value in enumerate(self.data):
                if value.username == user.username:
                    value = user

    def deleteItem(self, user):
        if self.data is not None:
            for index, value in enumerate(self.data):
                if value.username == user.username:
                    self.data.remove(value)
                    break


class Role(object):
    def __init__(self):
        self.data = []
        self.addItem(RoleVO('lstooge', [myenum.ROLE_PAYROLL, myenum.ROLE_EMP_BENEFITS]))
        self.addItem(RoleVO('cstooge', [myenum.ROLE_ACCT_PAY, myenum.ROLE_ACCT_RCV, myenum.ROLE_GEN_LEDGER]))
        self.addItem(
            RoleVO('mstooge', [myenum.ROLE_INVENTORY, myenum.ROLE_PRODUCTION, myenum.ROLE_SALES, myenum.ROLE_SHIPPING]))

    def getRoles(self):
        return self.data

    def addItem(self, item):
        self.data.append(item)

    def deleteItem(self, item):
        if self.data is not None:
            for index, value in enumerate(self.data):
                if value.username == item.username:
                    self.data.remove(value)
                    break

    def doesUserHaveRole(self, user, role):
        hasRole = False
        if self.data:
            for index, value in enumerate(self.data):
                if value.username == user:
                    userRoles = value.roles
                    for index_1, value_1 in enumerate(userRoles):
                        if value_1 == role:
                            hasRole = True
                            break
        return hasRole

    def addRoleToUser(self, user, role):
        result = False
        if not self.doesUserHaveRole(user, role):
            for index, value in enumerate(self.data):
                if value.username == user:
                    userRoles = value.roles
                    userRoles.append(role)
                    result = True
                    break

    def removeRolesFromUser(self, user, role):
        if self.doesUserHaveRole(user, role):
            for index, value in enumerate(self.data):
                if value.username == user:
                    userRoles = value.roles
                    for index_1, value_1 in enumerate(userRoles):
                        if value_1 == role:
                            userRoles.remove(value_1)
                            break

    def getUserRoles(self, username):
        userRoles = []
        for index, value in enumerate(self.data):
            if value.username == username:
                userRoles = value.roles
                break
        return userRoles

    def updateRoles(self, username, list):
        for index, value in enumerate(self.data):
            if value.username == username:
                value.roles = list


class RoleVO:
    username = None
    roles = []

    def __init__(self, username=None, roles=None):
        if username:
            self.username = username
        if roles:
            self.roles = roles


class UserVO:
    username = None
    firstname = None
    lastname = None
    email = None
    password = None
    department = myenum.DEPT_NONE_SELECTED

    def __init__(self, username=None, firstname=None, lastname=None, email=None, password=None, department=None):
        if username:
            self.username = username
        if firstname:
            self.firstname = firstname
        if lastname:
            self.lastname = lastname
        if email:
            self.email = email
        if password:
            self.password = password
        if department:
            self.department = department

    def isValid(self):
        return (len(self.username) > 0 and len(
            self.password) > 0 and self.department is not myenum.DeptEnum.None_SELECTED)

    def givenName(self):
        return self.lastname + ',' + self.firstname
