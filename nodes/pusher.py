#!/usr/bin/env python
import os
import smbc
import pdb

def my_auth_callback_fn():
	pdb.set_trace()
def pusher():
	ctx = smbc.Context (auth_fn=my_auth_callback_fn)
	file = ctx.open ("smb://davidgitzhomepc/shareddrive/file.txt", os.O_CREAT | os.O_WRONLY)
	file.write ("hello")

if __name__ == '__main__':
    pusher()

