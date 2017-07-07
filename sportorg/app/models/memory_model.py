import sys

from sportorg.language import _
import traceback
from datetime import timedelta

from PyQt5.QtCore import QVariant, QAbstractTableModel, Qt, QSortFilterProxyModel

from sportorg.app.models.memory import race, Result, Group, Course, Organization


class AbstractSportOrgMemoryModel (QAbstractTableModel):
    """
    Used to specify common table behavior
    """
    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.get_headers())

    def get_headers(self):
        pass


class PersonMemoryModel(AbstractSportOrgMemoryModel):
    def __init__(self):
        super().__init__()

    def rowCount(self, parent=None, *args, **kwargs):
        ret = len(race().persons)
        return ret

    def get_headers(self):
        return ['Surname', 'Name', 'Sex', 'Qualification', 'Group', 'Team', 'Year', 'Bib', 'Card', 'Rented card',
                'Comment', 'World code', 'National code', 'Out of competition']

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            # start = time.time()
            # answer = str(index.row()) + ' ' + str(index.column())
            answer = ''
            try:
                answer = self.get_participation_data(index.row())[index.column()]
            except:
                traceback.print_exc()

            # end = time.time()
            # logging.info('Data() ' + str(index.row()) + ' ' + str(index.column()) + ': ' + str(end - start) + ' s')
            return QVariant(answer)

        return QVariant()

    def headerData(self, index, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            columns = self.get_headers()
            return _(columns[index])

    def get_participation_data(self, position):
        return self.get_value_from_object(race().persons[position])

    def get_value_from_object(self, object):
        ret = list()
        person = object

        ret.append(person.surname)
        ret.append(person.name)
        ret.append(person.sex)
        ret.append(person.qual)
        if person.group is None:
            ret.append('')
        else:
            ret.append(person.group.name)
        if person.organization is None:
            ret.append('')
        else:
            ret.append(person.organization.name)
        ret.append(person.year)
        ret.append(person.bib)
        ret.append(person.card_number)
        ret.append('rented stub')
        ret.append(person.comment)
        ret.append(person.world_code)
        ret.append(person.national_code)

        out_of_comp_status = ''
        if person.is_out_of_competition:
            out_of_comp_status = 'o/c'
        ret.append(out_of_comp_status)


        return ret

    def update_one_object(self, part, index):
        self.values[index] = self.get_values_from_object(part)


class ResultMemoryModel(AbstractSportOrgMemoryModel):
    def __init__(self):
        super().__init__()
        self.values = None
        self.count = None

    def rowCount(self, parent=None, *args, **kwargs):
        return len(race().results)

    def get_headers(self):
        return ['Surname', 'Name', 'Group', 'Team', 'Bib', 'Start', 'Finish', 'Result', 'Status', 'Penalty', 'Place']

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            # start = time.time()
            # answer = str(index.row()) + ' ' + str(index.column())
            answer = ''
            try:
                answer = self.get_participation_data(index.row())[index.column()]
            except:
                print(sys.exc_info())
                traceback.print_exc()

            # end = time.time()
            # logging.info('Data() ' + str(index.row()) + ' ' + str(index.column()) + ': ' + str(end - start) + ' s')
            return QVariant(answer)

        return QVariant()

    def headerData(self, index, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            columns = self.get_headers()
            return _(columns[index])

    def get_participation_data(self, position):
        ret = self.get_values_from_object(race().results[position])
        return ret

    def get_values_from_object(self, result):
        i = result
        assert (isinstance(i, Result))
        person = i.person

        return list([
            person.surname,
            person.name,
            person.group.name,
            person.organization.name,
            person.bib,
            i.start_time.strftime('%H:%M:%S'),
            i.finish_time.strftime('%H:%M:%S'),
            i.get_result(),
            i.status,
            i.penalty_time,
            i.place])

    def update_one_object(self, part, index):
        self.values[index] = self.get_values_from_object(part)


class GroupMemoryModel(AbstractSportOrgMemoryModel):
    def __init__(self):
        super().__init__()

    def rowCount(self, parent=None, *args, **kwargs):
        return len(race().groups)

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            answer = ''
            try:
                answer = self.get_data(index.row())[index.column()]
            except:
                traceback.print_exc()

            return QVariant(answer)

        return QVariant()

    def get_headers(self):
        return ['Name', 'Full name', 'Course name', 'Course type', 'Length', 'Point count', 'Climb', 'Sex', 'Min age', 'Max age',\
                'Start interval', 'Start corridor', 'Order in corridor']

    def headerData(self, index, orientation, role=None):

        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            columns = self.get_headers()
            return _(columns[index])

    def get_data(self, position):
        ret = self.get_values_from_object(race().groups[position])
        return ret

    def get_values_from_object(self, group):
        assert (isinstance(group, Group))
        course = group.course
        assert (isinstance(course, Course))
        if course is None:
            course = Course()

        control_count = 0
        if course.controls is not None:
            control_count = len (course.controls)

        return list([
            group.name,
            group.long_name,
            course.name,
            course.type,
            course.length,
            control_count,
            course.climb,
            group.sex,
            group.min_age,
            group.max_age,
            group.start_interval,
            group.start_corridor,
            group.order_in_corridor,
        ])

    def update_one_object(self, part, index):
        self.values[index] = self.get_values_from_object(part)


class CourseMemoryModel(AbstractSportOrgMemoryModel):
    def __init__(self):
        super().__init__()

    def rowCount(self, parent=None, *args, **kwargs):
        return len(race().courses)

    def get_headers(self):
        return ['Name', 'Course type', 'Length', 'Point count', 'Climb', 'Controls']

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            answer = ''
            try:
                answer = self.get_data(index.row())[index.column()]
            except:
                traceback.print_exc()

            return QVariant(answer)

        return QVariant()

    def headerData(self, index, orientation, role=None):

        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            columns = self.get_headers()
            return _(columns[index])

    def get_data(self, position):
        ret = self.get_values_from_object(race().courses[position])
        return ret

    def get_values_from_object(self, course):
        assert (isinstance(course, Course))
        if course is None:
            course = Course()

        return list([
            course.name,
            course.type,
            course.length,
            len(course.controls),
            course.climb,
            ' '.join(course.get_code_list())
        ])

    def update_one_object(self, part, index):
        self.values[index] = self.get_values_from_object(part)


class TeamMemoryModel(AbstractSportOrgMemoryModel):
    def __init__(self):
        super().__init__()

    def rowCount(self, parent=None, *args, **kwargs):
        return len(race().organizations)

    def get_headers(self):
        return ['Name', 'Address', 'Country', 'Region', 'City', 'Contact']

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            answer = ''
            try:
                answer = self.get_data(index.row())[index.column()]
            except:
                traceback.print_exc()

            return QVariant(answer)

        return QVariant()

    def headerData(self, index, orientation, role=None):

        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            columns = self.get_headers()
            return _(columns[index])

    def get_data(self, position):
        ret = self.get_values_from_object(race().organizations[position])
        return ret

    def get_values_from_object(self, team):
        assert (isinstance(team, Organization))
        if team is None:
            team = Organization()

        return list([
            team.name,
            team.address.street,
            team.country.name,
            team.region,
            team.city,
            team.contact.name
        ])

    def update_one_object(self, part, index):
        self.values[index] = self.get_values_from_object(part)


class PersonProxyModel(QSortFilterProxyModel):

    def __init__(self, parent):
        super(PersonProxyModel, self).__init__(parent)
        self.filter_map = None
        self.filter_applied = False

    def clear_filter(self):
        self.filter_map = list()
        for i in range(self.sourceModel().columnCount()):
            self.filter_map.append('')
        self.filter_applied = False

    def set_filter_for_column(self, column, filter_string):
        if self.filter_map is None:
            self.clear_filter()
        self.filter_map[column] = filter_string
        self.invalidateFilter()
        self.filter_applied = True

    def filterAcceptsRow(self, row, index):
        if not self.filter_applied:
            return True
        try:
            source_model = self.sourceModel()
            size = source_model.columnCount()
            for i in range(size):
                if self.filter_map is not None and self.filter_map[i] is not None and self.filter_map[i] != '':
                    filter_string = self.filter_map[i]
                    cell = source_model.data(source_model.index(row, i), Qt.DisplayRole)
                    if str(cell.value()).find(filter_string) == -1:
                        return False
        except:
            print(sys.exc_info())
            traceback.print_exc()
        return True