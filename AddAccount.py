import pickle
import poplib
import sys
from importlib import reload
#Parser用于创建子消息对象
from email.parser import Parser
from email.parser import BytesParser
#header用于支持非ASCII字符编码，RS2822仅支持ASCII
from email.header import decode_header
#utils.parseaddr，解析地址
from email.utils import parseaddr
import email.iterators
#提供遍历方法.walk

path = 'F://dowload/account.txt'
filepath = 'F://dowload/'


try:
    account_file = open(path, 'rb')
    print('success')
    account_info = pickle.load(account_file)
    user_list = account_info['user']
    print(user_list)
except:
    account_file = open(path,'wb')
    user_list = []
    password_list = []
    server_list = []
    latest_mail = []
    account_info = {
    'user': user_list,
    'password': password_list,
    'server': server_list,
    'latest_index': latest_mail
    }
    pickle.dump(account_info, account_file)
    account_file.close()


#解析消息头中的字符串
def decode_str(s):
    value, charset = decode_header(s)[0] #解码消息但不改变字符集
    if charset:
        value = value.decode(charset)
    return value


def savefile(filename, data, path):
    try:
        filepath = path + filename
        print('Save as: ' + filepath)
        f = open(filepath, 'wb')
    except:
        print(filepath + ' open failed')
        #f.close()
    else:
        f.write(data)
        f.close()


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos+8:].strip()
    return charset


def print_info(msg):
    for header in ['From', 'To', 'Subject']:
        value = msg.get(header, '')
        if value:
            if header == 'Subject':
                value = decode_str(value)
            else:
                hdr, addr = parseaddr(value)
                name = decode_str(addr)
                value = name + ' < ' + addr + ' > '
        print(header + ':' + value)
    for part in msg.walk():
        filename = part.get_filename()
        content_type = part.get_content_type()
        charset = guess_charset(part)
        if filename:
            filename = decode_str(filename)
            data = part.get_payload(decode = True)
            if filename != None or filename != '':
                print('Accessory: ' + filename)
                savefile(filename, data, filepath)
        else:
            email_content_type = ''
            content = ''
            if content_type == 'text/plain':
                email_content_type = 'text'
            elif content_type == 'text/html':
                email_content_type = 'html'
            if charset:
                content = part.get_payload(decode=True).decode(charset)
            # print(email_content_type + ' ' + content)


def Get_account():
    f = open(path, 'rb')
    account_info = pickle.load(f)
    user_list = account_info['user']
    print(user_list)


def Add_account():
    f = open(path, 'rb')
    account_info = pickle.load(f)
    f.close()
    user_list = account_info['user']
    user = input('请输入用户名：')
    user_list.append(user)
    password_list = account_info['password']
    password = input('请输入密码：')
    password_list.append(password)
    server_list = account_info['server']
    server = input('请输入服务器地址：')
    server_list.append(server)
    latest_mail = account_info['latest_index']
    length = len(user_list)
    print(length)
    i = 0
    while i < length:
        user = user_list[i]
        password = password_list[i]
        server = server_list[i]
        pop3_server = poplib.POP3(server)
        pop3_server.user(user)
        pop3_server.pass_(password)
        resp, mails, objects = pop3_server.list()
        index = len(mails)
        latest_mail.append(index)
        pop3_server.quit()
        i += 1
    ff = open(path,'wb')
    pickle.dump(account_info, ff)
    ff.close()


def Fetch_attach():
    f = open(path, 'wb+')
    account_info = pickle.load(f)
    user_list = account_info['user']
    password_list = account_info['password']
    server_list = account_info['server']
    latest_mail = account_info['latest_index']
    length = len(user_list)
    i = 0
    while i < length:
        user = user_list[i]
        password = password_list[i]
        server = server_list[i]
        pop3_server = poplib.POP3(server)
        pop3_server.user(user)
        pop3_server.pass_(password)
        print('Message: %s Size: %s' % pop3_server.stat())
        resp, mails, objects = pop3_server.list()
        index = len(mails)
        #判断是否有新邮件
        old_index = latest_mail[i]
        if index > old_index:
            j = old_index
            while j <= index:
                #取出某一个邮件的全部信息
                resp, lines, octets = pop3_server.retr(index)
                #邮件取出的信息是bytes，转换成Parser支持的str
                lists = []
                for e in lines:
                    lists.append(e.decode())
                msg_content = '\r\n'.join(lists)
                msg = Parser().parsestr(msg_content)
                print_info(msg)
                j+=1
            latest_mail[i] = index
            pop3_server.quit()
        else:
            print('没有收到新邮件')
            pop3_server.quit()
        i+=1
    pickle.dump(account_info,f)
    f.close


def List_account():
    Get_account()


def Delete_account():
    f = open(path, 'rb')
    account_info = pickle.load(f)
    f.close()
    user_list = account_info['user']
    password_list = account_info['password']
    server_list = account_info['server']
    print(user_list)
    index = input('请输入删除帐号的序号：')
    del_index = int(index) - 1
    del user_list[del_index]
    del password_list[del_index]
    del server_list[del_index]
    ff = open(path,'wb')
    pickle.dump(account_info, ff)
    ff.close()


start = 1

while start > 0:
    print('请选择命令：')
    print('0:添加账户')
    print('1:下载附件')
    print('2:查看账户列表')
    print('3:删除账户')
    print('4;退出')
    command = input('请输入命令：')
    if command == '0':
        Add_account()
    elif command == '1':
        Fetch_attach()
    elif command == '2':
        List_account()
    elif command == '3':
        Delete_account()
    elif command == '4':
        start = 0

