import logging

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QTableView, QDialogButtonBox, QFormLayout

from sportorg import config
from sportorg.gui.dialogs.entry_edit import EntryEditDialog
from sportorg.gui.global_access import GlobalAccess
from sportorg.gui.utils.custom_controls import AdvComboBox
from sportorg.language import _
from sportorg.models.constant import get_race_teams, get_race_groups

from sportorg.models.memory import race


class DialogFilter(QDialog):

    def __init__(self, table=None):
        super().__init__(GlobalAccess().get_main_window())
        if table is not None:
            self.table = table

    def exec(self):
        self.init_ui()
        return super().exec()

    def init_ui(self):
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowIcon(QIcon(config.ICON))
        self.resize(300, 0)
        self.setSizeGripEnabled(False)
        self.setModal(True)

        self.layout = QFormLayout(self)
        
        self.group_label = QtWidgets.QLabel(self)

        self.group_combo = AdvComboBox(self)
        self.group_combo.addItem('')
        self.group_combo.addItems(get_race_groups())
        self.layout.addRow(self.group_label, self.group_combo)

        self.team_label = QtWidgets.QLabel(self)

        self.team_combo = AdvComboBox(self)
        self.team_combo.addItem('')
        self.team_combo.addItems(get_race_teams())
        self.layout.addRow(self.team_label, self.team_combo)
        
        self.status_label = QtWidgets.QLabel(self)

        self.status_combo = AdvComboBox(self)
        self.status_combo.addItem('')
        self.status_combo.addItems([_("DNR"),_("DNS"),_("OK"),_("DSQ"),_("DNF")])
        self.layout.addRow(self.status_label, self.status_combo)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_ok = button_box.button(QDialogButtonBox.Ok)
        self.button_ok.clicked.connect(self.accept)
        self.button_cancel = button_box.button(QDialogButtonBox.Cancel)
        self.button_cancel.clicked.connect(self.reject)

        self.layout.addRow(button_box)

        self.retranslate_ui()

        self.show()

    def accept(self):

        try:
            # apply filter here
            if self.table is not None:
                assert (isinstance(self.table, QTableView))
                proxy_model = self.table.model()
                proxy_model.clear_filter()

                group_column = 4
                team_column = 5

                if GlobalAccess().get_main_window().current_tab == 1:
                    group_column = 2
                    team_column = 3

                proxy_model.set_filter_for_column(group_column, self.group_combo.currentText())
                proxy_model.set_filter_for_column(team_column, self.team_combo.currentText())
                proxy_model.set_filter_for_function(race().result_status_filter, self.status_combo.currentText())

                proxy_model.apply_filter()

                EntryEditDialog.GROUP_NAME = self.group_combo.currentText()
                EntryEditDialog.ORGANIZATION_NAME = self.team_combo.currentText()

                GlobalAccess().get_main_window().refresh()
        except Exception as e:
            logging.error(str(e))

        self.destroy()

    def reject(self):
        self.destroy()

    def retranslate_ui(self):
        self.setWindowTitle(_("Filter Dialog"))
        self.group_label.setText(_("Group"))
        self.team_label.setText(_("Team"))
        self.status_label.setText(_("Status"))
        self.button_ok.setText(_('OK'))
        self.button_cancel.setText(_('Cancel'))
