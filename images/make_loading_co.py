with open('loading_co.txt', 'w') as f:
	for i in range(0, 45200, 400):
		f.write('{} {} {} {}\n'.format(i, 0, 400, 300))