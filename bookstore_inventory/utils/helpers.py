from datetime import datetime


def format_timestamp(dt=None):
	"""Return a consistent timestamp string for logs and records."""
	dt = dt or datetime.utcnow()
	return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
