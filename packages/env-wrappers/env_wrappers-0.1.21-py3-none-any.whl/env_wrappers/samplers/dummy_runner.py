from itertools import cycle

"""An RL Sampling Running built with (pyTorch) Multiprocessing"""

USE_TORCH_MP = True


class DummyRunner:
    gen_fns = []

    def __init__(self, gen_fns, *args, context_fn=None, **kwargs):
        """
        :param worker:
        :param context_fn: a function you can use to create shared memory objects
        """
        kw = context_fn(None) if callable(context_fn) else {}
        kw.update(kwargs)
        self.gen_fns = [f(*args, **kw) for f in gen_fns]
        self.new_gens = [*self.gen_fns]
        for gen in self.new_gens:
            assert next(gen) == "ready"

    def __repr__(self):
        return f"<DummyRunner>"

    def trajs(self, *msgs, limit=None, **data):
        """ yields full trajectories"""
        if limit:
            data["limit"] = limit
        if data:
            msgs = [*msgs, data] if msgs else data
        for gen in cycle(self.gen_fns):
            yield next(gen) if not msgs else gen.send(msgs)

    def close(self):
        for gen in self.gen_fns:
            gen.close()

    def __del__(self):
        self.close()
