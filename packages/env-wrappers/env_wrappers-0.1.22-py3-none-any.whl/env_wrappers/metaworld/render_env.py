from gym import Wrapper
from mujoco_py import MjViewer, MjRenderContextOffscreen


class RenderEnv(Wrapper):
    def __init__(self, env,
                 cam_id=None, cam_pos=None, cam_angle=None, cameras=None,
                 view="left", zoom=1.0,
                 width=84, height=None, ):
        super().__init__(env)
        self.env = env
        self.cam_id = cam_id
        self.cam_pos = cam_pos
        self.cam_angle = cam_angle
        self.cameras = cameras or []
        self.width = width
        self.height = height
        self.unwrapped._view = view
        self.unwrapped._zoom = zoom

        def viewer_setup(self):
            # note: this is the front (left side) view. rotate
            #  side-ways for stereo or to avoid occlusion with
            #  some of the tasks
            #  Some of the reference camera views can be found
            #  here: https://github.com/rlworkgroup/metaworld/issues/35
            if self._view == "frontal":
                self.viewer.cam.azimuth = 270
                self.viewer.cam.elevation = -40
                self.viewer.cam.distance = 0.6 * self._zoom
                self.viewer.cam.lookat[0] = 0
                self.viewer.cam.lookat[1] = 0.9
                self.viewer.cam.lookat[2] = 0.3
            elif self._view == "left":
                self.viewer.cam.azimuth = 0
                self.viewer.cam.elevation = -20
                self.viewer.cam.distance = 0.4 * self._zoom
                self.viewer.cam.lookat[0] = -0.4
                self.viewer.cam.lookat[1] = 0.575
                self.viewer.cam.lookat[2] = 0.3

        # this is the most damming change
        def _get_viewer(self, mode):
            self.viewer = self._viewers.get(mode)
            if self.viewer is None:
                if mode == 'human':
                    self.viewer = MjViewer(self.sim)
                else:
                    self.viewer = MjRenderContextOffscreen(self.sim, -1)
                self.viewer_setup()
                self._viewers[mode] = self.viewer
            self.viewer_setup()
            return self.viewer

        def close(self):
            self.viewer = None
            self._viewers.clear()

            for viewer in self._viewers.items():
                import glfw
                glfw.destroy_window(viewer.window)

        # monkey patch here
        from functools import partial
        self.unwrapped.viewer_setup = partial(viewer_setup, self=self.unwrapped)
        self.unwrapped._get_viewer = lambda mode: _get_viewer(self.unwrapped, mode)
        self.unwrapped.close = lambda: close(self)

    def reset(self):
        env = self.unwrapped
        obs = self.env.reset()

        old = env.viewer
        for env.viewer in env._viewers.values():
            self.viewer_setup()
        env.viewer = old
        return obs

    def render(self, mode="human", width=None, height=None):
        width = width or self.width
        height = height or self.height or width

        if mode == "human":
            return self.unwrapped.render(mode, width=None, height=None)

        viewer = self.unwrapped._get_viewer(mode)
        viewer.render(width, height)
        data = viewer.read_pixels(width, height, depth=False)
        return data[::-1]

    def close(self):
        try:
            self.unwrapped.close()
            delattr(self, "unwrapped")
        except:
            pass