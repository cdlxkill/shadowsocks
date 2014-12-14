#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 cdlxkill
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
import cymysql
import time
import sys
from server_pool import ServerPool
import Config
import json

def add_user_to_sql(user_json_file):
    #id, email, pass, passwd, t, u, d, transfer_enable, port, switch, enalbe, type, last_get_gift_time, last_rest_pass_time
    # PRIMARY KEY (`id`,`port`,'email')
    fp = open(user_json_file, 'r')
    switch = '1'
    enable = '1'
    type = '7'
    last_get_gift_time = '0'
    last_rest_pass_time = '0'
    user_info = json.load(fp)
    conn = cymysql.connect(host=Config.MYSQL_HOST, port=Config.MYSQL_PORT, user=Config.MYSQL_USER,
                           passwd=Config.MYSQL_PASS, db=Config.MYSQL_DB, charset='utf8')
    cur = conn.cursor()
    insert_sql = u"INSERT INTO `user` VALUE ('%d', '%s', '%s', '%s', '%d', '%d', '%d', '%d', '%d', '1' ,'1' ,'7', '0', '0')" \
                 % (user_info['id'], user_info['email'],
                 user_info['pass'], user_info['passwd'],
                 user_info['t'], user_info['u'], user_info['d'],
                 user_info['transfer_enable'], user_info['port'])
    print insert_sql
    print cur
    try:
        cur.execute(insert_sql)
        cur.close()
        conn.commit()
    except:
        logging.warning('db error, user exist! id:[%d] email:[%s] port:[%d]' % (user_info['id'],
                                                                      user_info['email'], user_info['port']))
        pass
    cur = conn.cursor()
    cur.execute("SELECT port, u, d, transfer_enable, passwd, switch, enable FROM user")
    print cur.fetchall()
    conn.close()


add_user_to_sql('./user.json')
