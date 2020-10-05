def bresenham_line(x0, y0, x1, y1, grid, fill):
	dx = x1 - x0
	dy = y1 - y0
	derr = abs(dy/dx)
	error = 0.0
	y = y0
	for x in range(x0, x1, 1):
		grid[y][x] = fill # can change behavior but for now setting as specified
		error += derr
		if error >= 0.5:
			y += int(dy/abs(dy))
			error -= 1.0

def bresenham_line_y(x0, y0, x1, y1, grid, fill):
	# same by x y flipped except for plotting
	dx = x1 - x0
	dy = y1 - y0
	derr = abs(dx/dy)
	error = 0.0
	x = x0
	for y in range(y0, y1, 1):
		grid[y][x] = fill
		error += derr
		if error >= 0.5:
			x += int(dx/abs(dx))
			error -= 1.0

def plot_line(x0, y0, x1, y1, grid, fill):
	# if dx is less than dy swap x<->y and call basic func
	# before first determine if vertical or horizontal...
	dx = x1 - x0
	dy = y1 - y0
	if dx == 0:
		# plot vertical
		x = x0
		for y in range(y0, y1, int(dy/abs(dy))):
			grid[y][x] = fill
	if dy == 0:
		# plot horizontal
		y = y0
		for x in range(x0, x1, (int(dx/abs(dx)))):
			grid[y][x] = fill

	if abs(dy) > abs(dx):
		if y0 > y1:
			bresenham_line_y(x1, y1, x0, y0, grid, fill)
		else:
			bresenham_line_y(x0, y0, x1, y1, grid, fill)
	else:
		if x0 > x1:
			bresenham_line(x1, y1, x0, y0, grid, fill)
		else:
			bresenham_line(x0, y0, x1, y1, grid, fill)


def bresenham_los_line(x0, y0, x1, y1, grid):
	# TODO problem when flipping start pt, could start in wall...
	# for now fix by not being able to see wall...
	# same but stops when hits wall (i.e. grid[y][x] == 1) and returns set of points
	visible = []
	dx = x1 - x0
	dy = y1 - y0
	derr = abs(dy/dx)
	error = 0.0
	y = y0
	for x in range(x0, x1, int(dx/abs(dx))):
		if grid[y][x] == 1:
			visible.append((x,y))
			return visible
		visible.append((x,y))
		error += derr
		if error >= 0.5:
			y += int(dy/abs(dy))
			error -= 1.0
	return visible

def bresenham_los_line_y(x0, y0, x1, y1, grid):
	# same but stops when hits wall (i.e. grid[y][x] == 1) and returns set of points
	visible = []
	dx = x1 - x0
	dy = y1 - y0
	derr = abs(dx/dy)
	error = 0.0
	x = x0
	for y in range(y0, y1, int(dy/abs(dy))):
		if grid[y][x] == 1:
			visible.append((x,y))
			return visible
		visible.append((x,y))
		error += derr
		if error >= 0.5:
			x += int(dx/abs(dx))
			error -= 1.0
	return visible

def los_line(x0, y0, x1, y1, grid):
	visible = []
	dx = x1 - x0
	dy = y1 - y0
	if dx == 0:
		# plot vertical
		x = x0
		for y in range(y0, y1, int(dy/abs(dy))):
			if grid[y][x] == 1:
				visible.append((x,y))
				return visible
			visible.append((x,y))
		return visible
	if dy == 0:
		# plot horizontal
		y = y0
		for x in range(x0, x1, (int(dx/abs(dx)))):
			if grid[y][x] == 1:
				visible.append((x,y))
				return visible
			visible.append((x,y))
		return visible
	if abs(dy) > abs(dx):
		if y0 > y1:
			#visible = bresenham_los_line_y(x1, y1, x0, y0, grid)
			visible = bresenham_los_line_y(x0, y0, x1, y1, grid)
		else:
			visible = bresenham_los_line_y(x0, y0, x1, y1, grid)
	else:
		if x0 > x1:
			#visible = bresenham_los_line(x1, y1, x0, y0, grid)
			visible = bresenham_los_line(x0, y0, x1, y1, grid)
		else:
			visible = bresenham_los_line(x0, y0, x1, y1, grid)
	return visible