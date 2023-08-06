import numpy as np
import gym.spaces as spaces
from gym import ObservationWrapper, Wrapper
from gym.spaces import Dict, Box


class FlatEnv(ObservationWrapper):
    r"""Observation wrapper that flattens the observation."""

    def __init__(self, env, keys=None):
        super().__init__(env)

        # todo: allow selecting subsets using keys
        dim = spaces.flatdim(env.observation_space)
        self.observation_space = spaces.Box(low=-float('inf'), high=float('inf'), shape=(dim,), dtype=np.float32)

    def observation(self, observation):
        return spaces.flatten(self.env.observation_space, observation)


class FlatGoalEnv(Wrapper):
    """FlatGoalEnv

    Support both the Fetch environments containing ['observation', 'achieved_goal', 'goal']
    in addition to our sawyer environments using ['hand', 'slot', ...]
    """

    def __init__(self, env, obs_keys=None, goal_keys=None):
        super(FlatGoalEnv, self).__init__(env)

        if obs_keys is None:
            obs_keys = env.obs_keys
        if goal_keys is None:
            goal_keys = env.goal_keys
        for k in obs_keys:
            assert k in env.observation_space.spaces
        for k in goal_keys:
            assert k in env.observation_space.spaces
        assert isinstance(env.observation_space, Dict)

        self.obs_keys = obs_keys
        self.goal_keys = goal_keys

        space = self.unwrapped.observation_space.spaces
        self.observation_space = Box(np.hstack([*[space[k].low for k in obs_keys],
                                                *[space[k].low for k in goal_keys]]),
                                     np.hstack([*[space[k].high for k in obs_keys],
                                                *[space[k].high for k in goal_keys]]), )

    def step(self, action):
        obs, reward, done, info = self.env.step(action)
        env = self.env
        flat_obs = np.hstack([*[obs[k] for k in self.obs_keys], *[self.env.goal[k] for k in self.goal_keys]])
        return flat_obs, reward, done, info

    def reset(self):
        env = self.env
        obs = self.env.reset()
        return np.hstack([*[obs[k] for k in self.obs_keys], *[self.env.goal[k] for k in self.goal_keys]])

