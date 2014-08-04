#!/usr/bin/env python
import math

PHI = (1 + math.sqrt(5)) / 2

class golden_tree(object):
    def __init__(self, length, slope, root_point, gen_order):
        self.length = length
        self.slope = slope
        self.root_point = root_point
        self.end_point = (0, 0)
        self.right_branch = None
        self.left_branch = None
        self.gen_order = gen_order
        self.generate_next_generation()


    def __str__(self):
        return "Root point {0}, End point {1}, Length {2}".format(
             self.root_point, self.end_point, self.length) 


    def _gen_right_branch(self):
        r_len = self.length
        r_slope = 0
        r_root_point = self.end_point
        r_gen_order = self.gen_order - 1
        self.right_branch = golden_tree(r_len, r_slope, r_root_point, r_gen_order)


    def _gen_left_branch(self):
        l_len = self.length / PHI
        l_slope = 0
        l_root_point = self.end_point
        l_gen_order = self.gen_order - 1
        self.left_branch = golden_tree(l_len, l_slope, l_root_point, l_gen_order)


    def walk(self):
        if self.right_branch != None:
            print "Right walk getting called"
            self.right_branch.walk()
        if self.left_branch != None:
            print "Left walk getting called"
            self.left_branch.walk()
        yield self


    def generate_next_generation(self):
        if self.gen_order != 0:
            self._gen_left_branch()
            self._gen_right_branch()



def gimp_run(*args):
    gen_order, length = args
    height = 1000
    width = 1000
    root_point = (int(math.floor(height/3)), int(math.floor(width/2)))
    tree = gen_tree(gen_order, length, root_point)
    img = gimp.Image(height, width, RGB)
    layer = gimp.Layer(img, 'Layer 1', height, width, RGB_IMAGE, 100, NORMAL_MODE)
    img.add_layer(layer, 0)
    pdb.gimp_edit_fill(layer, BACKGROUND_FILL)
    gimp.Display(img)
    gimp.displays_flush()
    gimp.set_foreground(0, 0, 0) 
    drw = pdb.gimp_image_active_drawable(img)
    all_branches = tree.get_all_branches()
    pdb.gimp_message('The list of branches is: {0}'.format(*all_branches))
    for b in all_branches:
        s_x, s_y = b.root_point
        e_x, e_y = b.end_point
        ctrl_points = [s_x, s_y, e_x, e_y]
        pdb.gimp_paintbrush_default(drw, len(ctrl_points), ctrl_points)
    gimp.displays_flush()


################################################################################
# Entry points: either it is a plugin for the gimp or we are debuggin the class
# on the terminal
################################################################################
try:
    from gimpfu import *
    register(
        "golden_tree_gen", "", "", "", "", "",
        "<Toolbox>/Xtns/Languages/Python-Fu/_Golden Tree Generator", "",
        [
            (PF_INT,    "arg0", "The number of generations deep the tree will be", 4),
            (PF_INT,    "arg1", "Length of the root branch", 30),
        ],
        [],
        gimp_run
        )
    main()
except ImportError:
    if __name__ == '__main__':
        # We must be on the terminal debugging....
        gen_order = 4
        length = 30
        root_point = (333, 500)
        slope = 0
        tree = golden_tree(length, slope, root_point, gen_order)
        for branch in tree.walk():
            print(branch)
