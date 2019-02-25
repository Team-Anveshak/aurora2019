import tensorflow as tf
import time
from . import help
from . import flow
from .ops import op_create, identity
from .ops import HEADER, LINE
from .framework import create_framework
from ..dark.darknet import Darknet
import json
import os

class TFNet(object):
	
	# imported methods
	_get_fps = help._get_fps
	say = help.say
	camera = help.camera
	to_darknet = help.to_darknet 			
	return_predict = flow.return_predict
	load_from_ckpt = help.load_from_ckpt

	def __init__(self, FLAGS, darknet = None):
		self.ntrain = 0

		if isinstance(FLAGS, dict):
			from ..defaults import argHandler
			newFLAGS = argHandler()
			newFLAGS.setDefaults()
			newFLAGS.update(FLAGS)
			FLAGS = newFLAGS

		self.FLAGS = FLAGS
		
		if darknet is None:	
			darknet = Darknet(FLAGS)
			self.ntrain = len(darknet.layers)

		self.darknet = darknet
		args = [darknet.meta, FLAGS]
		self.num_layer = len(darknet.layers)
		self.framework = create_framework(*args)
		
		self.meta = darknet.meta

		self.say('\nBuilding net ...')
		start = time.time()
		self.graph = tf.Graph()
		device_name = FLAGS.gpuName \
			if FLAGS.gpu > 0.0 else None
		with tf.device(device_name):
			with self.graph.as_default() as g:
				self.build_forward()
				self.setup_meta_ops()
		self.say('Finished in {}s\n'.format(
			time.time() - start))
	
	# Not sure about its use
	def build_forward(self):
		verbalise = self.FLAGS.verbalise

		# Placeholders
		inp_size = [None] + self.meta['inp_size']
		self.inp = tf.placeholder(tf.float32, inp_size, 'input')
		self.feed = dict() # other placeholders

		# Build the forward pass
		state = identity(self.inp)
		roof = self.num_layer - self.ntrain
		self.say(HEADER, LINE)
		for i, layer in enumerate(self.darknet.layers):
			scope = '{}-{}'.format(str(i),layer.type)
			args = [layer, state, i, roof, self.feed]
			state = op_create(*args)
			mess = state.verbalise()
			self.say(mess)
		self.say(LINE)

		self.top = state
		self.out = tf.identity(state.out, name='output')
