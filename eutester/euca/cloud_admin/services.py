__author__ = 'clarkmatthew'

from boto.resultset import ResultSet
from eutester.euca.cloud_admin import EucaBaseObj
import  time


class EucaServiceType(EucaBaseObj):

    def __init__(self, connection=None):
        super(EucaServiceType, self).__init__(connection)
        self.groupmembers=[]
        self._name = None
        self._componentname = None
        self.description = None
        self.entry = None

    @property
    def name(self):
        if not self._name:
            self._name = getattr(self, 'componentname', None)
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def componentname(self):
        return self._componentname

    @componentname.setter
    def componentname(self, value):
        self._name = value
        self._componentname = value


    def startElement(self, name, value, connection):
        ename = name.replace('euca:','')
        if ename == 'serviceGroupMembers':
            groupmembers = ResultSet([('item', EucaSeviceGroupMember),
                                    ('euca:item', EucaSeviceGroupMember)])
            self.groupmembers = groupmembers
            return groupmembers
        else:
            return None

    def endElement(self, name, value, connection):
        ename = name.lower().replace('euca:','')
        if ename:
            #print 'service type got ename:{0}'.format(ename)
            if ename == 'componentname':
                self.name = value
            setattr(self, ename, value)

class EucaSeviceGroupMember(EucaBaseObj):
    def endElement(self, name, value, connection):
        ename = name.lower().replace('euca:','')
        if ename:
            if ename == 'entry':
                self.name = value
            setattr(self, ename, value)

class EucaServiceGroupMembers(ResultSet):
    def __init__(self, connection=None):
        super(EucaServiceGroupMembers, self).__init__(connection)
        self.markers = [('item', EucaSeviceGroupMember)]

    def __repr__(self):
        return str(self.__class__.__name__) + ":(Count:" + str(len(self)) + ")"

    def startElement(self, name, value, connection):
        ename = name.lower().replace('euca:','')
        print 'group member: name:{0}, value:{1}'.format(name,value)
        if ename == 'item':
            new_member = EucaSeviceGroupMember(connection=connection)
            self.append(new_member)
            return new_member
        else:
            return None

    def endElement(self, name, value, connection):
        ename = name.lower().replace('euca:','')
        if ename:
            setattr(self, ename, value)



class EucaServiceList(ResultSet):

    def __init__(self, connection=None):
        super(EucaServiceList, self).__init__(connection)
        last_updated = time.time()

    def __repr__(self):
        return str(self.__class__.__name__) + ":(Count:" + str(len(self)) + ")"


    def startElement(self, name, value, connection):
        ename = name.replace('euca:','')
        if ename == 'item':
            new_service = EucaService(connection=connection)
            self.append(new_service)
            return new_service
        else:
            return None

    def endElement(self, name, value, connection):
        ename = name.lower().replace('euca:','')
        if ename:
            setattr(self, ename, value)

    def show_list(self, print_method=None):
        for service in self:
            if print_method:
                print_method("{0}:{1}".format(service.type, service.name))
            else:
                print "{0}:{1}".format(service.type, service.name)


class EucaUris(EucaBaseObj):
    # Base Class for Eucalyptus Service Objects
    def __init__(self, connection=None):
        super(EucaUris, self).__init__(connection)
        self.uris=[]

    def startElement(self, name, value, connection):
        elem = super(EucaUris, self).startElement(name, value, connection)
        if elem is not None:
            return elem

    def endElement(self, name, value, connection):
        ename = name.replace('euca:','')
        if ename:
            if ename == 'entry':
                self.uris.append(value)
            else:
                setattr(self, ename, value)

class EucaService(EucaBaseObj):
    # Base Class for Eucalyptus Service Objects
    def __init__(self, connection=None):
        super(EucaService, self).__init__(connection)
        self.name = None
        self.partition = None
        self.uris = []

    def startElement(self, name, value, connection):
        ename = name.replace('euca:','')
        elem = super(EucaService, self).startElement(name,
                                                         value,
                                                         connection)
        if elem is not None:
            return elem
        if ename == 'uris':
            self.uris = EucaUris(connection=connection)
            return self.uris

    def endElement(self, name, value, connection):
        ename = name.replace('euca:','')
        if ename:
            if ename == 'entry':
                self.uris.append(value)
            if ename == '_name':
                if not hasattr(self, 'name') or not self.name:
                    setattr(self, 'name', value)
                setattr(self, ename, value)
            else:
                setattr(self, ename, value)


class EucaCloudControllerService(EucaServiceType):
    pass

class EucaClusterControllerService(EucaServiceType):
    pass

class EucaObjectStorageGatewayService(EucaServiceType):
    pass

class EucaStorageControllerService(EucaServiceType):
    pass
