from random import randint

# =====================================================================
# UTILITIES
# =====================================================================
# Useful random equation meant to better mimic human browsing behavior
def rand_int_with_occassional_big_int(time1,time2,long_wait):
	#Every 1 in this many times, do the long wait
	long_wait_int = randint(1, 20)
	if long_wait_int == 1:
		print("Sleeping for " + str(long_wait) + " seconds")
		return long_wait	# if 1 out of 20 times get the #1, then wait long_wait time
	else:
		sleep_time = randint(time1, time2)
		print("Sleeping for " + str(sleep_time) + " seconds")
		return sleep_time



