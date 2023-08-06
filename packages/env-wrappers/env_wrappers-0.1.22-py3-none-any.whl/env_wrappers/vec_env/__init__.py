from .dummy_vec_env import DummyVecEnv
from .subproc_vec_env import SubprocVecEnv


def make_env(env_id, seed, *wrappers, **env_kwargs):
    """A delayed function

    :param env_id: environment id (as in gym)
    :param seed: the seed
    :param wrappers: positional arguments as wrappers
    :param env_kwargs: keyword arguments as environment arguments to the gym.make call.
    :return: a thunk calling which creates the environment
    """

    def _thunk():
        import gym

        env = gym.make(env_id, **env_kwargs)
        for w in wrappers:
            env = w(env)
        env.seed(seed)
        return env

    return _thunk
