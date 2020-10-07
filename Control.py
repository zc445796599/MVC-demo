# 互相传参，以及对应逻辑的类
import sys
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from Model import Model, Role, RoleVO, UserVO
from View import View
import myenum


class Controller:
    def __init__(self):
        self._model = Model()
        self._view = View()
        self._role = Role()
        self.init()

    def init(self):
        self.view.addSignal.connect(self.add)
        self.view.cancelSignal.connect(self.cancel)
        self.view.updateSignal.connect(self.update)
        self.view.deleteSignal.connect(self.delete)
        self.view.newSignal.connect(self.new)
        self.view.removeSignal.connect(self.remove)
        self.view.tableWidget.itemClicked.connect(self.updaterole)
        self.getdata()

    @property
    def model(self):
        return self._model

    @property
    def view(self):
        return self._view

    @property
    def role(self):
        return self._role

    def getdata(self):
        self.updateuser()
        self.updaterole()
        self.updatelineedit()

    def add(self):
        # model 的Role类需要更新
        self.role.addRoleToUser(self.view.getusername(), self.view.currentTextofComboBox())
        self.updaterole()

    def remove(self, string):
        self.role.removeRolesFromUser(self.view.getusername(), string)
        self.updaterole()

    def new(self):
        self.item = UserVO()
        self.role_item = RoleVO()
        self.model.addItem(self.item)
        self.role.addItem(self.role_item)

    def delete(self, temp):
        for index, value in enumerate(self.model.getUsers()):
            if value.username == temp:
                self.model.deleteItem(self.model.getUsers()[index])
        for index, value in enumerate(self.role.data):
            if value.username == temp:
                self.role.deleteItem(self.role.getUserRoles()[index])

    def update(self):
        is_none = False
        count = self.view.currentRowofTableWidget()

        for i in range(1, self.view.rowcountofTableWidget()):
            for j in range(6):
                if self.view.getItemofTableWidget(i,j) is None:
                    print('有空行')
                    is_none = True
                    break

        if is_none is False:
            self.item.username = self.view.getTextofTableWidget(count, 0)
            self.item.firstname = self.view.getTextofTableWidget(count, 1)
            self.item.lastname = self.view.getTextofTableWidget(count, 2)
            self.item.email = self.view.getTextofTableWidget(count, 3)
            self.item.department = self.view.getTextofTableWidget(count, 4)
            self.item.password = self.view.getTextofTableWidget(count, 5)

            self.role_item.username = self.view.getTextofTableWidget(count, 0)
            self.role_item.roles = []

            update_role_list = []
            item = UserVO(self.view.username, self.view.firstname, self.view.lastname, self.view.email,
                          self.view.password,
                          self.view.department)
            self.model.updateItem(item)

            for i in range(self.view.lenofRoleList()):
                temp = self.view.getTextofListWidget(i)
                update_role_list.append(temp)
            self.role.updateRoles(self.view.username, update_role_list)

    def cancel(self):
        pass

    def updateuser(self):
        if self.model.data:
            for index, value in enumerate(self.model.data):
                item = QTableWidgetItem(value.username)
                self.view.addRow(index)
                self.view.setItemofTableWidget(index, 0,item)
                item = QTableWidgetItem(value.firstname)
                self.view.setItemofTableWidget(index, 1,item)
                item = QTableWidgetItem(value.lastname)
                self.view.setItemofTableWidget(index, 2,item)
                item = QTableWidgetItem(value.email)
                self.view.setItemofTableWidget(index, 3,item)
                item = QTableWidgetItem(value.department)
                self.view.setItemofTableWidget(index, 4,item)
                item = QTableWidgetItem(value.password)
                self.view.setItemofTableWidget(index, 5,item)
        self.view.setRoleComboBox(myenum.RoleList)
        self.view.setDepartmentComboBox(myenum.DeptList)

    def updaterole(self):
        self.view.rolelist.clear()
        if self.role.data:
            for index, value in enumerate(self.role.data):
                if self.view.username == value.username:
                    self.view.setRoleList(value.roles)

    def updatelineedit(self):
        pass

    def run(self):
        self.view.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    c = Controller()
    c.run()
    app.exit(app.exec_())
