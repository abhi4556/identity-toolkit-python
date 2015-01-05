# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple command-line sample for the Gitkit API.

Command-line application that allows upload, download, information inquiries
and deletion of Gitkit user accounts
"""

import hashlib
import hmac
from pprint import pprint
import sys

import gitkitclient


def CalcHmac(hash_key, password, salt):
  func = hmac.new(hash_key, password, hashlib.sha1)
  func.update(salt)
  return func.digest()


def main(argv):
  gitkit_instance = gitkitclient.GitkitClient.FromConfigFile(
      'gitkit-server-config.json')
  command = argv[1]
  if command == 'upload':
    # upload account
    hash_key = 'hash-key'
    user1 = gitkitclient.GitkitUser.FromDictionary({
        'email': '1234@example.com',
        'localId': '1234',
        'salt': 'salt-1',
        'passwordHash': CalcHmac(hash_key, '1111', 'salt-1')
    })
    user2 = gitkitclient.GitkitUser.FromDictionary({
        'email': '5678@example.com',
        'localId': '5678',
        'salt': 'salt-2',
        'passwordHash': CalcHmac(hash_key, '5555', 'salt-2')
    })
    gitkit_instance.UploadUsers('HMAC_SHA1', hash_key, [user1, user2])
  elif command == 'download':
    # download accounts
    for account in gitkit_instance.GetAllUsers(2):
      pprint(vars(account))
  elif command == 'delete':
    # delete account
    gitkit_instance.DeleteUser('1234')
  elif command == 'get':
    # get account info
    pprint(vars(gitkit_instance.GetUserById('1234')))
    pprint(vars(gitkit_instance.GetUserByEmail('5678@example.com')))
  else:
    print 'unknown command'

if __name__ == '__main__':
  if len(sys.argv) <= 1:
    print 'command: upload, download, delete, get'
  else:
    main(sys.argv)
