import gym
import numpy as np
from collections import defaultdict

from typing import Sequence


def path_gen(env_id, seed: int, *wrappers, policy=None, collect=None, limit=None, env_kwargs=None, **config):
    """
    :env_id: str the gym environment id
    :*wrappers: positional arguments for the wrapper
    :policy: a policy function that takes in policy(*obs[k] for k in obs_keys)
    :collect: a tuple or None. When None, defaults back to obs_keys
    :limit: the step limit, if the env does not finish before this, there is no traj['done']
    :**env_kwargs: keyvalue arguments for the environment constructor.

    :yields: {
        *collected: numpy array. np.stacked from list of values.
        'success': True  # if the episode is successful. Otherwise returns nothing.
    }
    """

    # todo: add whildcard `*` for obs_keys
    env = gym.make(env_id, **(env_kwargs or {}))
    for w in wrappers:
        env = w(env)
    env.seed(seed)

    new_config = yield "ready"
    config.update({k: v for k, v in (new_config or {}).items() if v is not None})

    try:
        while True:
            obs, done = env.reset(), False
            if isinstance(obs, dict):
                d = {k: [obs[k]] for k in collect or obs.keys() if k in obs}
            else:
                d = {"obs": [obs]}
            path = defaultdict(list, d)
            for step in range(limit or 10):
                if policy is None:
                    action = env.action_space.sample()
                else:
                    action = policy(*[obs[k] for k in collect])
                obs, reward, done, info = env.step(action)
                if isinstance(obs, dict):
                    for k in collect or obs.keys():
                        if k in obs:
                            path[k].append(obs[k])
                else:
                    path['obs'].append(obs)
                path['r'].append(reward)
                path['a'].append(action)
                path['done'].append(done)
                path['info'].append(info)
                if done:
                    path['success'] = True
                    break

            new_config = yield {k: np.stack(v, axis=0) if isinstance(v, Sequence) else v for k, v in path.items()}
            config.update({k: v for k, v in (new_config or {}).items() if v is not None})

    finally:
        print('clean up the environment')
        env.close()


if __name__ == '__main__':
    gen = path_gen("Reacher-v2", seed=100)
    while True:
        traj = next(gen)
        for k, v in traj.items():
            print(f"{k}: Size{v.shape}")
        traj = gen.send(10)
        for k, v in traj.items():
            print(f"{k}: Size{v.shape}")
        break
    # for traj in gen:
    #     for k, v in traj.items():
    #         print(f"{k}: Size{v.shape}")
    #     break
