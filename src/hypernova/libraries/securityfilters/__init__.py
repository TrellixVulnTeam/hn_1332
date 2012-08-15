#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Security filter base class
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

class BaseSecurityFilter:
	"""
	Base security filter.

	This class should be used as a base for all security filter implementations.
	It outlines the function prototypes used for encrypting and signing requests
	and responses.
	"""

	def encrypt(data, sender, recipient):
		"""
		Encrypt the supplied data such that it may only be decrypted by the
		desired recipient.
		"""

		pass

	def decrypt(data, sender, recipient):
		"""
		Decrypt the data supplied by the given sender.
		"""

		pass

	def sign(data, sender, recipient):
		"""
		Sign the supplied data to allow the recipient to identify it as
		originating from the sender.
		"""

		pass

	def verify(data, sender, recipient):
		"""
		Verify that the supplied data originated from the sender.
		"""

		pass


def get_security_filter(filter, *args, **kwargs):
	pass
