import pyglet
from pyglet.gl import *
from pyglet.window import key


class BoxModel:
    def __init__(self, d, image_file):
        self.image_file = image_file
        self.d = d
        self.textures = []
        self.image = None
        self.load_target()

    def load_target(self):
        self.image = pyglet.image.load(self.image_file)
        self.textures.append(self.image.get_texture())

    def draw(self):
        glEnable(self.textures[-1].target)
        glBindTexture(self.textures[-1].target, self.textures[-1].id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.image.width, self.image.height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE,
                     self.image.get_image_data().get_data('RGBA',
                                                          self.image.width * 4))
        b = self.d
        a = -self.d
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(a, a, a)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(a, a, b)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(a, b, b)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(a, b, a)
        glEnd()

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(b, a, b)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(b, a, a)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(b, b, a)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(b, b, b)
        glEnd()

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(a, a, a)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(b, a, a)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(b, a, b)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(a, a, b)
        glEnd()

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(a, a, a)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(a, a, b)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(a, b, b)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(a, b, a)
        glEnd()

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(b, a, a)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(a, a, a)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(a, b, a)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(b, b, a)
        glEnd()

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(a, a, b)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(b, a, b)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(b, b, b)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(a, b, b)
        glEnd()

        glDisable(self.textures[-1].target)


class ViewCoords:
    def __init__(self):
        self.tx = self.ty = 0
        self.tz = -50
        self.rx = self.ry = self.rz = 0

    def trans_rotate(self):
        glLoadIdentity()
        glTranslatef(self.tx, self.ty, self.tz)
        glRotatef(self.rx, 1, 0, 0)
        glRotatef(self.ry, 0, 1, 0)
        glRotatef(self.rz, 0, 0, 1)


window = pyglet.window.Window(width=800, height=600, caption='QUADS', resizable=True)
gl.glClearColor(0, 0.3, 0.5, 0)
keys = key.KeyStateHandler()
window.push_handlers(keys)
vc = ViewCoords()
box = BoxModel(5, 'images/brick.png')


@window.event
def on_draw():
    glClear(gl.GL_COLOR_BUFFER_BIT)
    vc.trans_rotate()
    box.draw()


@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glu.gluPerspective(45.0, width / float(height), 0.5, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    return pyglet.event.EVENT_HANDLED


def update_frame(dt):
    if keys[pyglet.window.key.UP]:
        vc.rx += 5
    if keys[pyglet.window.key.DOWN]:
        vc.rx -= 5
    if keys[pyglet.window.key.LEFT]:
        vc.ry += 5
    if keys[pyglet.window.key.RIGHT]:
        vc.ry -= 5


@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    vc.tz -= scroll_y * 2.0


if __name__ == '__main__':
    pyglet.clock.schedule_interval(update_frame, 0.05)
    pyglet.app.run()
