from mainloop import generationRunThrough

GENERATIONS = 50
DURATION_LIMIT = 60 #seconds
AI_NUM = 50

for i in range(GENERATIONS):
    carList = generationRunThrough(DURATION_LIMIT, AI_NUM)
