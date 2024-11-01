class Marker:

	def __init__(self, id, corners):
		self.id = id
		self.corners = corners

		self.x1 = corners[0][0]
		self.y1 = corners[0][1]

		self.x2 = corners[1][0]
		self.y2 = corners[1][1]

		self.x3 = corners[2][0]
		self.y3 = corners[2][1]

		self.x4 = corners[3][0]
		self.y4 = corners[3][1]

		self.x = [self.x1, self.x2, self.x3, self.x4]
		self.y = [self.y1, self.y2, self.y3, self.y4]

def parseMarkers(detected):
	corners = detected[0]
	ids = detected[1]

	markers = []

	for i, corner in enumerate(corners):
		marker = Marker(ids[i][0], corner[0])
		markers.append(marker)

	return markers