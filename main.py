#!/usr/bin/env pybricks-micropython

from config import TRAINING
from train import learn
from line_follower import run

if(TRAINING):
    learn()

run()
