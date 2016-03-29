from django.apps import AppConfig

import bar.signals


class BarConfig(AppConfig):
	def ready(self):
		return super(BarConfig, super).ready()
