#!/bin/sh
if   [[  $(nmcli -t -f NAME connection show --active) == "ncist-teacher"  ]];
then 
  /home/xiadengma/miniconda3/envs/auto-ncist-teacher/bin/python /home/xiadengma/code/个人项目/python/auto-ncist-teacher/auto_2.py
fi
