class PublicValue:
    '''用来存放公共数值'''
    SQLFileName = 'User'
    SQLUserTable = 'user_information'
    SQLSentence = "select * from user_information where Username='{}' and Passwd='{}';" #注意这边{}两边的''
    SQLInsert = "INSERT INTO user_information(Username, Passwd) \
                 VALUES ({},{});"
    Username = ''
    CurrentGroupNumber = ''
    CurrentFriendName = ''
    Username1 = '张三'
    Username2 = '李四'

    Colors = ['CC6699','CC0066','CC6666','FF0066',
              'FF9966','FF9999','FF99CC','FF99FF',
              'FFCC00','CCFFFF','00CC66','00CCFF']

    def __init__(self):
        pass