#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Null (dummy) security filter
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.libraries.securityfilters import BaseSecurityFilter

class SecurityFilter(BaseSecurityFilter):
	"""
	Dummy security filter implementation.

	NOTE: this security filter provides no authentication, authorisation and
	security over the wire and should _not_ be used in production. It's ideal
	for monitoring network traffic between the agent and client for development
	and debugging purposes, though.
	"""

	def encrypt(data, sender, recipient):
		return data

	def decrypt(data, sender, recipient):
		return data

	def sign(data, sender, recipient):
		return data

	def verify(data, sender, recipient):
		return data
