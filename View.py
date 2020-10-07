# 封装gui的类
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtCore import pyqtSignal
from ui.mainwindow import Ui_MainWindow
import myenum


class View(QMainWindow, Ui_MainWindow):
    selected_role = ''
    username = ''
    firstname = ''
    lastname = ''
    email = ''
    password = ''
    confirm = ''
    department = ''
    addSignal = pyqtSignal()
    removeSignal = pyqtSignal(str)
    newSignal = pyqtSignal()
    deleteSignal = pyqtSignal(str)
    updateSignal = pyqtSignal()
    cancelSignal = pyqtSignal()

    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.setupUi(self)
        self.add_button.clicked.connect(self.onAdd)
        self.remove_button.clicked.connect(self.onRemove)
        self.update_user_button.clicked.connect(self.onUpdateUser)
        self.cancel_button.clicked.connect(self.onCancel)
        self.new_button.clicked.connect(self.onNew)
        self.delete_button.clicked.connect(self.onDelete)
        self.rolecombo.currentTextChanged.connect(self.onComboBoxClick)
        self.rolelist.itemClicked.connect(self.onListClick)
        self.tableWidget.itemClicked.connect(self.onTableClick)
        self.first_name_lineedit.textChanged.connect(self.onChanged)
        self.last_name_lineedit.textChanged.connect(self.onChanged)
        self.email_lineedit.textChanged.connect(self.onChanged)
        self.password_edit.textChanged.connect(self.onChanged)
        self.username_lineedit.textChanged.connect(self.onChanged)
        self.department_combo.currentTextChanged.connect(self.onChanged)
        self.confirm_lineedit.textChanged.connect(self.onChanged)
        self.remove_button.setEnabled(False)

    def setRoleList(self, list):
        self.rolelist.clear()
        self.rolelist.addItems(list)

    def setRoleComboBox(self, list):
        self.rolecombo.clear()
        self.rolecombo.addItems(list)

    def setDepartmentComboBox(self, list):
        self.department_combo.clear()
        self.department_combo.addItems(list)

    def onTableClick(self, event):
        if self.tableWidget.rowCount() > 0:
            count = self.tableWidget.currentRow()
            try:
                self.username_lineedit.setText(self.tableWidget.item(count, 0).text())
                self.first_name_lineedit.setText(self.tableWidget.item(count, 1).text())
                self.last_name_lineedit.setText(self.tableWidget.item(count, 2).text())
                self.email_lineedit.setText(self.tableWidget.item(count, 3).text())
                self.department_combo.setCurrentText(self.tableWidget.item(count, 4).text())
                self.password_edit.setText(self.tableWidget.item(count, 5).text())
                # self.confirm_lineedit.setText(self.tableWidget.item(count, 5).text())
            except:
                pass

    def onChanged(self):
        sender = self.sender()
        count = self.tableWidget.currentRow()
        if sender == self.first_name_lineedit:
            if self.tableWidget.item(count, 1):
                self.tableWidget.item(count, 1).setText(self.first_name_lineedit.text())
        elif sender == self.last_name_lineedit:
            if self.tableWidget.item(count, 2):
                self.tableWidget.item(count, 2).setText(self.last_name_lineedit.text())
        elif sender == self.email_lineedit:
            if self.tableWidget.item(count, 3):
                self.tableWidget.item(count, 3).setText(self.email_lineedit.text())
        elif sender == self.username_lineedit:
            if self.tableWidget.item(count, 0):
                self.tableWidget.item(count, 0).setText(self.username_lineedit.text())
        elif sender == self.password_edit:
            if self.tableWidget.item(count, 5):
                self.tableWidget.item(count, 5).setText(self.password_edit.text())
        elif sender == self.confirm_lineedit:
            self.confirm = self.confirm_lineedit.text()
        elif sender == self.department_combo:
            if self.tableWidget.item(count, 4):
                self.tableWidget.item(count, 4).setText(self.department_combo.currentText())

        self.username = self.username_lineedit.text()
        self.firstname = self.first_name_lineedit.text()
        self.lastname = self.last_name_lineedit.text()
        self.email = self.email_lineedit.text()
        self.password = self.password_edit.text()
        self.department = self.department_combo.currentText()

    def onComboBoxClick(self, event):
        if not self.rolecombo.currentText() == myenum.ROLE_NONE_SELECTED:
            self.add_button.setEnabled(True)
        else:
            self.add_button.setEnabled(False)
        self.selected_role = self.rolecombo.currentText()

    def onListClick(self, event):
        if not self.rolelist.currentItem().text() == myenum.ROLE_NONE_SELECTED:
            self.remove_button.setEnabled(True)
        else:
            self.remove_button.setEnabled(False)
        self.rolecombo.setCurrentText(myenum.ROLE_NONE_SELECTED)
        self.selected_role = self.rolelist.currentItem().text()

    def onAdd(self):
        if self.rolecombo.count() > 0:
            if self.rolelist.count() > 0:
                for i in range(self.rolelist.count()):
                    if self.rolelist.item(i).text() == self.rolecombo.currentText():
                        QMessageBox.information(self, '提醒', '已存在')
                        break
                self.rolelist.insertItem(self.rolelist.currentIndex().row() + 1, self.rolecombo.currentText())
            else:
                self.rolelist.addItem(self.rolecombo.currentText())
        self.addSignal.emit()
        self.rolelist.update()

    def onRemove(self):
        if self.rolelist.count() > 0:
            if self.rolelist.currentItem():
                temp = self.rolelist.currentItem().text()
                self.rolelist.takeItem(self.rolelist.currentRow())
                self.removeSignal.emit(temp)
                self.rolelist.update()

    def onNew(self):
        self.tableWidget.insertRow(self.tableWidget.currentIndex().row() + 1)
        self.newSignal.emit()
        self.tableWidget.update()

    def onDelete(self):
        if self.tableWidget.rowCount() > 0:
            temp = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            self.tableWidget.removeRow(self.tableWidget.currentIndex().row())
            self.deleteSignal.emit(temp)
            self.tableWidget.update()

    def onUpdateUser(self):
        self.username = self.username_lineedit.text()
        self.firstname = self.first_name_lineedit.text()
        self.lastname = self.last_name_lineedit.text()
        self.email = self.email_lineedit.text()
        self.password = self.password_edit.text()
        self.department = self.department_combo.currentText()
        if self.password == self.confirm:
            self.updateSignal.emit()
        else:
            QMessageBox.question(self, '请确认', '两次密码不同,请再次确认密码', QMessageBox.Yes | QMessageBox.Yes)

    def onCancel(self):
        self.close()
        self.cancelSignal.emit()

    def getusername(self):
        return self.username

    def currentTextofComboBox(self):
        return self.rolecombo.currentText()

    def currentRowofTableWidget(self):
        return self.tableWidget.currentIndex().row()

    def rowcountofTableWidget(self):
        return self.tableWidget.rowCount()

    def getItemofTableWidget(self, i, j):
        return self.tableWidget.item(i, j)

    def getTextofTableWidget(self, i, j):
        return self.tableWidget.item(i, j).text()

    def getTextofListWidget(self, i):
        return self.rolelist.item(i).text()

    def setItemofTableWidget(self, i, j, item):
        self.tableWidget.setItem(i, j, item)

    def lenofRoleList(self):
        return self.rolelist.count()

    def addRow(self, i):
        self.tableWidget.insertRow(i)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = View()
    m.show()
    app.exit(app.exec_())
