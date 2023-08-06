#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: ${FILE_NAME}
# Author: Raeid Saqur
# Email: rsaqur@cs.princeton.edu
# Created on: 13/04/2018
#
# This file is part of RSMLKit
# Distributed under terms of the MIT License

import gym

## See complete list of wrappers here:
## https://github.com/openai/gym/tree/master/gym/wrappers

class TimeLimitWrapper(gym.Wrapper):
    """
    :param env: (gym.Env) Gym environment that will be wrapped
    :param max_steps: (int) Max number of steps per episode

    See OpenAI's version: https://github.com/openai/gym/blob/master/gym/wrappers/time_limit.py
    """

    def __init__(self, env, max_steps=100):
        # Call the parent constructor, so we can access self.env later
        super(TimeLimitWrapper, self).__init__(env)
        self.max_steps = max_steps
        # Counter of steps per episode
        self.current_step = 0

    def reset(self):
        """
        Reset the environment
        """
        # Reset the counter
        self.current_step = 0
        return self.env.reset()

    def step(self, action):
        """
        :param action: ([float] or int) Action taken by the agent
        :return: (np.ndarray, float, bool, dict) observation, reward, is the episode over?, additional informations
        """
        self.current_step += 1
        obs, reward, done, info = self.env.step(action)
        # Overwrite the done signal when
        if self.current_step >= self.max_steps:
            done = True
            # Update the info dict to signal that the limit was exceeded
            info['time_limit_reached'] = True
        return obs, reward, done, info