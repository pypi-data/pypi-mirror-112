from .mysql import query


class Retrieve:
    def __init__(self, SN):
        self.SN = SN

    def query(self, table, field):
        cmd = 'select `%s` from `%s` where `SN` = %s' % (table, field, self.SN)
        res = query(cmd)
        if len(res) == 1:
            res = res[0]
        return res


class RetrieveBaseInfo(Retrieve):
    def __init__(self, SN):
        super(RetrieveBaseInfo, self).__init__(SN)
        self.IP = self.query('IP')
        self.ID = self.query('ID')
        self.Model = self.query('Model')

    def query(self, field):
        return super(RetrieveBaseInfo, self).query('baseInfo', field)
