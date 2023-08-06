from gym.envs import register
from metaworld.envs.mujoco.env_dict import ALL_V1_ENVIRONMENTS

ALL_ENVS = []

if __name__ != '__main__':
    for task_name in ALL_V1_ENVIRONMENTS:
        ID = f'{task_name.capitalize()}'
        register(id=ID,
                 entry_point='env_wrappers.metaworld.mw_env:MWEnv',
                 kwargs=dict(task_name=task_name,
                             # width=84, height=84, frame_skip=4
                             ),
                 )
        ALL_ENVS.append(ID)

        ID = f'{task_name[:-3].capitalize()}-fixed{task_name[-3:]}'
        register(id=ID,
                 entry_point='env_wrappers.metaworld.mw_env:MWFixedEnv',
                 kwargs=dict(task_name=task_name,
                             # width=84, height=84, frame_skip=4
                             ),
                 )
        ALL_ENVS.append(ID)
else:
    from cmx import doc

    doc @ """
    # Metaworld Environment Wrappers
    
    > This document, including the embedded video, is generated 
    > by [[cmx]](./__init__.py)
    
    This module includes wrappers that are required to work 
    with `Meta-World` [link](https://github.com/rlworkgroup/metaworld).
    In particular, we implemented a camera wrapper that directly
    taps into the underlying `env.sim.render` function as opposed
    to the gym environment `env.render` which is not implemented
    in metaworld [L:111-113](https://github.com/rlworkgroup/metaworld/blob/master/metaworld/envs/mujoco/mujoco_env.py#L109-L111).
    
    This wrapper makes it easy.
    
    # Usage Example
    
    We register single task Meta-World environments under the 
    `env_wrappers.metaworld` module, so that you can use `gym
    .make` to create the environments without have to import
    `metaworld` manually.
    """
    with doc, doc.table() as t:
        import gym
        from env_wrappers.metaworld import ALL_ENVS

        for i, env_id in enumerate(ALL_ENVS[:]):
            if i % 5 == 0:
                row = t.figure_row()
            env = gym.make(f'env_wrappers.metaworld:{env_id}')
            frames = []
            for i in range(10):
                env.reset()
                env.step(env.action_space.sample())
                frames.append(env.render("rgb", width=240, height=240))
            row.video(frames, f"videos/{env_id}.gif", caption=env_id)
    doc @ """
    The full list of environments are
    """
    doc.yaml @ ALL_ENVS
    doc.flush()

