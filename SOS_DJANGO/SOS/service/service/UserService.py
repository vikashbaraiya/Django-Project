

from service.models import User
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains User business logics.   
'''


class UserService(BaseService):
    def authenticate(self, params={}):
        userList = self.search2(params)
        if (userList.count() == 1):
            return userList[0]
        else:
            return None

    def search2(self, params):

        q = self.get_model().objects.filter()

        val = params.get("login_id", None)
        if(DataValidator.isNotNull(val)):
            q = q.filter(login_id=val)

        val = params.get("password", None)
        if(DataValidator.isNotNull(val)):
            q = q.filter(password=val)

        return q

    def search(self, params):
        pageNo = (params["pageNo"]-1)*self.pageSize
        sql = "select * from ors_user where 1=1"
        val = params.get("login_id", None)
        if DataValidator.isNotNull(val):
            sql += " and login_id = '"+val+"' "
        sql += " limit %s,%s"
        cursor = connection.cursor()
        print("--------", sql, pageNo, self.pageSize)
        params['index'] = ((params['pageNo'] - 1) * self.pageSize)+1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ("id", "firstName", "lastName", "login_id", "password", "confirmpassword",
                      "dob", "address", "gender", "mobilenumber", "role_Id", "role_Name")
        res = {
            "data": []
        }
        count = 0
        for x in result:
            # print({columnName[i] :  x[i] for i, _ in enumerate(x)})
            print(x)
            params['MaxId'] = x[0]
            res["data"].append({columnName[i]:  x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return User
