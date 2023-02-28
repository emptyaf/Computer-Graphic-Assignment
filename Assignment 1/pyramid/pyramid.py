import numpy as np

from libs.shader import *
from libs import transform as T
from libs.buffer import *
import ctypes
import glfw


class Pyramid(object):
    def __init__(self, vert_shader, frag_shader):
        # self.vertices = np.array(
        #     # YOUR CODE HERE to specify vertex's coordinates
        # )
        #
        # self.indices = np.array(
        #     # YOUR CODE HERE to specify index data
        # )
        #
        # self.normals = # YOUR CODE HERE to compute vertex's normal using the coordinates
        #
        # # colors: RGB format
        # self.colors = np.array(
        #     # YOUR CODE HERE to specify vertex's color
        # )

        self.vertices = np.array([
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5],
            [0, 0, 1],
        ], dtype=np.float32)

        # random normals (facing +z)
        normals = np.random.normal(0, 7, (self.vertices.shape[0], 6)).astype(np.float32)
        normals[:, 3] = np.abs(normals[:, 3])  # (facing +z)
        normals = normals / np.linalg.norm(normals, axis=1, keepdims=True)
        print(normals)

        # indices
        self.indices = np.array(
            [0, 1, 2, 2, 3, 0, 0, 4,
             4, 0, 1, 1, 4,
             4, 1, 2, 2, 4,
             4, 2, 3, 3, 4,
             4, 3, 0])  #np.arange(self.vertex_attrib.shape[0]).astype(np.int32)

        self.colors = np.array([

            [0.0, 0.0, 0.0],  # black
            [1.0, 0.0, 0.0],  # red
            [1.0, 1.0, 0.0],  # yellow
            [0.0, 1.0, 0.0],  # green
            [0.0, 0.0, 1.0],  # blue
            [1.0, 0.0, 1.0],  # magenta
            [1.0, 1.0, 1.0],  # white
            [0.0, 1.0, 1.0]  # cyan
        ], dtype=np.float32)

        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)
        #
     

    """
    Create object -> call setup -> call draw
    """
    def setup(self):
        # setup VAO for drawing cylinder's side
        self.vao.add_vbo(0, self.vertices, ncomponents=3, stride=0, offset=None)
        self.vao.add_vbo(1, self.colors, ncomponents=3, stride=0, offset=None)

        # setup EBO for drawing cylinder's side, bottom and top
        self.vao.add_ebo(self.indices)

        return self

    def draw(self, projection, view, model):
        GL.glUseProgram(self.shader.render_idx)
        modelview = view

        self.uma.upload_uniform_matrix4fv(projection, 'projection', True)
        self.uma.upload_uniform_matrix4fv(modelview, 'modelview', True)

        self.vao.activate()
        GL.glDrawElements(GL.GL_TRIANGLE_STRIP, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)


    def key_handler(self, key):

        if key == glfw.KEY_1:
            self.selected_texture = 1
        if key == glfw.KEY_2:
            self.selected_texture = 2

