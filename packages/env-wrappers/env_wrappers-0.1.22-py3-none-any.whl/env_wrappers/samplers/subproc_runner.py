from itertools import cycle

"""An RL Sampling Running built with (pyTorch) Multiprocessing"""

USE_TORCH_MP = True


class CloudpickleWrapper(object):
    """
    Uses cloudpickle to serialize contents (otherwise multiprocessing tries to use pickle)
    """

    def __init__(self, payload):
        self.payload = payload

    def __getstate__(self):
        import cloudpickle
        return cloudpickle.dumps(self.payload)

    def __setstate__(self, ob):
        import pickle
        self.payload = pickle.loads(ob)


def generator_worker(remote, parent_remote, traj_gen: CloudpickleWrapper, *args, **kwargs):
    parent_remote.close()
    traj_gen = traj_gen.payload
    args = [a.payload if isinstance(a, CloudpickleWrapper) else a for a in args]
    kwargs = {k: v.payload if isinstance(v, CloudpickleWrapper) else v for k, v in kwargs.items()}
    gen = traj_gen(*args, **kwargs)
    assert next(gen) == "ready", "generator need to first yield a 'ready' string."
    while True:
        msg = remote.recv()
        traj = gen.send(msg) if msg else next(gen)
        remote.send(traj)


class SubprocRunner:
    def __init__(self, gen_fns, *args, context="spawn", context_fn=None, use_torch_mp=None, **kwargs):
        """
        :param worker:
        :param context_fn: a function you can use to create shared memory objects
        """
        if use_torch_mp is None and not USE_TORCH_MP:
            from multiprocessing import get_context
        else:
            from torch.multiprocessing import get_context

        ctx = get_context(context)
        m = ctx.Manager()
        self.manager = manager = m.__enter__()

        args = [CloudpickleWrapper(a) for a in args]
        kw = context_fn(manager) if callable(context_fn) else {}
        kw.update({k: CloudpickleWrapper(v) for k, v in kwargs.items()})

        self.remotes, work_remotes = zip(*[ctx.Pipe(duplex=True) for _ in range(len(gen_fns))])
        self.pool = [ctx.Process(target=generator_worker,
                                 args=(work_remote, remote, CloudpickleWrapper(gen), *args), kwargs=kw)
                     for work_remote, remote, gen in zip(work_remotes, self.remotes, gen_fns)]

        for p in self.pool:
            p.daemon = True  # if the main process crashes, we should not cause things to hang
            p.start()
        for r in work_remotes:
            r.close()

    def __repr__(self):
        return f"<{self.manager} SubprocRunner>"

    def trajs(self, *msgs, limit=None, **data):
        """ yields full trajectories"""
        if limit:
            data["limit"] = limit
        if data:
            msgs = [*msgs, data] if msgs else data
        for r in self.remotes:
            r.send(msgs)
        for r in cycle(self.remotes):
            if r.poll():
                traj = r.recv()
                r.send(msgs)
                yield traj

    def close(self):
        for p in self.pool:
            p.terminate()
            p.join()
        self.manager.__exit__(None, None, None)

    def __del__(self):
        self.close()
